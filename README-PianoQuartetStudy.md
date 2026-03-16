# Piano Quartet Study

**Composer:** George K. Thiruvathukal

This project is a generated **tonal** piano quartet study for:

- piano
- violin
- viola
- cello

The current piece is titled **Algo Rhythms Quartet No. 1**. The title reflects the basic idea of the piece. Rhythm is central, and the music is generated under clear rules for range, motion, and density.

## Musical Idea

This piece is a proof of concept for a future planned work. That later work is intended to support a broader set of atonal approaches and a wider range of instrumentation. This quartet is an earlier stage in that process.

For now, the piece stays tonal on purpose. The goal is to test the basic musical and technical ideas first. Those ideas include:

- rhythm is treated as a primary structural force
- the ensemble writing is constrained enough to remain intelligible
- melodic motion is limited so that line and register stay coherent
- harmonic language remains restrained so the listener can hear the rhythmic design clearly

The point is not to present the final atonal system yet. The point is to confirm that the current method can produce material that is clear, playable, and worth developing further.

## Compositional Approach

The piano, violin, viola, and cello are used as distinct parts with different roles. The strings carry much of the line and sustain. The piano helps with attack, spacing, and support. The system avoids large leaps and excessive density so that the material stays readable and playable.

The title **Quartet No. 1** is also intentional. It marks this as a first entry in a larger line of work rather than as a finished endpoint. The planned direction is toward a more general algorithmic composition system that can handle different atonal options, different ensembles, and more developed formal ideas.

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

Although this study belongs to a larger atonal project, the present material is tonal. That is a deliberate choice. It allows the current system to be tested in a simpler setting before moving to a more general atonal design. The proof-of-concept stage is focused on rhythm, range handling, ensemble spacing, score generation, and audio rendering. Broader atonal methods and instrumentation come later.

## Files

- **Config:** `piano-quartet.toml`
- **Source:** `src/algorithmic_piano_quartet/`
- **CLI:** `python -m algorithmic_piano_quartet`

## Configuration Settings

The quartet is configured with `piano-quartet.toml`. The available sections are:

### Top-Level Fields

- `title`: score title
- `composer`: composer name shown in the score

### `[output]`

- `basename`: base filename for generated output
- `label`: optional extra text added to the filename stem
- `include_measures`: add the measure count to the filename
- `include_tempo`: add the tempo to the filename
- `include_seed`: add the random seed to the filename
- `include_timestamp`: add a timestamp to the filename
- `timestamp_format`: Python `strftime` format used for the timestamp

### `[render]`

- `piano_soundfont`: soundfont used for the piano render layer
- `strings_soundfont`: soundfont used for violin, viola, and cello
- `sample_rate`: output WAV sample rate

The config loader also accepts a legacy `soundfont` field, but the current production setup uses the split `piano_soundfont` and `strings_soundfont` fields.

### `[generation]`

- `measures`: number of measures to generate
- `time_signature`: bar structure as `[numerator, denominator]`
- `min_note_duration`: smallest note value allowed
- `max_note_duration`: largest note value allowed
- `min_rest_duration`: smallest rest value allowed
- `max_rest_duration`: largest rest value allowed
- `max_simultaneous_tones_per_quantum`: density cap for notes sounding at the same time
- `max_pitch_leap`: largest melodic leap allowed between adjacent notes
- `tempo_bpm`: tempo in quarter-notes per minute
- `seed`: random seed for reproducible output

Duration values such as `1/16` and `1/4` must align with the minimum note duration grid.

### `[materials]`

- `pitch_classes`: pitch-class collection used by the generator

### `[[parts]]`

Each part entry defines one instrument. The available fields are:

- `id`: stable internal part identifier
- `name`: full instrument name
- `short_name`: abbreviated name for the score
- `family`: instrument family such as `strings` or `keyboard`
- `clef`: staff clef
- `role`: broad musical role such as `melodic`, `bass`, or `keyboard`
- `midi_channel`: MIDI channel used for export
- `midi_program`: MIDI program number
- `midi_instrument`: LilyPond / MIDI instrument name
- `range`: playable range as `["LOW", "HIGH"]`
- `staff_type`: optional staff layout; use `grand` for piano

The current quartet uses four `[[parts]]` blocks:

- violin
- viola
- cello
- piano

## Building

From the repository root:

```bash
PYTHONPATH=src ./.venv/bin/python -m algorithmic_piano_quartet -c piano-quartet.toml -o build --pdf --wav
```

This produces uniquely named output files in `build/`, including:

- `.ly`
- `.pdf`
- `.midi`
- `.wav`

The filename stem is built from the configured base name plus selected generation properties such as measures, tempo, seed, and a timestamp.

## Notes On Audio

WAV rendering is done from Python through FluidSynth using the soundfont configured in `piano-quartet.toml`.

The current final production setup uses two soundfonts:

```bash
~/.soundfonts/SalamanderGrandPiano-V3+20200602.sf2
~/.soundfonts/AegeanSymphonicOrchestra.sf2
```

The production render uses:

- **Salamander Grand Piano** for the piano part
- **Aegean Symphonic Orchestra** for violin, viola, and cello

The render path creates a piano WAV and a strings WAV separately, then combines them into one final file with `ffmpeg`. This is the current preferred production method for the quartet because it gives a better result than trying to render all parts from a single soundfont.

If either file is missing, the quartet CLI will download and cache it automatically on first WAV render.

If the selected soundfont does not contain violin, viola, and cello patches, those parts will be substituted during playback. A piano-only soundfont such as Salamander is fine for render-path testing, but it does not provide true quartet timbres.

## Typical Commands

Render notation only:

```bash
PYTHONPATH=src ./.venv/bin/python -m algorithmic_piano_quartet -c piano-quartet.toml -o build --pdf
```

Override measures and tempo from the command line:

```bash
PYTHONPATH=src ./.venv/bin/python -m algorithmic_piano_quartet -c piano-quartet.toml -o build --pdf --wav --measures 24 --tempo 96
```
