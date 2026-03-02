"""Command-line interface for generating Modus Operandi for Piano."""

import argparse
import glob
import os
import subprocess
import sys

import abjad
import mido

from .score import build_lilypond_file

STEM = "modus-operandi-abjad"


def write_ly(lilypond_file, output_dir):
    """Write the .ly file and return its path."""
    os.makedirs(output_dir, exist_ok=True)
    ly_path = os.path.join(output_dir, f"{STEM}.ly")
    with open(ly_path, "w") as f:
        f.write(abjad.lilypond(lilypond_file))
    print(f"Wrote {ly_path}")
    return ly_path


def _seconds_to_ticks(seconds, tempo, ticks_per_beat):
    """Convert a duration in seconds to MIDI ticks.

    *tempo* is microseconds per beat (as stored in ``set_tempo`` messages).
    """
    beats = seconds / (tempo / 1_000_000)
    return int(round(beats * ticks_per_beat))


def _last_tempo(track):
    """Return the last ``set_tempo`` value in *track* (default 500000)."""
    tempo = 500_000  # MIDI default: 120 BPM
    for msg in track:
        if msg.type == "set_tempo":
            tempo = msg.tempo
    return tempo


def concatenate_midi(output_dir, gap_seconds=1.0):
    """Join per-movement MIDI files into a single combined file.

    LilyPond emits one MIDI file per ``\\score`` block:
    ``STEM.midi``, ``STEM-1.midi``, ``STEM-2.midi``, etc.
    This function concatenates them track-by-track (conductor, RH, LH)
    into ``STEM.midi``, then removes the per-movement files.

    *gap_seconds* controls how much silence is inserted between
    movements (default 1.0 s).  Use 0 for no gap.
    """
    base = os.path.join(output_dir, f"{STEM}.midi")
    # Collect per-movement files in order.
    # LilyPond names them: STEM.midi, STEM-1.midi, STEM-2.midi, ...
    parts = sorted(glob.glob(os.path.join(output_dir, f"{STEM}*.midi")))
    if len(parts) <= 1:
        return  # nothing to join

    midis = [mido.MidiFile(p) for p in parts]

    # All files should share the same ticks_per_beat and track count.
    tpb = midis[0].ticks_per_beat
    n_tracks = len(midis[0].tracks)

    # Pre-compute the gap in ticks for each movement boundary using
    # the tempo at the end of that movement's conductor track (track 0).
    gap_ticks = []
    for midi in midis[:-1]:  # no gap after the last movement
        tempo = _last_tempo(midi.tracks[0])
        gap_ticks.append(_seconds_to_ticks(gap_seconds, tempo, tpb))

    combined = mido.MidiFile(type=1, ticks_per_beat=tpb)

    for track_idx in range(n_tracks):
        merged = mido.MidiTrack()
        for file_idx, midi in enumerate(midis):
            track = midi.tracks[track_idx]
            for msg in track:
                if msg.type == "end_of_track":
                    # Replace end_of_track with silence gap between
                    # movements.  Any existing end_of_track padding is
                    # preserved as dead time, plus our explicit gap.
                    gap = msg.time
                    if file_idx < len(gap_ticks):
                        gap += gap_ticks[file_idx]
                    if gap > 0:
                        merged.append(mido.MetaMessage("text", text="", time=gap))
                else:
                    merged.append(msg.copy())
        # Final end_of_track
        merged.append(mido.MetaMessage("end_of_track", time=0))
        combined.tracks.append(merged)

    combined.save(base)
    gap_msg = f" with {gap_seconds}s gap" if gap_seconds > 0 else ""
    print(f"Combined {len(parts)} MIDI files into {base}{gap_msg}")

    # Remove the per-movement files (but not the combined one we just wrote).
    for p in parts:
        if p != base:
            os.remove(p)
            print(f"Removed {p}")


def compile_lilypond(ly_path, output_dir, fmt, gap_seconds=1.0):
    """Run lilypond to produce PDF and/or MIDI from a .ly file.

    *fmt* is a set that may contain ``"pdf"`` and/or ``"midi"``.
    LilyPond always produces both when a \\midi block is present, so we
    just run it once and remove unwanted artefacts afterwards.

    *gap_seconds* is passed to :func:`concatenate_midi` when MIDI is
    requested.
    """
    stem = os.path.join(output_dir, STEM)
    cmd = ["lilypond", "-o", stem, ly_path]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    # LilyPond emits status on stderr
    if result.stderr:
        print(result.stderr, end="")

    # Remove artefacts the user did not ask for.
    if "pdf" not in fmt:
        pdf = f"{stem}.pdf"
        if os.path.exists(pdf):
            os.remove(pdf)
            print(f"Removed {pdf} (not requested)")

    if "midi" not in fmt:
        # LilyPond may produce multiple MIDI files for multi-score docs.
        for entry in os.listdir(output_dir):
            if entry.startswith(STEM) and entry.endswith(".midi"):
                path = os.path.join(output_dir, entry)
                os.remove(path)
                print(f"Removed {path} (not requested)")
    else:
        # Combine per-movement MIDI files into one.
        concatenate_midi(output_dir, gap_seconds=gap_seconds)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate Modus Operandi for Piano from Abjad.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="build",
        help="directory for generated files (default: build)",
    )
    parser.add_argument(
        "--gap",
        type=float,
        default=1.0,
        metavar="SECONDS",
        help="silence between movements in combined MIDI (default: 1.0)",
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

    # If no format flags are given, produce everything.
    if not (args.ly or args.pdf or args.midi):
        args.ly = True
        args.pdf = True
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
        compile_lilypond(
            ly_path, args.output_dir, formats_to_compile, gap_seconds=args.gap
        )

    # If only --ly was requested (no --pdf/--midi), we're done.
    if not formats_to_compile and args.ly:
        print("Done (--ly only, skipping LilyPond compilation).")
