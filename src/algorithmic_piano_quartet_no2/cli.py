"""CLI for building Algo Rhythms Quartet No. 2."""

from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import abjad
import mido

from audio_rendering import normalize_wav, run_audio_command
from .config import load_config
from .generator import compose_piece
from .score import build_lilypond_file
from .soundfonts import ensure_soundfont


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Algo Rhythms Quartet No. 2 from TOML config.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="configs/algorithmic-piano-quartet-no2.toml",
        help="path to TOML config (default: configs/algorithmic-piano-quartet-no2.toml)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="build",
        help="directory for generated files (default: build)",
    )
    parser.add_argument(
        "--measures",
        type=int,
        default=None,
        help="override the number of measures from the config",
    )
    parser.add_argument(
        "--tempo",
        type=int,
        default=None,
        help="override tempo in quarter-notes per minute from the config",
    )

    group = parser.add_argument_group("output formats")
    group.add_argument("--ly", action="store_true", default=False, help="generate .ly")
    group.add_argument("--pdf", action="store_true", default=False, help="generate PDF")
    group.add_argument("--midi", action="store_true", default=False, help="generate MIDI")
    group.add_argument("--wav", action="store_true", default=False, help="render WAV via fluidsynth")
    parser.add_argument(
        "--soundfont",
        default=None,
        help="override soundfont path from config",
    )

    args = parser.parse_args(argv)
    if not (args.ly or args.pdf or args.midi or args.wav):
        args.ly = True
        args.pdf = True
        args.midi = True
    return args


def write_ly(lilypond_file, output_dir: str, stem: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{stem}.ly")
    with open(ly_path, "w", encoding="utf-8") as file_pointer:
        file_pointer.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def build_output_stem(config) -> str:
    parts = [config.output.basename]
    if config.output.label:
        parts.append(config.output.label)
    if config.output.include_measures:
        parts.append(f"m{config.generation.measures}")
    if config.output.include_tempo:
        parts.append(f"t{config.generation.tempo_bpm}")
    if config.output.include_seed:
        parts.append(f"s{config.generation.seed}")
    if config.output.include_timestamp:
        stamp = datetime.now().strftime(config.output.timestamp_format)
        parts.append(stamp)
    return "-".join(parts)


def compile_lilypond(ly_path: str, output_dir: str, stem: str, fmt: set[str]) -> None:
    cmd = ["lilypond", "-o", os.path.join(output_dir, stem), ly_path]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")

    if "pdf" not in fmt:
        pdf_path = os.path.join(output_dir, f"{stem}.pdf")
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    if "midi" not in fmt:
        midi_path = os.path.join(output_dir, f"{stem}.midi")
        if os.path.exists(midi_path):
            os.remove(midi_path)


def render_wav(
    midi_path: str,
    wav_path: str,
    soundfont_path: str,
    sample_rate: int,
    *,
    normalize_output: bool = True,
) -> None:
    soundfont = ensure_soundfont(soundfont_path)
    if normalize_output:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_wav_path = Path(temp_dir) / "quartet-raw.wav"
            cmd = [
                "fluidsynth",
                "-ni",
                "-F",
                str(raw_wav_path),
                "-r",
                str(sample_rate),
                str(soundfont),
                midi_path,
            ]
            run_audio_command(cmd, wrote_path=str(raw_wav_path))
            normalize_wav(str(raw_wav_path), wav_path, sample_rate)
        return

    cmd = [
        "fluidsynth",
        "-ni",
        "-F",
        wav_path,
        "-r",
        str(sample_rate),
        str(soundfont),
        midi_path,
    ]
    run_audio_command(cmd, wrote_path=wav_path)


def render_layered_wav(
    midi_path: str,
    wav_path: str,
    piano_soundfont_path: str,
    strings_soundfont_path: str,
    sample_rate: int,
) -> None:
    midi = mido.MidiFile(midi_path)
    piano_channels = _channels_for_prefixes(midi, {"piano_rh", "piano_lh"})
    strings_channels = _channels_for_prefixes(midi, {"violin", "viola", "cello"})

    if not piano_channels or not strings_channels:
        raise ValueError("Could not detect distinct piano and string MIDI channels for layered rendering.")

    with tempfile.TemporaryDirectory() as temp_dir:
        piano_midi = Path(temp_dir) / "quartet-piano.midi"
        strings_midi = Path(temp_dir) / "quartet-strings.midi"
        piano_wav = Path(temp_dir) / "quartet-piano.wav"
        strings_wav = Path(temp_dir) / "quartet-strings.wav"
        raw_wav = Path(temp_dir) / "quartet-mix.wav"

        _write_filtered_midi(midi, piano_channels, piano_midi)
        _write_filtered_midi(midi, strings_channels, strings_midi)

        render_wav(str(piano_midi), str(piano_wav), piano_soundfont_path, sample_rate, normalize_output=False)
        render_wav(str(strings_midi), str(strings_wav), strings_soundfont_path, sample_rate, normalize_output=False)
        mix_wavs(str(piano_wav), str(strings_wav), str(raw_wav))
        normalize_wav(str(raw_wav), wav_path, sample_rate)


def _channels_for_prefixes(midi: mido.MidiFile, prefixes: set[str]) -> set[int]:
    channels: set[int] = set()
    for track in midi.tracks:
        track_name = track.name.split(":", 1)[0] if getattr(track, "name", "") else ""
        if track_name not in prefixes:
            continue
        for msg in track:
            if hasattr(msg, "channel"):
                channels.add(msg.channel)
    return channels


def _write_filtered_midi(midi: mido.MidiFile, channels: set[int], output_path: Path) -> None:
    filtered = mido.MidiFile(type=midi.type, ticks_per_beat=midi.ticks_per_beat)
    for track in midi.tracks:
        new_track = mido.MidiTrack()
        pending_time = 0
        for msg in track:
            msg_time = pending_time + msg.time
            if hasattr(msg, "channel") and msg.channel not in channels:
                pending_time = msg_time
                continue
            pending_time = 0
            new_track.append(msg.copy(time=msg_time))
        if not new_track or new_track[-1].type != "end_of_track":
            new_track.append(mido.MetaMessage("end_of_track", time=pending_time))
        filtered.tracks.append(new_track)
    filtered.save(output_path)


def mix_wavs(piano_wav_path: str, strings_wav_path: str, output_path: str) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        piano_wav_path,
        "-i",
        strings_wav_path,
        "-filter_complex",
        "amix=inputs=2:duration=longest:normalize=0",
        "-c:a",
        "pcm_s16le",
        output_path,
    ]
    run_audio_command(cmd, wrote_path=output_path)


