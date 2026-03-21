# Music Composition with Abjad

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

## Projects

### Modus Operandi for Piano

A three-movement minimalist solo piano work in F Dorian, F Phrygian, and F Lydian.

- Source: `src/modus_operandi_abjad/`
- CLI: `python -m modus_operandi_abjad -o build`

| Format | Link |
| --- | --- |
| PDF | [modus-operandi-abjad.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.pdf) |
| LilyPond | [modus-operandi-abjad.ly](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.ly) |
| MIDI | [modus-operandi-abjad.midi](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.midi) |
| WAV | [modus-operandi-abjad.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.wav) |

### Jazz Rhythmic Patterns

A small library of generated jazz comping rhythms rendered as score, LilyPond, and MIDI.

- Source: `src/jazz_rhythm/`
- CLI: `python -m jazz_rhythm -o build`

| Format | Link |
| --- | --- |
| PDF | [jazz-rhythms.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.pdf) |
| LilyPond | [jazz-rhythms.ly](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.ly) |
| MIDI | [jazz-rhythms.midi](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.midi) |

### Algo Rhythms Quartet No. 1

A generated tonal piano quartet for piano, violin, viola, and cello. This is the first proof-of-concept score in the larger quartet line.

- Source: `src/algorithmic_piano_quartet/`
- Config: `configs/algorithmic-piano-quartet.toml`
- CLI: `python -m algorithmic_piano_quartet -c configs/algorithmic-piano-quartet.toml -o build`

| Format | Link |
| --- | --- |
| PDF | [algo-rhythms-quartet-no-1.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.pdf) |
| LilyPond | [algo-rhythms-quartet-no-1.ly](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.ly) |
| MIDI | [algo-rhythms-quartet-no-1.midi](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.midi) |
| WAV | [algo-rhythms-quartet-no-1.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.wav) |

### Algorithmic Piano Quartet No. 2

A separate exploratory branch of the quartet work. It starts from No. 1 but is allowed to evolve independently.

- Source: `src/algorithmic_piano_quartet_no2/`
- Config: `configs/algorithmic-piano-quartet-no2.toml`
- CLI: `python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build`

| Format | Link |
| --- | --- |
| PDF | [algorithmic-piano-quartet-no-2.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.pdf) |
| LilyPond | [algorithmic-piano-quartet-no-2.ly](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.ly) |
| MIDI | [algorithmic-piano-quartet-no-2.midi](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.midi) |
| WAV | [algorithmic-piano-quartet-no-2.wav](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.wav) |

### Algorithmic

A placeholder package for future algorithmic composition work.

- Source: `src/algorithmic/`
- CLI: `python -m algorithmic -o build`

| Format | Link |
| --- | --- |
| PDF | [algorithmic.pdf](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.pdf) |
| LilyPond | [algorithmic.ly](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.ly) |
| MIDI | [algorithmic.midi](https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.midi) |

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
algorithmic-piano-quartet
algorithmic-piano-quartet-no2
algorithmic
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
python -m algorithmic_piano_quartet -c configs/algorithmic-piano-quartet.toml -o build
python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build
python -m algorithmic -o build
```

## Releases and CI

The repository uses GitHub Actions for builds, releases, and documentation deployment.

- pushes to `main` rebuild the docs site
- version tags create a GitHub release
- releases include score assets, report PDF, and score thumbnails
- the docs site is published at `https://compositions.gkt.sh`

For inline audio players, score previews, and the full technical report, see:

- https://compositions.gkt.sh
