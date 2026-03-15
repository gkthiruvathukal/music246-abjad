"""CLI for building the atonal piano quartet prototype."""

from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys

import abjad

from .config import load_config
from .generator import compose_piece
from .score import build_lilypond_file


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a short atonal piano quartet study from TOML config.",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="piano-quartet.toml",
        help="path to TOML config (default: piano-quartet.toml)",
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
) -> None:
    soundfont = Path(soundfont_path).expanduser()
    if not soundfont.exists():
        raise FileNotFoundError(f"Soundfont not found: {soundfont}")
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
        soundfont = args.soundfont or config.render.soundfont
        if not soundfont:
            raise ValueError("WAV rendering requires --soundfont or [render].soundfont in config.")
        midi_path = os.path.join(args.output_dir, f"{stem}.midi")
        wav_path = os.path.join(args.output_dir, f"{stem}.wav")
        render_wav(
            midi_path=midi_path,
            wav_path=wav_path,
            soundfont_path=soundfont,
            sample_rate=config.render.sample_rate,
        )


if __name__ == "__main__":
    main()
