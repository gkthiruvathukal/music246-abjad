Case Study III: Algo Rhythms Quartet No. 1
==========================================

``Algo Rhythms Quartet No. 1`` is the first substantial config-driven score in the repository.
Its role is clear in the project documentation: it is a proof of concept for a broader future composition system.
The long-term direction is more general and eventually more post-tonal, but No. 1 is deliberately tonal.
That choice simplifies the first experiment.
It lets the project test rhythm, range handling, density control, engraving, and audio rendering before the harmonic language becomes more ambitious.

The score is defined through a TOML file and a generator package.
The TOML file controls title, file naming, render settings, core generation constraints, pitch-class material, and instrumentation.
The generator then creates quantized event streams for violin, viola, cello, and piano.
The system enforces a small set of global rules: pitch choice must remain within a supplied pitch-class collection, melodic leaps are bounded, note and rest lengths are bounded, and the total sounding density is capped.

The quartet code relies on a small set of data classes.
``PartConfig`` describes one instrument entry from the TOML file.
It carries the identifiers, instrument names, MIDI settings, and playable range.
``GenerationConfig`` holds the global generation rules such as measure count, durations, leap limits, and density limits.
``ProjectConfig`` is the top-level object passed through the package.
It bundles title, output settings, pitch material, generation settings, render settings, and the list of parts.

The config loader is where these musical and technical settings become one internal project configuration:

.. literalinclude:: ../src/algorithmic_piano_quartet/config.py
   :language: python
   :lines: 13-63
   :caption: Core quartet configuration data classes.

.. literalinclude:: ../src/algorithmic_piano_quartet/config.py
   :language: python
   :lines: 103-194
   :caption: Loading the No. 1 configuration from TOML.

The musical content is not chosen all at once.
It is built event by event on a quantized timeline.
The generator uses a few core classes here as well.
``Event`` represents a single timed unit with a start position, duration, and pitch.
``VoiceMaterial`` is the list of events for one staff.
``Piece`` is the generated score-level result, including the metadata needed later by the score layer.
These classes are simple containers, but they matter because they define the internal shape of the generated material.

The result is not strict counterpoint or formal harmony.
It is a constrained event generator designed to produce clear, playable material.

Download
--------

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `algo-rhythms-quartet-no-1.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.pdf>`_
   * - LilyPond
     - `algo-rhythms-quartet-no-1.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.ly>`_
   * - MIDI
     - `algo-rhythms-quartet-no-1.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.midi>`_
   * - WAV
     - `algo-rhythms-quartet-no-1.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.wav>`_

.. only:: html

   Listen
   ------

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

Score Preview
-------------

.. image:: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1-thumbnail.png
   :alt: First page preview of Algo Rhythms Quartet No. 1
   :target: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algo-rhythms-quartet-no-1.pdf
   :width: 50%

That event loop sits near the center of the package:

.. literalinclude:: ../src/algorithmic_piano_quartet/generator.py
   :language: python
   :lines: 188-272
   :caption: Core event generation for Quartet No. 1.

Once events exist, the score layer turns them into Abjad objects, attaches dynamics and notation details, applies ottava marks, and assembles the final ensemble score.
The system also adds a short end note that records the main compositional parameters for the generated run.

No. 1 also matters as a baseline for the second quartet.
It shows the original generator design before the later work on chordal piano writing, separate piano occupancy, and hand-specific spacing.
