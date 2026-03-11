# Music Composition with Abjad

This repository contains programmatic music composition experiments and finished works using [Abjad](https://abjad.github.io/) and [LilyPond](https://lilypond.org/).

The repository uses normal Python entry points instead of relying on a `Makefile`. Both projects expose module entry points (`python -m ...`) and console scripts after installation.

## Projects

### 1. [Modus Operandi for Piano](README-ModusOperandi.md)

A monody for solo piano in three movements (F Dorian, F Phrygian, F Lydian). This is a complete composition with a CI/CD pipeline for generating PDF scores and MIDI/WAV audio.

- **Source:** `src/modus_operandi_abjad/`
- **CLI:** `python -m modus_operandi_abjad -o build`

### 2. [Jazz Rhythmic Patterns](README-JazzRhythms.md)

A collection of generated jazz comping rhythms (Charleston, anticipation, syncopated figures) rendered as rhythmic notation, LilyPond source, and MIDI.

- **Source:** `src/jazz_rhythm/`
- **CLI:** `python -m jazz_rhythm -o build`

## Setup

Both projects require Python 3.10+ and LilyPond 2.24+.

1.  **Install dependencies:**

    ```bash
    pip install -e .
    ```

    This installs two console scripts:

    ```bash
    modus-operandi-abjad
    jazz-rhythms
    ```

2.  **Install LilyPond:**
    -   macOS: `brew install lilypond`
    -   Ubuntu: `sudo apt install lilypond`

3.  **Install FluidSynth (optional, for audio rendering):**
    -   macOS: `brew install fluidsynth`
    -   Ubuntu: `sudo apt install fluidsynth`

## Standard Python Workflows

Run the CLIs directly as modules:

```bash
python -m modus_operandi_abjad -o build
python -m jazz_rhythm -o build
```

Or use the installed console scripts:

```bash
modus-operandi-abjad -o build
jazz-rhythms -o build
```

If you want a wheel or source distribution, use the standard Python build tool:

```bash
python -m build
```

## CI/CD

GitHub Actions uses a single workflow file, [build.yml](.github/workflows/build.yml), to build both projects.

- `modus_operandi_abjad` produces `.ly`, `.pdf`, `.midi`, and `.wav`
- `jazz_rhythm` produces `.ly`, `.pdf`, and `.midi`
- pushing a version tag creates one GitHub release containing assets from both projects
