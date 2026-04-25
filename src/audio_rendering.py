"""Shared helpers for rendering and normalizing WAV output."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def run_audio_command(cmd: list[str], *, wrote_path: str | None = None) -> None:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stderr:
        print(result.stderr, end="")
    if wrote_path is not None:
        print(f"Wrote {wrote_path}")


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
    run_audio_command(cmd, wrote_path=output_path)


def copy_or_normalize_single_wav(
    input_path: str,
    output_path: str,
    sample_rate: int,
) -> None:
    if input_path == output_path:
        normalize_wav(input_path, output_path, sample_rate)
        return

    Path(output_path).write_bytes(Path(input_path).read_bytes())
    print(f"Wrote {output_path}")