def main(argv=None):
    args = parse_args(argv)
    config = load_config(args.config)
    generation = config.generation
    if args.measures is not None:
        generation = replace(generation, measures=args.measures)
    if args.tempo is not None:
        generation = replace(generation, tempo_bpm=args.tempo)
    if generation is not config.generation:
        config = replace(config, generation=generation)
    stem = build_output_stem(config)
    piece = compose_piece(config)
    lilypond_file = build_lilypond_file(piece)
    ly_path = write_ly(lilypond_file, args.output_dir, stem)

    formats_to_compile = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    if args.midi:
        formats_to_compile.add("midi")
    if args.wav:
        formats_to_compile.add("midi")

    if formats_to_compile:
        compile_lilypond(ly_path, args.output_dir, stem, formats_to_compile)
    elif args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")

    if args.wav:
        midi_path = os.path.join(args.output_dir, f"{stem}.midi")
        wav_path = os.path.join(args.output_dir, f"{stem}.wav")
        if args.soundfont:
            render_wav(
                midi_path=midi_path,
                wav_path=wav_path,
                soundfont_path=args.soundfont,
                sample_rate=config.render.sample_rate,
            )
        elif config.render.piano_soundfont and config.render.strings_soundfont:
            render_layered_wav(
                midi_path=midi_path,
                wav_path=wav_path,
                piano_soundfont_path=config.render.piano_soundfont,
                strings_soundfont_path=config.render.strings_soundfont,
                sample_rate=config.render.sample_rate,
            )
        elif config.render.soundfont:
            render_wav(
                midi_path=midi_path,
                wav_path=wav_path,
                soundfont_path=config.render.soundfont,
                sample_rate=config.render.sample_rate,
            )
        else:
            raise ValueError(
                "WAV rendering requires --soundfont, [render].soundfont, "
                "or both [render].piano_soundfont and [render].strings_soundfont."
            )


if __name__ == "__main__":
    main()
