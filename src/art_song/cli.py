"""Command-line interface for generating the Art Song scaffold."""

import argparse
import os
import subprocess
import sys

import abjad

from .score import (
    build_part_lilypond_file,
    build_chord_voicing_cheat_sheet,
    build_lilypond_file,
)

STEM = "art-song"
PARTS = ["voice", "violin", "viola", "trumpet-c", "trumpet-bb", "piano"]


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

    args = parser.parse_args(argv)

    if not (args.ly or args.pdf or args.midi):
        args.ly = True
        args.pdf = True
        args.midi = True

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

    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")


if __name__ == "__main__":
    main()
