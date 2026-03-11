"""Command-line interface for generating Jazz Rhythm Patterns."""

import argparse
import os
import subprocess
import sys

import abjad

try:
    from .score import build_lilypond_file
except ImportError as e:
    print(f"Error importing build_lilypond_file: {e}", file=sys.stderr)
    import traceback

    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

STEM = "jazz-rhythms"


def write_ly(lilypond_file, output_dir) -> str:
    """Write the .ly file and return its path."""
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{STEM}.ly")
    with open(ly_path, "w") as f:
        f.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def compile_lilypond(ly_path, output_dir, fmt) -> None:
    """Run lilypond to produce PDF from a .ly file.

    *fmt* is a set that may contain ``"pdf"``.
    LilyPond always produces both when a \\midi block is present, but for rhythm charts,
    we only care about the PDF.
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

    # Remove artefacts the user did not ask for.
    if "pdf" not in fmt:
        pdf = f"{stem}.pdf"
        if os.path.exists(pdf):
            os.remove(pdf)
            print(f"Removed {pdf} (not requested)")

    # Always remove MIDI files as they are not requested for jazz rhythms.
    for entry in os.listdir(output_dir):
        if entry.startswith(STEM) and entry.endswith(".midi"):
            path = os.path.join(output_dir, entry)
            os.remove(path)
            print(f"Removed {path} (not requested for jazz rhythms)")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Jazz Rhythm Patterns from Abjad.",
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

    args = parser.parse_args(argv)

    # If no format flags are given, produce both .ly and .pdf.
    if not (args.ly or args.pdf):
        args.ly = True
        args.pdf = True

    return args


def main(argv=None):
    print("DEBUG: Entering main function")
    args = parse_args(argv)
    print(f"DEBUG: Parsed arguments: {args}")
    try:
        print("DEBUG: Calling build_lilypond_file()")
        lilypond_file = build_lilypond_file()
        print("DEBUG: Returned from build_lilypond_file()")
    except Exception as e:
        print(f"Error building LilyPond file: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    print("DEBUG: Calling write_ly()")
    ly_path = write_ly(lilypond_file, args.output_dir)
    print(f"DEBUG: Returned from write_ly(), ly_path: {ly_path}")

    formats_to_compile = set()
    if args.pdf:
        formats_to_compile.add("pdf")
    print(f"DEBUG: formats_to_compile: {formats_to_compile}")

    if formats_to_compile:
        print("DEBUG: Calling compile_lilypond()")
        compile_lilypond(ly_path, args.output_dir, formats_to_compile)
        print("DEBUG: Returned from compile_lilypond()")

    # If only --ly was requested (no --pdf), we're done.
    if not formats_to_compile and args.ly:
        print("DEBUG: Done (--ly only, skipping LilyPond compilation).")
    print("DEBUG: Exiting main function")


print("DEBUG: End of cli.py module")

if __name__ == "__main__":
    main()
