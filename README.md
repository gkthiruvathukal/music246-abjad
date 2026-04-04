# Music Composition with Abjad

[![Build And Release](https://github.com/gkthiruvathukal/compositions-abjad/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/gkthiruvathukal/compositions-abjad/actions/workflows/build.yml)
[![Docs](https://github.com/gkthiruvathukal/compositions-abjad/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/gkthiruvathukal/compositions-abjad/actions/workflows/docs.yml)
[![Release](https://img.shields.io/github/v/release/gkthiruvathukal/compositions-abjad)](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest)

This repository contains programmatic music composition work built with [Python](https://www.python.org/), [Abjad](https://abjad.github.io/), and [LilyPond](https://lilypond.org/). It includes finished scores, exploratory composition systems, and a Sphinx-based technical report.

## Documentation

The full documentation and technical report are available at:

- https://compositions.gkt.sh

The docs site includes:

- project overview
- case studies for each current score
- release download links
- listen sections for available WAV files
- score preview thumbnails

## Citation

If this repository or the accompanying report is useful in your own work, please consider citing it.

```bibtex
@article{Thiruvathukal2026,
  author = "George K. Thiruvathukal",
  title = "{Composition using Python and Abjad/LilyPond: Life Beyond Notation Software}",
  year = "2026",
  month = "3",
  url = "https://figshare.com/articles/online_resource/Composition_using_Python_and_Abjad_LilyPond_Life_Beyond_Notation_Software/31827391",
  doi = "10.6084/m9.figshare.31827391.v1"
}
```

## Projects

### Modus Operandi for Piano

A three-movement minimalist solo piano work in F Dorian, F Phrygian, and F Lydian.

- Source: `src/modus_operandi_abjad/`
- CLI: `python -m modus_operandi_abjad -o build`

| Format | Link |
| --- | --- |
| PDF | [modus-operandi-abjad.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.pdf) |
| WAV | [modus-operandi-abjad.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.wav) |

### Jazz Rhythmic Patterns

A small library of generated jazz comping rhythms rendered as score, LilyPond, MIDI, and clap-based WAV.

- Source: `src/jazz_rhythm/`
- CLI: `python -m jazz_rhythm -o build`

| Format | Link |
| --- | --- |
| PDF | [jazz-rhythms.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.pdf) |
| WAV | [jazz-rhythms.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.wav) |

### Algo Rhythms Quartet No. 1

A generated tonal piano quartet for piano, violin, viola, and cello. This is the first proof-of-concept score in the larger quartet line.

- Source: `src/algorithmic_piano_quartet_no1/`
- Config: `configs/algorithmic-piano-quartet-no1.toml`
- CLI: `python -m algorithmic_piano_quartet_no1 -c configs/algorithmic-piano-quartet-no1.toml -o build`

| Format | Link |
| --- | --- |
| PDF | [algo-rhythms-quartet-no-1.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.pdf) |
| WAV | [algo-rhythms-quartet-no-1.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.wav) |

### Algo Rhythms Quartet No. 2

A separate exploratory branch of the quartet work. It starts from No. 1 but is allowed to evolve independently.

- Source: `src/algorithmic_piano_quartet_no2/`
- Config: `configs/algorithmic-piano-quartet-no2.toml`
- CLI: `python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build`

| Format | Link |
| --- | --- |
| PDF | [algo-rhythms-quartet-no-2.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-2.pdf) |
| WAV | [algo-rhythms-quartet-no-2.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-2.wav) |

### Algorithmic

A placeholder package for future algorithmic composition work.

- Source: `src/algorithmic/`
- CLI: `python -m algorithmic -o build`

| Format | Link |
| --- | --- |
| PDF | [algorithmic.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.pdf) |

### Bird Im-Migration

An analysis-driven reduction of curated birdsong partials into short playable score fragments.

- Source: `src/bird_im_migration/`
- CLI: `python -m bird_im_migration -o build --quantization 16 --pdf --midi`

| Format | Link |
| --- | --- |
| PDF (q16) | [bird-im-migration-q16.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.pdf) |
| WAV (q16) | [bird-im-migration-q16.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.wav) |
| PDF (q32) | [bird-im-migration-q32.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.pdf) |
| WAV (q32) | [bird-im-migration-q32.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.wav) |

### Bird Im-Migration Ensemble

A three-movement chamber expansion of the Bird Im-Migration material for violin, trumpet, percussion, and piano.

- Source: `src/bird_im_migration_ensemble/`
- CLI: `python -m bird_im_migration_ensemble -o build --pdf --wav`

| Format | Link |
| --- | --- |
| PDF | [bird-im-migration-ensemble.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.pdf) |
| WAV | [bird-im-migration-ensemble.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.wav) |

## Setup

Requirements:

- Python 3.10+
- LilyPond 2.24+
- FluidSynth and `ffmpeg` for WAV rendering

Install the package in editable mode:

```bash
pip install -e .
```

This exposes these console scripts:

```bash
modus-operandi-abjad
jazz-rhythms
algorithmic-piano-quartet-no1
algorithmic-piano-quartet-no2
algorithmic
bird-im-migration
bird-im-migration-ensemble
```

Install LilyPond:

- macOS: `brew install lilypond`
- Ubuntu: `sudo apt install lilypond`

Install audio tools if you want WAV output:

- macOS: `brew install fluidsynth ffmpeg`
- Ubuntu: `sudo apt install fluidsynth ffmpeg`

## Local Builds

Build the score artifacts:

```bash
./build.sh
```

Use a different output directory if needed:

```bash
./build.sh out
```

Build the Sphinx docs and report:

```bash
./build-docs.sh
```

This builds:

- HTML docs in `docs/_build/html`
- PDF report in `docs/_build/latex/composition-report.pdf`

## Direct CLI Usage

You can also run the packages directly:

```bash
python -m modus_operandi_abjad -o build
python -m jazz_rhythm -o build
python -m algorithmic_piano_quartet_no1 -c configs/algorithmic-piano-quartet-no1.toml -o build
python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build
python -m algorithmic -o build
python -m bird_im_migration -o build --quantization 16 --pdf --midi
python -m bird_im_migration_ensemble -o build --pdf --wav
```

## Releases and CI

The repository uses GitHub Actions for builds, releases, and documentation deployment.

- pushes to `main` rebuild the docs site
- version tags create a GitHub release
- releases include score assets, report PDF, and score thumbnails
- the docs site is published at `https://compositions.gkt.sh`

For inline audio players, score previews, and the full technical report, see:

- https://compositions.gkt.sh
