#!/usr/bin/env bash
#
# build.sh - Bootstrap a local virtualenv and build current project artifacts.
#
# Usage:
#   ./build.sh [output-dir]

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
OUTPUT_DIR="${1:-build}"
QUARTET_CONFIG="${ROOT_DIR}/configs/algorithmic-piano-quartet.toml"
QUARTET_NO2_CONFIG="${ROOT_DIR}/configs/algorithmic-piano-quartet-no2.toml"
HAS_FLUIDSYNTH=0
HAS_FFMPEG=0
HAS_ALGORITHMIC=0
PYTHON_BIN=""

require_command() {
    local command_name="$1"
    local error_message="$2"
    if ! command -v "${command_name}" >/dev/null 2>&1; then
        echo "Error: ${error_message}" >&2
        return 1
    fi
}

detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    else
        echo "Error: Python 3 is required but was not found in PATH." >&2
        exit 1
    fi
}

ensure_venv() {
    if [ ! -d "${VENV_DIR}" ]; then
        echo "Creating virtual environment at ${VENV_DIR}"
        "${PYTHON_BIN}" -m venv "${VENV_DIR}"
    fi
}

activate_venv() {
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
}

ensure_build_backend() {
    if python -c "import setuptools" >/dev/null 2>&1; then
        return
    fi

    echo "Installing setuptools build backend into ${VENV_DIR}"
    python -m pip install "setuptools>=68.0" wheel
}

install_project() {
    echo "Installing project in editable mode"
    python -m pip install --no-build-isolation -e "${ROOT_DIR}"
}

check_required_tools() {
    require_command "lilypond" "lilypond is required to build scores." || {
        echo "  macOS:  brew install lilypond" >&2
        echo "  Ubuntu: sudo apt install lilypond" >&2
        exit 1
    }
}

detect_optional_tools() {
    if command -v fluidsynth >/dev/null 2>&1; then
        HAS_FLUIDSYNTH=1
    fi

    if command -v ffmpeg >/dev/null 2>&1; then
        HAS_FFMPEG=1
    fi

    if [ -f "${ROOT_DIR}/src/algorithmic/__main__.py" ]; then
        HAS_ALGORITHMIC=1
    fi
}

prepare_output_dir() {
    mkdir -p "${OUTPUT_DIR}"
}

build_modus_operandi() {
    echo "Building Modus Operandi outputs into ${OUTPUT_DIR}"
    python -m modus_operandi_abjad -o "${OUTPUT_DIR}"
}

build_jazz_rhythms() {
    echo "Building Jazz Rhythms outputs into ${OUTPUT_DIR}"
    python -m jazz_rhythm -o "${OUTPUT_DIR}" --pdf --wav
}

build_piano_quartet() {
    if [ -f "${QUARTET_CONFIG}" ]; then
        echo "Building Piano Quartet Study outputs into ${OUTPUT_DIR}"
        if [ "${HAS_FLUIDSYNTH}" -eq 1 ] && [ "${HAS_FFMPEG}" -eq 1 ]; then
            python -m algorithmic_piano_quartet -c "${QUARTET_CONFIG}" -o "${OUTPUT_DIR}" --pdf --wav
        else
            python -m algorithmic_piano_quartet -c "${QUARTET_CONFIG}" -o "${OUTPUT_DIR}"
            if [ "${HAS_FLUIDSYNTH}" -eq 0 ]; then
                echo "Warning: fluidsynth is not installed; skipping Piano Quartet WAV render." >&2
            fi
            if [ "${HAS_FFMPEG}" -eq 0 ]; then
                echo "Warning: ffmpeg is not installed; skipping Piano Quartet WAV render." >&2
                echo "  macOS:  brew install ffmpeg" >&2
                echo "  Ubuntu: sudo apt install ffmpeg" >&2
            fi
        fi
    else
        echo "Warning: ${QUARTET_CONFIG} not found; skipping Piano Quartet Study." >&2
    fi
}

build_piano_quartet_no2() {
    if [ -f "${QUARTET_NO2_CONFIG}" ]; then
        echo "Building Algorithmic Piano Quartet No. 2 outputs into ${OUTPUT_DIR}"
        if [ "${HAS_FLUIDSYNTH}" -eq 1 ] && [ "${HAS_FFMPEG}" -eq 1 ]; then
            python -m algorithmic_piano_quartet_no2 -c "${QUARTET_NO2_CONFIG}" -o "${OUTPUT_DIR}" --pdf --wav
        else
            python -m algorithmic_piano_quartet_no2 -c "${QUARTET_NO2_CONFIG}" -o "${OUTPUT_DIR}"
            if [ "${HAS_FLUIDSYNTH}" -eq 0 ]; then
                echo "Warning: fluidsynth is not installed; skipping Piano Quartet No. 2 WAV render." >&2
            fi
            if [ "${HAS_FFMPEG}" -eq 0 ]; then
                echo "Warning: ffmpeg is not installed; skipping Piano Quartet No. 2 WAV render." >&2
                echo "  macOS:  brew install ffmpeg" >&2
                echo "  Ubuntu: sudo apt install ffmpeg" >&2
            fi
        fi
    else
        echo "Warning: ${QUARTET_NO2_CONFIG} not found; skipping Algorithmic Piano Quartet No. 2." >&2
    fi
}

build_algorithmic() {
    if [ "${HAS_ALGORITHMIC}" -eq 1 ]; then
        echo "Building Algorithmic scaffold into ${OUTPUT_DIR}"
        python -m algorithmic -o "${OUTPUT_DIR}"
    fi
}

render_modus_operandi_wav() {
    if [ "${HAS_FLUIDSYNTH}" -eq 1 ]; then
        echo "Rendering Modus Operandi WAV into ${OUTPUT_DIR}"
        "${ROOT_DIR}/midi2wav.sh" \
            "${OUTPUT_DIR}/modus-operandi-abjad.midi" \
            "${OUTPUT_DIR}/modus-operandi-abjad.wav"
    else
        echo "Warning: fluidsynth is not installed; skipping WAV render." >&2
        echo "  macOS:  brew install fluidsynth" >&2
        echo "  Ubuntu: sudo apt install fluidsynth" >&2
    fi
}

main() {
    detect_python
    ensure_venv
    activate_venv
    ensure_build_backend
    install_project
    check_required_tools
    detect_optional_tools
    prepare_output_dir
    build_modus_operandi
    build_jazz_rhythms
    build_piano_quartet
    build_piano_quartet_no2
    build_algorithmic
    render_modus_operandi_wav
    echo "Build complete. Artifacts are in ${OUTPUT_DIR}"
}

main "$@"
