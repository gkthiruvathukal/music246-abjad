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
QUARTET_NO1_CONFIG="${ROOT_DIR}/configs/algorithmic-piano-quartet-no1.toml"
QUARTET_NO2_CONFIG="${ROOT_DIR}/configs/algorithmic-piano-quartet-no2.toml"
HAS_FLUIDSYNTH=0
HAS_FFMPEG=0
HAS_ALGORITHMIC=0
HAS_BIRD_IM_MIGRATION=0
HAS_THUMBNAIL_TOOLS=0
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

    if [ -f "${ROOT_DIR}/src/bird_im_migration/__main__.py" ]; then
        HAS_BIRD_IM_MIGRATION=1
    fi

    if command -v pdftoppm >/dev/null 2>&1 && command -v convert >/dev/null 2>&1; then
        HAS_THUMBNAIL_TOOLS=1
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
    if [ -f "${QUARTET_NO1_CONFIG}" ]; then
        echo "Building Algo Rhythms Quartet No. 1 outputs into ${OUTPUT_DIR}"
        if [ "${HAS_FLUIDSYNTH}" -eq 1 ] && [ "${HAS_FFMPEG}" -eq 1 ]; then
            python -m algorithmic_piano_quartet_no1 -c "${QUARTET_NO1_CONFIG}" -o "${OUTPUT_DIR}" --pdf --wav
        else
            python -m algorithmic_piano_quartet_no1 -c "${QUARTET_NO1_CONFIG}" -o "${OUTPUT_DIR}"
            if [ "${HAS_FLUIDSYNTH}" -eq 0 ]; then
                echo "Warning: fluidsynth is not installed; skipping Algo Rhythms Quartet No. 1 WAV render." >&2
            fi
            if [ "${HAS_FFMPEG}" -eq 0 ]; then
                echo "Warning: ffmpeg is not installed; skipping Algo Rhythms Quartet No. 1 WAV render." >&2
                echo "  macOS:  brew install ffmpeg" >&2
                echo "  Ubuntu: sudo apt install ffmpeg" >&2
            fi
        fi
    else
        echo "Warning: ${QUARTET_NO1_CONFIG} not found; skipping Algo Rhythms Quartet No. 1." >&2
    fi
}

build_piano_quartet_no2() {
    if [ -f "${QUARTET_NO2_CONFIG}" ]; then
        echo "Building Algo Rhythms Quartet No. 2 outputs into ${OUTPUT_DIR}"
        if [ "${HAS_FLUIDSYNTH}" -eq 1 ] && [ "${HAS_FFMPEG}" -eq 1 ]; then
            python -m algorithmic_piano_quartet_no2 -c "${QUARTET_NO2_CONFIG}" -o "${OUTPUT_DIR}" --pdf --wav
        else
            python -m algorithmic_piano_quartet_no2 -c "${QUARTET_NO2_CONFIG}" -o "${OUTPUT_DIR}"
            if [ "${HAS_FLUIDSYNTH}" -eq 0 ]; then
                echo "Warning: fluidsynth is not installed; skipping Algo Rhythms Quartet No. 2 WAV render." >&2
            fi
            if [ "${HAS_FFMPEG}" -eq 0 ]; then
                echo "Warning: ffmpeg is not installed; skipping Algo Rhythms Quartet No. 2 WAV render." >&2
                echo "  macOS:  brew install ffmpeg" >&2
                echo "  Ubuntu: sudo apt install ffmpeg" >&2
            fi
        fi
    else
        echo "Warning: ${QUARTET_NO2_CONFIG} not found; skipping Algo Rhythms Quartet No. 2." >&2
    fi
}

build_algorithmic() {
    if [ "${HAS_ALGORITHMIC}" -eq 1 ]; then
        echo "Building Algorithmic scaffold into ${OUTPUT_DIR}"
        python -m algorithmic -o "${OUTPUT_DIR}"
    fi
}

build_bird_im_migration() {
    if [ "${HAS_BIRD_IM_MIGRATION}" -eq 1 ]; then
        echo "Building Bird Im-Migration outputs into ${OUTPUT_DIR}"
        python -m bird_im_migration -o "${OUTPUT_DIR}" --quantization 16 --pdf --midi
        python -m bird_im_migration -o "${OUTPUT_DIR}" --quantization 32 --pdf --midi
    fi
}

render_bird_im_migration_wavs() {
    if [ "${HAS_BIRD_IM_MIGRATION}" -ne 1 ]; then
        return
    fi

    if [ "${HAS_FLUIDSYNTH}" -eq 1 ]; then
        echo "Rendering Bird Im-Migration WAV outputs into ${OUTPUT_DIR}"
        if [ -f "${OUTPUT_DIR}/bird-im-migration-q16.midi" ]; then
            "${ROOT_DIR}/midi2wav.sh" \
                "${OUTPUT_DIR}/bird-im-migration-q16.midi" \
                "${OUTPUT_DIR}/bird-im-migration-q16.wav"
        fi
        if [ -f "${OUTPUT_DIR}/bird-im-migration-q32.midi" ]; then
            "${ROOT_DIR}/midi2wav.sh" \
                "${OUTPUT_DIR}/bird-im-migration-q32.midi" \
                "${OUTPUT_DIR}/bird-im-migration-q32.wav"
        fi
    else
        echo "Warning: fluidsynth is not installed; skipping Bird Im-Migration WAV render." >&2
        echo "  macOS:  brew install fluidsynth" >&2
        echo "  Ubuntu: sudo apt install fluidsynth" >&2
    fi
}

create_thumbnail() {
    local pdf_path="$1"
    local png_path="$2"
    local base_path="${png_path%.png}"
    local temp_path="${base_path}-page1"

    pdftoppm -png -f 1 -singlefile "${pdf_path}" "${temp_path}"
    convert "${temp_path}.png" -resize 50% "${png_path}"
    rm -f "${temp_path}.png"
    echo "Wrote ${png_path}"
}

render_bird_im_migration_thumbnails() {
    if [ "${HAS_BIRD_IM_MIGRATION}" -ne 1 ]; then
        return
    fi

    if [ "${HAS_THUMBNAIL_TOOLS}" -eq 1 ]; then
        echo "Rendering Bird Im-Migration PNG previews into ${OUTPUT_DIR}"
        if [ -f "${OUTPUT_DIR}/bird-im-migration-q16.pdf" ]; then
            create_thumbnail \
                "${OUTPUT_DIR}/bird-im-migration-q16.pdf" \
                "${OUTPUT_DIR}/bird-im-migration-q16-thumbnail.png"
        fi
        if [ -f "${OUTPUT_DIR}/bird-im-migration-q32.pdf" ]; then
            create_thumbnail \
                "${OUTPUT_DIR}/bird-im-migration-q32.pdf" \
                "${OUTPUT_DIR}/bird-im-migration-q32-thumbnail.png"
        fi
    else
        echo "Warning: pdftoppm and/or convert are not installed; skipping Bird Im-Migration thumbnail render." >&2
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
    build_bird_im_migration
    render_modus_operandi_wav
    render_bird_im_migration_wavs
    render_bird_im_migration_thumbnails
    echo "Build complete. Artifacts are in ${OUTPUT_DIR}"
}

main "$@"
