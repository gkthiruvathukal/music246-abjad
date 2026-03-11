# Modus Operandi for Piano

**Composer:** George K. Thiruvathukal

A monody for solo piano in three movements, each built on a different mode rooted on F. The *minimalist* piece explores the melodic character of the Dorian, Phrygian, and Lydian modes through contrasting tempi and textures while maintaining a single-voice (monophonic) melodic line in the right hand over simple intervallic accompaniment in the left hand.

| Movement | Mode | Meter | Tempo |
|----------|------|-------|-------|
| I | F Dorian | 4/4 | Lento (quarter = 46) |
| II | F Phrygian | 6/8 | Presto agitato (dotted quarter = 80) |
| III | F Lydian | 4/4 | Andante tranquillo (quarter = 76) |

Each movement is 16 bars long. The right hand carries the melodic line in quarter notes (I), eighth notes with ottava (II), and quarter notes with ottava (III). The left hand provides a slower-moving accompaniment in half notes (I, III) or dotted quarters (II), outlining intervals of fourths and fifths rooted on F.

## AI Disclosure with Commentary

The compositional ideas in this work are my own.

After using WYSIWYG tools for notating my composition, I decided to reexamine Abjad (a Python framework for composing music). I have used Abjad for other works, including my Jazz Scales "book" at https://github.com/gkthiruvathukal/jazz-patterns.

I have used LLMs to become more proficient with the Abjad API. It is both amazing and astonishing what is possible when one knows what they are doing in computer science and music at the same time!

This API is powerful but complex and greatly benefits from LLMs to learn many of its advanced (sometimes cryptic!) features.
Although I have written Abjad/Python code by hand, it is much better to have assistance from the LLM so I can focus on the "good stuff" in CS and Music.


## Building

The score is generated programmatically using [Abjad](https://abjad.github.io/), a Python library for formalized score control, and compiled to PDF and MIDI with [LilyPond](https://lilypond.org/).

### Requirements

- Python >= 3.10
- LilyPond >= 2.24

### Install and build

```bash
pip install -e .
python -m modus_operandi_abjad -o build
./midi2wav.sh build/modus-operandi-abjad.midi
```

This produces the LilyPond source, engraved score, and combined MIDI in `build/`. Running `midi2wav.sh` adds the WAV render:

| File | Description |
|------|-------------|
| `modus-operandi-abjad.ly` | Generated LilyPond source |
| `modus-operandi-abjad.pdf` | Engraved score |
| `modus-operandi-abjad.midi` | Combined MIDI (all three movements) |
| `modus-operandi-abjad.wav` | Playable audio with Yamaha Grand Piano Sound Font |

You can also build individual outputs:

```bash
python -m modus_operandi_abjad -o build --ly
python -m modus_operandi_abjad -o build --pdf
python -m modus_operandi_abjad -o build --midi
```

### Rendering audio from MIDI

The MIDI file can be rendered to WAV using [FluidSynth](https://www.fluidsynth.org/) and the [Salamander Grand Piano](https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html) soundfont (Yamaha C5, 16 velocity layers). The included `midi2wav.sh` script handles downloading the soundfont (~296 MB) on first use and caching it in `~/.soundfonts/`.

**Requirements:** FluidSynth must be installed on your system (`brew install fluidsynth` on macOS, `apt install fluidsynth` on Ubuntu).

You can also run the script directly on any MIDI file:

```bash
./midi2wav.sh <input.midi> [output.wav]
```

If the output path is omitted, it defaults to the input filename with a `.wav` extension. For example:

```bash
./midi2wav.sh build/modus-operandi-abjad.midi
# produces build/modus-operandi-abjad.wav
```

### Playing audio from the command line

Once you have a WAV file, you can play it directly from the terminal without a GUI player:

**macOS** (built-in, no install needed):

```bash
afplay build/modus-operandi-abjad.wav
```

`afplay` also supports `-t <seconds>` to limit playback duration and `-r <rate>` to adjust playback speed.

**Linux** (using `aplay` from ALSA, typically pre-installed):

```bash
aplay build/modus-operandi-abjad.wav
```

Alternatively, if you have PulseAudio or PipeWire:

```bash
paplay build/modus-operandi-abjad.wav
```

**Windows** (PowerShell, no install needed):

```powershell
(New-Object Media.SoundPlayer "build\modus-operandi-abjad.wav").PlaySync()
```

Or using the built-in `start` command to open the file in the default media player:

```cmd
start build\modus-operandi-abjad.wav
```

### Building from the LilyPond source directly

If you have LilyPond installed but not Python/Abjad, you can compile the hand-written source or a released `.ly` file directly:

```bash
lilypond -o build src/modus-operandi.ly
```

Or download `modus-operandi-abjad.ly` from the [latest release](../../releases/latest) and run:

```bash
lilypond modus-operandi-abjad.ly
```

## CI/CD

Every push to `main` and every pull request builds the score via GitHub Actions. The repository uses one shared workflow to build both compositions. When a version tag (`v*`) is pushed, a GitHub Release is created automatically with the PDF, MIDI, LilyPond source, and WAV for Modus Operandi attached.

```bash
git tag v0.2
git push --tags
```
