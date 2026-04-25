"""Command-line interface for generating jazz rhythm studies."""

import argparse
import os
import subprocess
import sys

import abjad

from .render import render_clap_wav
from .score import build_lilypond_file

STEM = "jazz-rhythms"


def write_ly(lilypond_file, output_dir) -> str:
    """Write the .ly file and return its path."""
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{STEM}.ly")
    with open(ly_path, "w") as file_pointer:
        file_pointer.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def compile_lilypond(ly_path, output_dir, fmt) -> None:
    """Run lilypond to produce PDF and/or MIDI from a .ly file.

    *fmt* is a set that may contain ``"pdf"`` and/or ``"midi"``.
    LilyPond always produces both when a \\midi block is present, so we
    run it once and remove unrequested artifacts afterwards.
    """
    stem = os.path.join(output_dir, STEM)
    cmd = ["lilypond", "-o", stem, ly_path]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    if result.stderr:
        print(result.stderr, end="")

    if "pdf" not in fmt:
        pdf = f"{stem}.pdf"
        if os.path.exists(pdf):
            os.remove(pdf)
            print(f"Removed {pdf} (not requested)")

    if "midi" not in fmt:
        for entry in os.listdir(output_dir):
            if entry.startswith(STEM) and entry.endswith(".midi"):
                path = os.path.join(output_dir, entry)
                os.remove(path)
                print(f"Removed {path} (not requested)")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate jazz rhythmic pattern studies from Abjad.",
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
        help="render a clap-based WAV file from the generated MIDI",
    )

    args = parser.parse_args(argv)

    if not (args.ly or args.pdf or args.midi or args.wav):
        args.ly = True
        args.pdf = True
        args.midi = True
    if args.wav:
        args.midi = True

    return args


def main(argv=None):
    args = parse_args(argv)
    lilypond_file = build_lilypond_file()
    ly_path = write_ly(lilypond_file, args.output_dir)

    formats_to_compile = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    if args.midi:
        formats_to_compile.add("midi")

    if formats_to_compile:
        compile_lilypond(ly_path, args.output_dir, formats_to_compile)
        if args.wav:
            midi_path = os.path.join(args.output_dir, f"{STEM}.midi")
            wav_path = os.path.join(args.output_dir, f"{STEM}.wav")
            render_clap_wav(midi_path, wav_path)

    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")

if __name__ == "__main__":
    main()
