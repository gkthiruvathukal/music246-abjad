# Music Composition with Abjad

This repository contains programmatic music composition experiments and finished works using [Abjad](https://abjad.github.io/) and [LilyPond](https://lilypond.org/).

The repository uses normal Python entry points instead of relying on a `Makefile`. Each package exposes a module entry point (`python -m ...`) and, after installation, a console script.

## Projects

### 1. [Modus Operandi for Piano](README-ModusOperandi.md)

A monody for solo piano in three movements (F Dorian, F Phrygian, F Lydian). This is a complete composition with a CI/CD pipeline for generating PDF scores and MIDI/WAV audio.

- **Source:** `src/modus_operandi_abjad/`
- **CLI:** `python -m modus_operandi_abjad -o build`

### 2. [Jazz Rhythmic Patterns](README-JazzRhythms.md)

A collection of generated jazz comping rhythms (Charleston, anticipation, syncopated figures) rendered as rhythmic notation, LilyPond source, and MIDI.

- **Source:** `src/jazz_rhythm/`
- **CLI:** `python -m jazz_rhythm -o build`

### 3. [Piano Quartet Study](README-PianoQuartetStudy.md)

A generated **tonal** chamber study for piano, violin, viola, and cello. This is an exploratory step toward a future atonal composition system, but this study itself is tonal and should be described that way.

- **Source:** `src/algorithmic_piano_quartet/`
- **CLI:** `python -m algorithmic_piano_quartet -c configs/algorithmic-piano-quartet.toml -o build`

### 4. [Algorithmic](README-Algorithmic.md)

A placeholder scaffold for a future algorithmic composition package. It currently exists to keep the package, CLI, and score-generation path wired up while the musical material is still pending.

- **Source:** `src/algorithmic/`
- **CLI:** `python -m algorithmic -o build`

### 5. [Algorithmic Piano Quartet No. 2](README-AlgorithmicPianoQuartetNo2.md)

A separate exploratory branch of the quartet work. It starts from the current No. 1 implementation but is intended to develop independently so new musical ideas can be tested without changing the established No. 1 score.

- **Source:** `src/algorithmic_piano_quartet_no2/`
- **Config:** `configs/algorithmic-piano-quartet-no2.toml`
- **CLI:** `python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build`

## Setup

All projects require Python 3.10+ and LilyPond 2.24+.

1.  **Install dependencies:**

    ```bash
    pip install -e .
    ```

    This installs four console scripts:

    ```bash
    modus-operandi-abjad
    jazz-rhythms
    algorithmic-piano-quartet
    algorithmic-piano-quartet-no2
    algorithmic
    ```

2.  **Install LilyPond:**
    -   macOS: `brew install lilypond`
    -   Ubuntu: `sudo apt install lilypond`

3.  **Install FluidSynth (optional, for audio rendering):**
    -   macOS: `brew install fluidsynth`
    -   Ubuntu: `sudo apt install fluidsynth`

## Standard Python Workflows

For a full local build with automatic `.venv` creation, use:

```bash
./build.sh
```

This bootstraps `.venv`, installs the project in editable mode, builds the current score packages into `build/`, renders the Modus Operandi WAV if `fluidsynth` is installed, and renders the piano quartet WAV when FluidSynth is available. The quartet render path automatically caches Salamander for piano, Aegean for strings, and mixes the layers with `ffmpeg`.

You can override the output directory:

```bash
./build.sh out
```

If you prefer running the project entry points directly, use:

Run the CLIs directly as modules:

```bash
python -m modus_operandi_abjad -o build
python -m jazz_rhythm -o build
python -m algorithmic_piano_quartet -c configs/algorithmic-piano-quartet.toml -o build
python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build
python -m algorithmic -o build
```

Or use the installed console scripts:

```bash
modus-operandi-abjad -o build
jazz-rhythms -o build
algorithmic-piano-quartet -c configs/algorithmic-piano-quartet.toml -o build
algorithmic-piano-quartet-no2 -c configs/algorithmic-piano-quartet-no2.toml -o build
algorithmic -o build
```

If you want a wheel or source distribution, use the standard Python build tool:

```bash
python -m build
```

## CI/CD

GitHub Actions uses a single workflow file, [build.yml](.github/workflows/build.yml), to build the repository artifacts.

- `modus_operandi_abjad` produces `.ly`, `.pdf`, `.midi`, and `.wav`
- `jazz_rhythm` produces `.ly`, `.pdf`, and `.midi`
- `algorithmic_piano_quartet` produces uniquely named `.ly`, `.pdf`, `.midi`, and `.wav` when FluidSynth is available
- `algorithmic_piano_quartet_no2` produces uniquely named `.ly`, `.pdf`, `.midi`, and `.wav` when FluidSynth is available
- `algorithmic` currently produces placeholder `.ly`, `.pdf`, and `.midi`
- pushing a version tag creates one GitHub release containing assets from the built projects
