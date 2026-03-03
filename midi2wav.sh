#!/usr/bin/env bash
#
# midi2wav.sh — Render a MIDI file to WAV using FluidSynth and the
#               Salamander Grand Piano soundfont.
#
# Usage:
#   ./midi2wav.sh <input.midi> [output.wav]
#
# The soundfont (~296 MB) is downloaded on first use and cached in
# ~/.soundfonts/.  Requires: fluidsynth, curl, tar, xz.

set -euo pipefail

# --- Configuration -----------------------------------------------------------

SOUNDFONT_URL="https://freepats.zenvoid.org/Piano/SalamanderGrandPiano/SalamanderGrandPiano-SF2-V3+20200602.tar.xz"
SOUNDFONT_DIR="${HOME}/.soundfonts"
SOUNDFONT_SF2="${SOUNDFONT_DIR}/SalamanderGrandPiano-V3+20200602.sf2"

# --- Argument handling -------------------------------------------------------

if [ $# -lt 1 ]; then
    echo "Usage: $0 <input.midi> [output.wav]" >&2
    exit 1
fi

MIDI_FILE="$1"
WAV_FILE="${2:-${MIDI_FILE%.midi}.wav}"

if [ ! -f "$MIDI_FILE" ]; then
    echo "Error: MIDI file not found: $MIDI_FILE" >&2
    exit 1
fi

# --- Check for fluidsynth ----------------------------------------------------

if ! command -v fluidsynth &>/dev/null; then
    echo "Error: fluidsynth is not installed." >&2
    echo "  macOS:  brew install fluidsynth" >&2
    echo "  Ubuntu: sudo apt install fluidsynth" >&2
    exit 1
fi

# --- Fetch soundfont if needed -----------------------------------------------

if [ ! -f "$SOUNDFONT_SF2" ]; then
    echo "Downloading Salamander Grand Piano soundfont (~296 MB)..."
    mkdir -p "$SOUNDFONT_DIR"
    ARCHIVE="${SOUNDFONT_DIR}/salamander.tar.xz"
    curl -L -o "$ARCHIVE" "$SOUNDFONT_URL"
    echo "Extracting..."
    tar -xf "$ARCHIVE" -C "$SOUNDFONT_DIR" --strip-components=1
    # Remove everything except the .sf2 file
    find "$SOUNDFONT_DIR" -type f ! -name '*.sf2' -delete
    find "$SOUNDFONT_DIR" -type d -empty -delete
    rm -f "$ARCHIVE"
    if [ ! -f "$SOUNDFONT_SF2" ]; then
        echo "Error: expected $SOUNDFONT_SF2 after extraction" >&2
        exit 1
    fi
    echo "Soundfont cached: $SOUNDFONT_SF2"
else
    echo "Soundfont already cached: $SOUNDFONT_SF2"
fi

# --- Render ------------------------------------------------------------------

echo "Rendering: $MIDI_FILE -> $WAV_FILE"
fluidsynth -ni -F "$WAV_FILE" -r 44100 "$SOUNDFONT_SF2" "$MIDI_FILE"
echo "Done: $WAV_FILE"
