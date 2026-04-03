Case Study VII: Bird Im-Migration Ensemble
==========================================

``bird_im_migration_ensemble`` takes the analysis-driven material from :doc:`10a-case-study-bird-im-migration` and turns it into a short chamber piece.
The earlier package is a proof of concept for reducing bird-like partial activity into playable notation.
The ensemble package keeps that reduction as its source library, but it stops trying to remain purely spectral.
Instead, it treats the bird fragments as modular motives and places them inside a more obviously composed environment: alternating treble calls, a low piano drone with patterned variation, and percussion that behaves like an environmental pulse rather than a literal transcription of the recording.

This case study shows a second stage of the same project.
The spectral analysis is still there.
The curated regions are still there.
But the composition is no longer only a reduction of recorded sound.
It becomes a score system that can support performance, transformation, substitution of instruments, and movement-level formal planning.

Download
--------

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `bird-im-migration-ensemble.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.pdf>`_
   * - LilyPond
     - `bird-im-migration-ensemble.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.ly>`_
   * - MIDI
     - `bird-im-migration-ensemble.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.midi>`_
   * - WAV
     - `bird-im-migration-ensemble.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.wav>`_
   * - Movement I WAV
     - `bird-im-migration-ensemble-mvt1.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt1.wav>`_
   * - Movement II WAV
     - `bird-im-migration-ensemble-mvt2.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt2.wav>`_
   * - Movement III WAV
     - `bird-im-migration-ensemble-mvt3.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt3.wav>`_

.. only:: html

   Listen
   ------

   Full Piece
   ^^^^^^^^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

   Movement I
   ^^^^^^^^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt1.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

   Movement II
   ^^^^^^^^^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt2.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

   Movement III
   ^^^^^^^^^^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-mvt3.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

Score Preview
-------------

.. image:: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble-thumbnail.png
   :alt: First page preview of Bird Im-Migration Ensemble
   :target: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-ensemble.pdf
   :width: 50%

From Spectral Reduction to Modular Phrases
------------------------------------------

The raw material is still the same field recording and the same curated regions introduced in the original Bird Im-Migration chapter.
The difference is that the ensemble package does not treat those regions as a finished score.
It converts them into a phrase library.
Each phrase remembers which sample and which curated region it came from.
This keeps later transformations attached to a recognizable source motive rather than turning them into anonymous note sequences.

The core data structures and the default movement plans live together in the generator module:

.. literalinclude:: ../src/bird_im_migration_ensemble/generator.py
   :language: python
   :lines: 33-199
   :caption: Phrase and movement data classes plus the default three-movement plan.

In practice this means the composition can be described at the level of phrase behavior rather than note-by-note editing.
The movement configuration chooses tempo, meter, pitch center, phrase count, percussion density, and the allowed transformations for calls and responses.
That is the main difference between this package and the earlier spectral reduction package.
The new piece is still derived from the bird analysis, but it is shaped as a parametric form.

Phrase Extraction and Transformation
------------------------------------

The phrase library is built directly from the curated spectral regions.
Each region is quantized onto a 16th-note grid and stored as one modular phrase object.
From there, the package creates variants using a deliberately small set of operations: identity, retrograde, augmentation, and repetition.

.. literalinclude:: ../src/bird_im_migration_ensemble/generator.py
   :language: python
   :lines: 246-299
   :caption: Converting curated regions into phrase objects and creating transformed phrase variants.

This is the central compositional decision in the package.
The score does not ask the spectral analysis to solve the whole piece.
Instead, the analysis contributes a motive bank.
The movement planner then decides whether a phrase should be stated plainly, reversed, stretched, or repeated.
That keeps the birdsong recognizable but also lets the piece behave like chamber music rather than a transcription exercise.

How the Bird Lines Are Created
------------------------------

The violin and trumpet lines are built from the same pool of phrase variants.
The generator chooses a phrase for the call, maps it into the violin register, and then optionally answers it with a transformed phrase in the trumpet register.
The mapping is intentionally asymmetric: the higher line prefers the upper note in each bin, while the trumpet response sits lower and answers rather than duplicates.

.. literalinclude:: ../src/bird_im_migration_ensemble/generator.py
   :language: python
   :lines: 600-785
   :caption: Movement construction, including call-and-response writing for violin and trumpet.

This is where the alternating bird effect comes from.
One line states a phrase and the other line responds in the next span.
Because calls and responses draw from overlapping but not identical transformation sets, the exchange can sound like imitation, transformation, or recollection.
If violin or trumpet are unavailable in performance, the same lines could be reassigned to voice, whistle, or another treble instrument without changing the underlying phrase logic.
The system is therefore instrument-specific in engraving, but not conceptually tied to one only possible ensemble.

Environmental Layers: Piano and Percussion
------------------------------------------

The environmental effect in this piece is not produced by spectral fidelity alone.
It comes from adding non-spectral layers that support the bird material without trying to mimic it exactly.
The piano is the clearest example.
The left hand provides the low drone and harmonic floor.
The right hand adds a lighter, pattern-based comping layer on an eighth-note grid.
Movement II is handled differently again, with a two-measure arpeggiated left-hand cycle to make the nocturne character more audible.

.. literalinclude:: ../src/bird_im_migration_ensemble/generator.py
   :language: python
   :lines: 376-503
   :caption: Building the piano layers, with sustained drone behavior, right-hand patterns, and the nocturne arpeggiation.

The percussion line is also environmental rather than imitative.
It does not try to duplicate every attack in the birdsong.
Instead, it uses named rhythmic patterns and then thins or accents them according to what the bird lines are doing.
That gives the texture a sense of place: not literal forest noise, but a patterned pulse that can suggest environment, motion, or distance.

.. literalinclude:: ../src/bird_im_migration_ensemble/generator.py
   :language: python
   :lines: 550-597
   :caption: Turning named rhythmic patterns into a light environmental percussion line.

This added material is why the piece is not simply a spectral reduction with accompaniment.
The ensemble code accepts that a playable composition can preserve the bird motive while also introducing supporting musical layers that are chosen for form, playability, and atmosphere.

How the Piece Is Rendered
-------------------------

The package also treats rendering as part of the composition system.
Notation is produced in LilyPond and then the audio path separates the ensemble into layers before synthesis.
The current render path uses Salamander for the two piano hands, Aegean for the melodic ensemble, and a clap-style render for percussion.
Each movement is rendered separately and then concatenated into a full listening file.

.. literalinclude:: ../src/bird_im_migration_ensemble/cli.py
   :language: python
   :lines: 194-325
   :caption: Movement-aware layered WAV rendering for Bird Im-Migration Ensemble.

This layered render path exists for musical reasons as much as technical ones.
It keeps the piano drone audible, gives the treble material its own timbral space, and allows the release process to expose both the full piece and the individual movement WAVs.
The build and release workflow therefore records not only the score but also the listening model used during composition.

What This Case Study Shows
--------------------------

The ensemble package shows a practical way to move from analysis-derived material into a more independent composition.
The source recording still plays an important role.
The curated regions remain central as well.
But the final result is not governed only by the source audio.
It is governed by a phrase system, a movement plan, and a set of environmental layers designed to make the piece performable.

This hybrid approach is one way to move from analysis-derived material toward a more independent composition.
It suggests how an analysis-driven motive can remain visible while the surrounding musical world becomes more flexible, more modular, and more explicitly composed.
