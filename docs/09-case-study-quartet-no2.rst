Case Study IV: Algorithmic Piano Quartet No. 2
===============================================

``Algorithmic Piano Quartet No. 2`` exists because the repository needed a place to continue experimenting without destabilizing No. 1. From a software point of view, this is a forked package. From a musical point of view, it is a controlled branch for testing new behavior. The decision to fork rather than rewrite No. 1 in place is important. It keeps the first proof-of-concept score intact while opening a second path for more aggressive technical and musical changes.

The first large difference is the piano. No. 1 mainly treats piano lines as single-note event streams. No. 2 allows the piano to generate chords. Those chords are still derived from the configured pitch-class material and the configured hand ranges, but they are shaped with more detail. The left and right hands can have different chord sizes, different preferred spacing, and different span limits.

The second large difference is the occupancy model. In No. 1, the piano competes with the strings under the same density cap. In No. 2, piano has its own occupancy budget. That gives the keyboard more room to act like a harmonic instrument rather than like two more melodic voices squeezed into the same global constraint.

The third difference is the way left-hand spacing is treated. No. 2 now looks at whole chord shapes instead of simply growing a chord one pitch at a time from a seed. This makes it possible to prefer a wider overall left-hand span and to move away from narrow triadic shapes when the configuration asks for something more open.

The second quartet extends the same basic internal model as No. 1, but it expands the generation settings. The added fields define separate piano occupancy, separate left-hand and right-hand chord ranges, and separate preferred spacing rules. In other words, No. 2 does not invent a new architecture. It stretches the old one in a more piano-aware direction.

Latest release artifacts for this score are:

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `algorithmic-piano-quartet-no-2.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.pdf>`_
   * - LilyPond
     - `algorithmic-piano-quartet-no-2.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.ly>`_
   * - MIDI
     - `algorithmic-piano-quartet-no-2.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.midi>`_
   * - WAV
     - `algorithmic-piano-quartet-no-2.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic-piano-quartet-no-2.wav>`_

The config classes make that change easy to see. ``PartConfig`` still carries one instrument definition, including name, role, staff type, and range. ``RenderConfig`` still carries the SoundFont choices and sample rate. The main difference is ``GenerationConfig``. In No. 2, this class carries the extra piano controls: separate occupancy for piano, separate chord-size limits for each hand, separate span limits, and separate preferred interval lists. Those fields are the contract between the TOML file and the generator.

.. literalinclude:: ../src/algorithmic_piano_quartet_no2/config.py
   :language: python
   :lines: 16-92
   :caption: Core No. 2 configuration data classes.

The chord builder is a good example of that evolution. This function expects a seed pitch, hand range, pitch-class pool, requested chord size, span limits, preferred interval steps, and a minimum separation between adjacent notes. Given those inputs, it searches candidate chord shapes and keeps the result inside the hand range:

.. literalinclude:: ../src/algorithmic_piano_quartet_no2/generator.py
   :language: python
   :pyobject: _build_piano_chord
   :caption: Chord construction in Quartet No. 2.

No. 2 also has a larger configuration surface than No. 1 because it needs to expose these experiments clearly. That is a feature, not a flaw. The second quartet is the branch where new musical controls are tested. If a change proves useful and stable, it can later inform a more general future system.
