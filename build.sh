#!/usr/bin/env bash
#
# build.sh - Bootstrap a local virtualenv and build all project artifacts.
#
# Usage:
#   ./build.sh [output-dir]

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
OUTPUT_DIR="${1:-build}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Error: Python 3 is required but was not found in PATH." >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at ${VENV_DIR}"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "Installing project dependencies into ${VENV_DIR}"
python -m pip install "abjad>=3.19" "mido>=1.3" "tomli>=2.0"

if ! command -v lilypond >/dev/null 2>&1; then
    echo "Error: lilypond is required to build scores." >&2
    echo "  macOS:  brew install lilypond" >&2
    echo "  Ubuntu: sudo apt install lilypond" >&2
    exit 1
fi

echo "Building Modus Operandi outputs into ${OUTPUT_DIR}"
PYTHONPATH="${ROOT_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}" \
    python -m modus_operandi_abjad -o "$OUTPUT_DIR"

echo "Building Jazz Rhythms outputs into ${OUTPUT_DIR}"
PYTHONPATH="${ROOT_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}" \
    python -m jazz_rhythm -o "$OUTPUT_DIR"

if command -v fluidsynth >/dev/null 2>&1; then
    echo "Rendering Modus Operandi WAV into ${OUTPUT_DIR}"
    "${ROOT_DIR}/midi2wav.sh" \
        "${OUTPUT_DIR}/modus-operandi-abjad.midi" \
        "${OUTPUT_DIR}/modus-operandi-abjad.wav"
else
    echo "Warning: fluidsynth is not installed; skipping WAV render." >&2
    echo "  macOS:  brew install fluidsynth" >&2
    echo "  Ubuntu: sudo apt install fluidsynth" >&2
fi

echo "Build complete. Artifacts are in ${OUTPUT_DIR}"
