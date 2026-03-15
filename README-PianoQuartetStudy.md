# Piano Quartet Study

**Composer:** George K. Thiruvathukal

This project is a generated **tonal** piano quartet study for:

- piano
- violin
- viola
- cello

It sits in the repository as a practical stepping stone toward a larger atonal composition system, but the study itself should not be described as atonal. The tonal focus is deliberate: it provides a controlled way to verify that the core building blocks are working before moving to atonal composition. The current generator focuses on constrained rhythmic generation, bounded melodic motion, range-aware writing, and score/audio output workflows.

## Current Scope

The study is built from a TOML configuration file and rendered with Abjad and LilyPond. The generator currently supports:

- configurable measure count
- configurable tempo
- reproducible generation via seed
- minimum / maximum note durations
- minimum / maximum rest durations
- a global cap on simultaneous tones per quantized time unit
- range limits per instrument
- conservative voice leading with bounded pitch leaps
- ottava notation for extreme registers
- automatic consolidation of adjacent rests

## Tonal Status

Although this study is part of the broader path toward an atonal composition project, the present material is tonal in character and should be treated as an exploratory chamber-writing study rather than as the atonal symphonic work itself. The reason for keeping it tonal at this stage is to validate the underlying machinery first: instrumentation, rhythmic constraints, range handling, voice-leading controls, score generation, and audio rendering all need to be reliable before the project moves into atonal language.

## Files

- **Config:** `piano-quartet.toml`
- **Source:** `src/atonal_piano_quartet/`
- **CLI:** `python -m atonal_piano_quartet`

## Building

From the repository root:

```bash
PYTHONPATH=src ./.venv/bin/python -m atonal_piano_quartet -c piano-quartet.toml -o build --pdf --wav
```

This produces uniquely named output files in `build/`, including:

- `.ly`
- `.pdf`
- `.midi`
- `.wav`

The filename stem is built from the configured base name plus selected generation properties such as measures, tempo, seed, and a timestamp.

## Notes On Audio

WAV rendering is done from Python through FluidSynth using the soundfont configured in `piano-quartet.toml`.

If the selected soundfont does not contain violin, viola, and cello patches, those parts will be substituted during playback. The current local Salamander piano soundfont is sufficient to test the render path, but it does not provide true quartet timbres.

## Typical Commands

Render notation only:

```bash
PYTHONPATH=src ./.venv/bin/python -m atonal_piano_quartet -c piano-quartet.toml -o build --pdf
```

Override measures and tempo from the command line:

```bash
PYTHONPATH=src ./.venv/bin/python -m atonal_piano_quartet -c piano-quartet.toml -o build --pdf --wav --measures 24 --tempo 96
```
