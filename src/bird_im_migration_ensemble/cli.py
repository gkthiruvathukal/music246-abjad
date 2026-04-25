"""Command-line interface for Bird Im-Migration Ensemble."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import abjad
import mido

from audio_rendering import normalize_wav, run_audio_command
from algorithmic_piano_quartet_no2.soundfonts import ensure_soundfont
from jazz_rhythm.render import render_clap_wav
from .generator import build_ensemble_piece
from .score import build_lilypond_file


STEM = "bird-im-migration-ensemble"
DEFAULT_SALAMANDER = "~/.soundfonts/SalamanderGrandPiano-V3+20200602.sf2"
DEFAULT_AEGEAN = "~/.soundfonts/AegeanSymphonicOrchestra.sf2"


def write_ly(lilypond_file, output_dir: str, stem: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{stem}.ly")
    with open(ly_path, "w", encoding="utf-8") as file_pointer:
        file_pointer.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def compile_lilypond(ly_path: str, output_dir: str, stem: str, formats: set[str]) -> None:
    output_stem = os.path.join(output_dir, stem)
    cmd = ["lilypond", "-o", output_stem, ly_path]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")

    if "pdf" not in formats:
        pdf_path = f"{output_stem}.pdf"
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print(f"Removed {pdf_path} (not requested)")

    if "midi" not in formats:
        for entry in os.listdir(output_dir):
            if entry.startswith(stem) and entry.endswith(".midi"):
                path = os.path.join(output_dir, entry)
                os.remove(path)
                print(f"Removed {path} (not requested)")


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
            raw_wav_path = Path(temp_dir) / "ensemble-raw.wav"
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


def _channels_for_prefixes(midi: mido.MidiFile, prefixes: set[str]) -> set[int]:
    channels: set[int] = set()
    for track in midi.tracks:
        track_name = track.name.split(":", 1)[0] if getattr(track, "name", "") else ""
        if track_name not in prefixes:
            continue
        for message in track:
            if hasattr(message, "channel"):
                channels.add(message.channel)
    return channels


def _write_filtered_midi(
    midi: mido.MidiFile,
    channels: set[int],
    output_path: Path,
    *,
    channel_map: dict[int, int] | None = None,
    force_program: int | None = None,
) -> None:
    filtered = mido.MidiFile(type=midi.type, ticks_per_beat=midi.ticks_per_beat)
    for track in midi.tracks:
        new_track = mido.MidiTrack()
        pending_time = 0
        program_injected = False
        for message in track:
            message_time = pending_time + message.time
            if hasattr(message, "channel") and message.channel not in channels:
                pending_time = message_time
                continue
            pending_time = 0
            copied = message.copy(time=message_time)
            if hasattr(copied, "channel") and channel_map is not None:
                copied = copied.copy(channel=channel_map.get(copied.channel, copied.channel))
            if copied.type == "program_change" and force_program is not None:
                copied = copied.copy(program=force_program)
                program_injected = True
            new_track.append(copied)
            if (
                force_program is not None
                and channel_map is not None
                and not program_injected
                and hasattr(copied, "channel")
                and copied.type in {"note_on", "note_off"}
            ):
                new_track.insert(
                    len(new_track) - 1,
                    mido.Message(
                        "program_change",
                        channel=copied.channel,
                        program=force_program,
                        time=0,
                    ),
                )
                program_injected = True
        if not new_track or new_track[-1].type != "end_of_track":
            new_track.append(mido.MetaMessage("end_of_track", time=pending_time))
        filtered.tracks.append(new_track)
    filtered.save(output_path)


def mix_wavs(input_paths: list[str], output_path: str, *, weights: list[float] | None = None) -> None:
    if len(input_paths) == 1:
        source = input_paths[0]
        if source != output_path:
            Path(output_path).write_bytes(Path(source).read_bytes())
        print(f"Wrote {output_path}")
        return

    cmd = ["ffmpeg", "-y"]
    for input_path in input_paths:
        cmd.extend(["-i", input_path])
    filter_complex = None
    if weights is not None:
        if len(weights) != len(input_paths):
            raise ValueError("weights must match input_paths length")
        stage_names: list[str] = []
        for index, weight in enumerate(weights):
            stage = f"a{index}"
            stage_names.append(f"[{stage}]")
            cmd_label = f"[{index}:a]volume={weight}[{stage}]"
            filter_complex = cmd_label if filter_complex is None else f"{filter_complex};{cmd_label}"
        mix_inputs = "".join(stage_names)
        filter_complex = (
            f"{filter_complex};{mix_inputs}amix=inputs={len(input_paths)}:duration=longest:normalize=0"
        )
    else:
        filter_complex = f"amix=inputs={len(input_paths)}:duration=longest:normalize=0"
    cmd.extend(
        [
            "-filter_complex",
            filter_complex,
            "-c:a",
            "pcm_s16le",
            output_path,
        ]
    )
    run_audio_command(cmd, wrote_path=output_path)


def _movement_midi_paths(output_dir: str, stem: str) -> list[str]:
    def sort_key(entry: str) -> tuple[int, str]:
        if entry == f"{stem}.midi":
            return (0, entry)
        prefix = f"{stem}-"
        suffix = entry[len(prefix):-5]
        if entry.startswith(prefix) and suffix.isdigit():
            return (int(suffix) + 1, entry)
        return (10_000, entry)

    midi_files = [
        os.path.join(output_dir, entry)
        for entry in sorted(
            (
                entry
                for entry in os.listdir(output_dir)
                if entry.startswith(stem) and entry.endswith(".midi")
            ),
            key=sort_key,
        )
    ]
    return midi_files


def _movement_wav_name(stem: str, index: int) -> str:
    if index <= 3:
        return f"{stem}-mvt{index}.wav"
    appendix_index = index - 3
    return f"{stem}-appendix-a{appendix_index}.wav"


# [docs:layered-render:start]
def render_layered_wav_for_midi(
    midi_path: str,
    wav_path: str,
    piano_soundfont_path: str,
    ensemble_soundfont_path: str,
    sample_rate: int,
) -> None:
    midi = mido.MidiFile(midi_path)
    piano_rh_channels = _channels_for_prefixes(midi, {"piano_rh"})
    piano_lh_channels = _channels_for_prefixes(midi, {"piano_lh"})
    ensemble_channels = _channels_for_prefixes(midi, {"violin", "trumpet"})
    percussion_channels = _channels_for_prefixes(midi, {"percussion"})

    if not piano_rh_channels or not piano_lh_channels or not ensemble_channels:
        render_wav(midi_path, wav_path, ensemble_soundfont_path, sample_rate)
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        piano_rh_midi = Path(temp_dir) / "ensemble-piano-rh.midi"
        piano_lh_midi = Path(temp_dir) / "ensemble-piano-lh.midi"
        ensemble_midi = Path(temp_dir) / "ensemble-other.midi"
        percussion_midi = Path(temp_dir) / "ensemble-percussion.midi"
        piano_rh_wav = Path(temp_dir) / "ensemble-piano-rh.wav"
        piano_lh_wav = Path(temp_dir) / "ensemble-piano-lh.wav"
        ensemble_wav = Path(temp_dir) / "ensemble-other.wav"
        percussion_wav = Path(temp_dir) / "ensemble-percussion.wav"
        mixed_wav = Path(temp_dir) / "ensemble-mix.wav"

        _write_filtered_midi(
            midi,
            piano_rh_channels,
            piano_rh_midi,
            channel_map={channel: 0 for channel in piano_rh_channels},
            force_program=0,
        )
        _write_filtered_midi(
            midi,
            piano_lh_channels,
            piano_lh_midi,
            channel_map={channel: 0 for channel in piano_lh_channels},
            force_program=0,
        )
        _write_filtered_midi(midi, ensemble_channels, ensemble_midi)
        if percussion_channels:
            _write_filtered_midi(midi, percussion_channels, percussion_midi)

        render_wav(str(piano_rh_midi), str(piano_rh_wav), piano_soundfont_path, sample_rate, normalize_output=False)
        render_wav(str(piano_lh_midi), str(piano_lh_wav), piano_soundfont_path, sample_rate, normalize_output=False)
        render_wav(str(ensemble_midi), str(ensemble_wav), ensemble_soundfont_path, sample_rate, normalize_output=False)
        layers = [str(piano_lh_wav), str(piano_rh_wav), str(ensemble_wav)]
        weights = [1.8, 1.0, 0.9]
        if percussion_channels:
            render_clap_wav(str(percussion_midi), str(percussion_wav), sample_rate=sample_rate)
            layers.append(str(percussion_wav))
            weights.append(0.8)
        mix_wavs(layers, str(mixed_wav), weights=weights)
        normalize_wav(str(mixed_wav), wav_path, sample_rate)
# [docs:layered-render:end]


# [docs:movement-render-order:start]
def render_full_wav(
    *,
    output_dir: str,
    stem: str,
    piano_soundfont_path: str,
    ensemble_soundfont_path: str,
    sample_rate: int,
) -> None:
    midi_paths = _movement_midi_paths(output_dir, stem)
    if not midi_paths:
        raise FileNotFoundError("No MIDI files found to render.")

    movement_wavs: list[str] = []
    for index, midi_path in enumerate(midi_paths, start=1):
        movement_wav = os.path.join(output_dir, _movement_wav_name(stem, index))
        render_layered_wav_for_midi(
            midi_path=midi_path,
            wav_path=movement_wav,
            piano_soundfont_path=piano_soundfont_path,
            ensemble_soundfont_path=ensemble_soundfont_path,
            sample_rate=sample_rate,
        )
        movement_wavs.append(movement_wav)

    with tempfile.TemporaryDirectory() as temp_dir:
        concat_list = os.path.join(temp_dir, "concat.txt")
        raw_output_wav = os.path.join(temp_dir, f"{stem}-raw.wav")
        Path(concat_list).write_text(
            "".join(f"file '{Path(path).resolve()}'\n" for path in movement_wavs),
            encoding="utf-8",
        )
        output_wav = os.path.join(output_dir, f"{stem}.wav")
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_list,
            "-c",
            "copy",
            raw_output_wav,
        ]
        run_audio_command(cmd, wrote_path=raw_output_wav)
        normalize_wav(raw_output_wav, output_wav, sample_rate)
# [docs:movement-render-order:end]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Bird Im-Migration Ensemble from curated bird phrases.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="build",
        help="directory for generated files (default: build)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="random seed for phrase ordering and responses (default: 7)",
    )
    parser.add_argument(
        "--stem",
        default=STEM,
        help=f"override output stem (default: {STEM})",
    )

    group = parser.add_argument_group("output formats")
    group.add_argument("--ly", action="store_true", default=False, help="generate .ly file only")
    group.add_argument("--pdf", action="store_true", default=False, help="compile and produce PDF")
    group.add_argument("--midi", action="store_true", default=False, help="compile and produce MIDI")
    group.add_argument("--wav", action="store_true", default=False, help="render WAV")
    parser.add_argument(
        "--piano-soundfont",
        default=DEFAULT_SALAMANDER,
        help=f"piano soundfont path (default: {DEFAULT_SALAMANDER})",
    )
    parser.add_argument(
        "--ensemble-soundfont",
        default=DEFAULT_AEGEAN,
        help=f"ensemble soundfont path (default: {DEFAULT_AEGEAN})",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=44100,
        help="sample rate for WAV rendering (default: 44100)",
    )

    args = parser.parse_args(argv)
    if not (args.ly or args.pdf or args.midi or args.wav):
        args.ly = True
        args.pdf = True
        args.midi = True
    return args


def main(argv=None):
    args = parse_args(argv)
    piece = build_ensemble_piece(seed=args.seed)
    lilypond_file = build_lilypond_file(piece)
    ly_path = write_ly(lilypond_file, args.output_dir, args.stem)

    formats_to_compile: set[str] = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    if args.midi:
        formats_to_compile.add("midi")
    if args.wav:
        formats_to_compile.add("midi")
    if formats_to_compile:
        compile_lilypond(ly_path, args.output_dir, args.stem, formats_to_compile)
    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")

    if args.wav:
        render_full_wav(
            output_dir=args.output_dir,
            stem=args.stem,
            piano_soundfont_path=args.piano_soundfont,
            ensemble_soundfont_path=args.ensemble_soundfont,
            sample_rate=args.sample_rate,
        )


if __name__ == "__main__":
    main()
