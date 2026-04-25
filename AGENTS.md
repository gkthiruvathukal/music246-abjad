# AGENTS.md

This file provides repository-specific guidance for coding agents working in this repository.

## Project Overview

Programmatic music composition system using [Abjad](https://abjad.github.io/) and [LilyPond](https://lilypond.org/). Each composition is a Python package under `src/` that generates `.ly` files, compiles them to PDF/MIDI, and optionally renders WAV via FluidSynth.

## Common Commands

Build all compositions and documentation:

```bash
./build.sh [output-dir]   # defaults to build/
./build-docs.sh           # Sphinx HTML + PDF to docs/_build/
```

Run a single composition:

```bash
python -m modus_operandi_abjad -o build
python -m jazz_rhythm -o build --pdf --wav
python -m bird_im_migration -o build --quantization 16 --pdf --midi
python -m algorithmic_piano_quartet_no1 -c configs/algorithmic-piano-quartet-no1.toml -o build --pdf --wav
python -m art_song -o build --pdf --midi
```

Render MIDI to WAV manually:

```bash
./midi2wav.sh <file.midi> <soundfont.sf2> <output.wav>
```

System requirements:

- Python 3.10+
- LilyPond 2.24+
- FluidSynth and `ffmpeg` for WAV output
- `pdfcrop`, `pdftoppm`, and ImageMagick (`magick` or `convert`) for thumbnails

## Architecture

### Package Layout

Each composition follows the same internal structure:

```text
src/<composition>/
  __main__.py    # entry point
  cli.py         # argparse, orchestrates full pipeline
  score.py       # Abjad score construction
  generator.py   # algorithmic generation (quartet/rhythm pieces only)
  config.py      # TOML config parsing (quartet pieces only)
```

### Shared Pipeline

1. Parse CLI args and optional TOML config.
2. Construct or generate an Abjad `Score` object in `score.py`.
3. Write `.ly` source.
4. Shell out to `lilypond` to produce PDF and/or MIDI.
5. Post-process as needed:
   - concatenate multi-movement MIDIs for Modus Operandi
   - render WAV with FluidSynth and `ffmpeg`
   - mix separate piano/strings renders for quartet pieces

### TOML Configuration

Configs live in `configs/`. They define:

- per-part pitch classes, instrument ranges, and MIDI channels
- generation parameters such as measures, tempo, and random seed
- output naming options
- separate piano and string soundfonts for layered audio rendering

### Composition Packages

| Package | Description |
| --- | --- |
| `modus_operandi_abjad` | Three-movement piano work |
| `jazz_rhythm` | Generated rhythm studies |
| `algorithmic_piano_quartet_no1` | Quartet with TOML-driven generation |
| `algorithmic_piano_quartet_no2` | Exploratory quartet variant |
| `bird_im_migration` | Birdsong-inspired reduction with audio data assets |
| `bird_im_migration_ensemble` | Three-movement chamber expansion |
| `art_song` | Work in progress |
| `algorithmic` | Scaffold placeholder |

## CI/CD

- `build.yml`: parallel jobs build every composition; the release job runs on `v*` tags, collects artifacts, generates thumbnails, and publishes a GitHub Release.
- `docs.yml`: builds Sphinx HTML and deploys to GitHub Pages on every push to `main`.

Triggering a release: push a tag matching `v*`.

## Documentation

The `docs/` directory is a Sphinx project with architecture notes, case studies, configuration documentation, and build/release workflow notes. Source lives in `docs/`; built output goes to `docs/_build/` and is git-ignored.

## Working Norms

- Prefer repo-specific commands and validation over generic guesses.
- When editing score data, keep all parts aligned by measure count and duration.
- Run the relevant generator after score changes so PDF/MIDI output is verified.
- When changing docs that describe score form, keep them aligned with the current notated implementation.
