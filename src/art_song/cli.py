"""Command-line interface for generating the Art Song scaffold."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import abjad
import mido

from algorithmic_piano_quartet_no2.soundfonts import ensure_soundfont

from .score import (
    build_part_lilypond_file,
    build_chord_voicing_cheat_sheet,
    build_lilypond_file,
)

STEM = "art-song"
PARTS = ["voice", "violin", "viola", "trumpet-c", "trumpet-bb", "piano"]
DEFAULT_SALAMANDER = "~/.soundfonts/SalamanderGrandPiano-V3+20200602.sf2"
DEFAULT_AEGEAN = "~/.soundfonts/AegeanSymphonicOrchestra.sf2"
PROGRAM_VOICE = 52
PROGRAM_VIOLIN = 40
PROGRAM_VIOLA = 41
PROGRAM_TRUMPET = 56


def write_ly(lilypond_file, output_dir, stem=STEM) -> str:
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{stem}.ly")
    with open(ly_path, "w") as file_pointer:
        file_pointer.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def write_cheat_sheet(output_dir) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{STEM}-chord-voicings.md")
    with open(path, "w") as file_pointer:
        file_pointer.write(build_chord_voicing_cheat_sheet())
    print(f"Wrote {path}")
    return path


def render_wav(
    midi_path: str,
    wav_path: str,
    soundfont_path: str,
    sample_rate: int,
) -> None:
    soundfont = ensure_soundfont(soundfont_path)
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
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")
    print(f"Wrote {wav_path}")


def _channels_for_prefixes(midi: mido.MidiFile, prefixes: set[str]) -> set[int]:
    channels: set[int] = set()
    normalized_prefixes = {prefix.lower() for prefix in prefixes}
    for track in midi.tracks:
        track_name = track.name.split(":", 1)[0].strip().lower() if getattr(track, "name", "") else ""
        if track_name not in normalized_prefixes:
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
            stage_filter = f"[{index}:a]volume={weight}[{stage}]"
            filter_complex = stage_filter if filter_complex is None else f"{filter_complex};{stage_filter}"
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
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")
    print(f"Wrote {output_path}")


def normalize_wav(
    input_path: str,
    output_path: str,
    sample_rate: int,
    *,
    integrated_loudness: float = -16.0,
    true_peak: float = -1.5,
    loudness_range: float = 11.0,
) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-af",
        (
            "loudnorm="
            f"I={integrated_loudness}:"
            f"TP={true_peak}:"
            f"LRA={loudness_range}"
        ),
        "-ar",
        str(sample_rate),
        "-c:a",
        "pcm_s16le",
        output_path,
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")
    print(f"Wrote {output_path}")


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
    voice_channels = _channels_for_prefixes(midi, {"voice"})
    violin_channels = _channels_for_prefixes(midi, {"violin"})
    viola_channels = _channels_for_prefixes(midi, {"viola"})
    trumpet_channels = _channels_for_prefixes(midi, {"trumpet in c", "trumpet"})

    if not piano_rh_channels and not piano_lh_channels:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_wav_path = Path(temp_dir) / "art-song-raw.wav"
            render_wav(midi_path, str(raw_wav_path), ensemble_soundfont_path, sample_rate)
            normalize_wav(str(raw_wav_path), wav_path, sample_rate)
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        layers: list[str] = []
        weights: list[float] = []
        raw_wav_path = Path(temp_dir) / "art-song-raw.wav"

        def add_layer(
            stem: str,
            channels: set[int],
            *,
            soundfont_path: str,
            output_channel: int = 0,
            force_program: int | None = None,
            weight: float = 1.0,
        ) -> None:
            if not channels:
                return
            midi_layer = Path(temp_dir) / f"{stem}.midi"
            wav_layer = Path(temp_dir) / f"{stem}.wav"
            _write_filtered_midi(
                midi,
                channels,
                midi_layer,
                channel_map={channel: output_channel for channel in channels},
                force_program=force_program,
            )
            render_wav(str(midi_layer), str(wav_layer), soundfont_path, sample_rate)
            layers.append(str(wav_layer))
            weights.append(weight)

        add_layer(
            "art-song-piano-rh",
            piano_rh_channels,
            soundfont_path=piano_soundfont_path,
            force_program=0,
            weight=1.0,
        )
        add_layer(
            "art-song-piano-lh",
            piano_lh_channels,
            soundfont_path=piano_soundfont_path,
            force_program=0,
            weight=1.5,
        )
        add_layer(
            "art-song-voice",
            voice_channels,
            soundfont_path=ensemble_soundfont_path,
            force_program=PROGRAM_VOICE,
            weight=1.1,
        )
        add_layer(
            "art-song-violin",
            violin_channels,
            soundfont_path=ensemble_soundfont_path,
            force_program=PROGRAM_VIOLIN,
            weight=0.9,
        )
        add_layer(
            "art-song-viola",
            viola_channels,
            soundfont_path=ensemble_soundfont_path,
            force_program=PROGRAM_VIOLA,
            weight=0.85,
        )
        add_layer(
            "art-song-trumpet",
            trumpet_channels,
            soundfont_path=ensemble_soundfont_path,
            force_program=PROGRAM_TRUMPET,
            weight=0.8,
        )

        if not layers:
            raise FileNotFoundError("Could not detect instrument channels in MIDI for WAV rendering.")

        mix_wavs(layers, str(raw_wav_path), weights=weights)
        normalize_wav(str(raw_wav_path), wav_path, sample_rate)


def compile_lilypond(ly_path, output_dir, fmt, stem=STEM) -> None:
    output_stem = os.path.join(output_dir, stem)
    cmd = ["lilypond", "-o", output_stem, ly_path]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    if result.stderr:
        print(result.stderr, end="")

    if "pdf" not in fmt:
        pdf = f"{output_stem}.pdf"
        if os.path.exists(pdf):
            os.remove(pdf)
            print(f"Removed {pdf} (not requested)")

    if "midi" not in fmt:
        for entry in os.listdir(output_dir):
            if entry.startswith(stem) and entry.endswith(".midi"):
                path = os.path.join(output_dir, entry)
                os.remove(path)
                print(f"Removed {path} (not requested)")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate the Art Song scaffold from Abjad.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="build",
        help="directory for generated files (default: build)",
    )

    group = parser.add_argument_group("output formats")
    group.add_argument(
        "--ly",
        action="store_true",
        default=False,
        help="generate .ly file only (no compilation)",
    )
    group.add_argument(
        "--pdf",
        action="store_true",
        default=False,
        help="compile and produce PDF",
    )
    group.add_argument(
        "--midi",
        action="store_true",
        default=False,
        help="compile and produce MIDI",
    )
    group.add_argument(
        "--wav",
        action="store_true",
        default=False,
        help="render WAV from MIDI using soundfonts",
    )
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
        help="WAV sample rate for FluidSynth output (default: 44100)",
    )

    args = parser.parse_args(argv)

    if not (args.ly or args.pdf or args.midi or args.wav):
        args.ly = True
        args.pdf = True
        args.midi = True
    if args.wav:
        args.midi = True
        args.pdf = True

    return args


def main(argv=None):
    args = parse_args(argv)
    lilypond_file = build_lilypond_file()
    ly_path = write_ly(lilypond_file, args.output_dir)
    part_paths = {
        part: write_ly(build_part_lilypond_file(part), args.output_dir, stem=f"{STEM}-{part}")
        for part in PARTS
    }
    write_cheat_sheet(args.output_dir)

    formats_to_compile = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    if args.midi:
        formats_to_compile.add("midi")

    if formats_to_compile:
        compile_lilypond(ly_path, args.output_dir, formats_to_compile)
        if args.pdf:
            for part, part_path in part_paths.items():
                compile_lilypond(part_path, args.output_dir, {"pdf"}, stem=f"{STEM}-{part}")
        if args.wav:
            render_layered_wav_for_midi(
                midi_path=os.path.join(args.output_dir, f"{STEM}.midi"),
                wav_path=os.path.join(args.output_dir, f"{STEM}.wav"),
                piano_soundfont_path=args.piano_soundfont,
                ensemble_soundfont_path=args.ensemble_soundfont,
                sample_rate=args.sample_rate,
            )

    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")


if __name__ == "__main__":
    main()
