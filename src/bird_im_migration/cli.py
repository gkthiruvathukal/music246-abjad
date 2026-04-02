"""Command-line interface for generating Bird Im-Migration."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

import abjad

from .analysis import DEFAULT_PARTIALS_PATH
from .score import build_lilypond_file

STEM_BASE = "bird-im-migration"


def default_stem(quantization: int) -> str:
    return f"{STEM_BASE}-q{quantization}"


def write_ly(lilypond_file, output_dir: str, stem: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{stem}.ly")
    with open(ly_path, "w") as file_pointer:
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


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Bird Im-Migration from the SPEAR partials analysis.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="build",
        help="directory for generated files (default: build)",
    )
    parser.add_argument(
        "--partials",
        default=str(DEFAULT_PARTIALS_PATH),
        help="path to the SPEAR partials file",
    )
    parser.add_argument(
        "--quantization",
        choices=(16, 32),
        type=int,
        default=32,
        help="rhythmic denominator used for region quantization (default: 32)",
    )
    parser.add_argument(
        "--tempo",
        type=int,
        default=90,
        help="tempo in quarter-notes per minute (default: 90)",
    )
    parser.add_argument(
        "--midi-instrument",
        default="acoustic grand",
        help='LilyPond MIDI instrument name (default: "acoustic grand")',
    )
    parser.add_argument(
        "--stem",
        default=None,
        help="override output stem (default: bird-im-migration-q16 or q32)",
    )

    group = parser.add_argument_group("output formats")
    group.add_argument("--ly", action="store_true", default=False, help="generate .ly file only")
    group.add_argument("--pdf", action="store_true", default=False, help="compile and produce PDF")
    group.add_argument("--midi", action="store_true", default=False, help="compile and produce MIDI")

    args = parser.parse_args(argv)
    if not (args.ly or args.pdf or args.midi):
        args.ly = True
        args.pdf = True
        args.midi = True
    return args


def main(argv=None):
    args = parse_args(argv)
    stem = args.stem or default_stem(args.quantization)
    lilypond_file = build_lilypond_file(
        partials_path=Path(args.partials),
        quantization=args.quantization,
        tempo_bpm=args.tempo,
        midi_instrument=args.midi_instrument,
    )
    ly_path = write_ly(lilypond_file, args.output_dir, stem)

    formats_to_compile: set[str] = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    if args.midi:
        formats_to_compile.add("midi")

    if formats_to_compile:
        compile_lilypond(ly_path, args.output_dir, stem, formats_to_compile)

    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")


if __name__ == "__main__":
    main()
