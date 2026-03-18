# Algorithmic Piano Quartet No. 2

**Composer:** George K. Thiruvathukal

This package starts from the current `algorithmic_piano_quartet` implementation, but it is intended to develop independently. The goal is to preserve **Algo Rhythms Quartet No. 1** as it is while giving No. 2 a separate place for new musical ideas, parameter choices, and future structural changes.

## Starting Point

The initial config for No. 2 is based on the same quartet setup used for No. 1:

- piano
- violin
- viola
- cello

It uses its own config file:

- `configs/algorithmic-piano-quartet-no2.toml`

and its own module entry point:

- `python -m algorithmic_piano_quartet_no2`
- `algorithmic-piano-quartet-no2`

## Purpose

This package exists so that new ideas can be explored without changing the existing No. 1 composition. In practice, that means No. 2 can diverge in any of these areas:

- pitch materials
- rhythmic behavior
- texture and density
- form
- dynamics
- instrumentation rules
- rendering and notation choices

## Typical Commands

Build notation, MIDI, and LilyPond source:

```bash
python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build
```

Build PDF and WAV as well:

```bash
python -m algorithmic_piano_quartet_no2 -c configs/algorithmic-piano-quartet-no2.toml -o build --pdf --wav
```

## Current Build Scope

No. 2 is part of the local `build.sh` workflow, so a normal local build will generate its outputs alongside the other compositions.

It is not part of the GitHub Actions workflow yet. That is still intentional while No. 2 remains in an exploratory stage.
