Case Study VI: Bird Im-Migration
================================

The ``bird_im_migration`` package adapts a spectral-composition workflow into the larger ``compositions-abjad`` repository.
It begins from a field recording of birds and a SPEAR partial-tracking analysis of that recording.
The compositional goal is to reduce bird-like spectral behavior into performable notation while preserving a visible link to the source analysis.

Unlike the more abstract or algorithmic case studies in this repository, this package starts with a fixed audio analysis file and then applies musical reduction on top of it.
That makes it a useful counterexample in the book because the score does not begin from a pitch set or a generative procedure.
It begins from tracked partials in a real sound recording.

Download
--------

.. list-table::
   :header-rows: 1

   * - Variant
     - Format
     - Link
   * - q16
     - PDF
     - `bird-im-migration-q16.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.pdf>`_
   * - q16
     - LilyPond
     - `bird-im-migration-q16.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.ly>`_
   * - q16
     - MIDI
     - `bird-im-migration-q16.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.midi>`_
   * - q16
     - WAV
     - `bird-im-migration-q16.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.wav>`_
   * - q32
     - PDF
     - `bird-im-migration-q32.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.pdf>`_
   * - q32
     - LilyPond
     - `bird-im-migration-q32.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.ly>`_
   * - q32
     - MIDI
     - `bird-im-migration-q32.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.midi>`_
   * - q32
     - WAV
     - `bird-im-migration-q32.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.wav>`_

.. only:: html

   Listen
   ------

   q16
   ^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

   q32
   ^^^

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

Score Preview
-------------

q16
^^^

.. image:: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16-thumbnail.png
   :alt: First page preview of Bird Im-Migration q16
   :target: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q16.pdf
   :width: 50%

q32
^^^

.. image:: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32-thumbnail.png
   :alt: First page preview of Bird Im-Migration q32
   :target: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/bird-im-migration-q32.pdf
   :width: 50%

Source Materials
----------------

The package keeps its source materials inside the package data directory.

- ``src/bird_im_migration/data/DL_parkbirds.wav``
- ``src/bird_im_migration/data/DL_parkbirds_partials.txt``

The WAV file is the original recording.
The partials text file is the SPEAR analysis export that drives the score generation.

Analytical Premise
------------------

The analysis code focuses on a bird-like high-frequency band around ``4.5-6.0 kHz``.
That band is not meant to be a universal description of birdsong.
It is a practical filter for isolating the recurring chirp-like material in this recording.

The package keeps two layers of interpretation.
It can infer approximate candidate regions from the partials automatically.
It also preserves a curated set of bird regions that serve as the score timeline.

The currently curated regions are:

- ``Early birds``: ``0.6-1.9 s``
- ``Middle birds``: ``2.8-5.6 s``
- ``Strong middle/late birds``: ``7.3-9.1 s``
- ``Late birds``: ``10.8-13.9 s``

Transcription Strategy
----------------------

The package parses the SPEAR text file, filters for bird-like partials, quantizes onset material within each curated region, reduces each rhythmic bin to one or two salient pitches, and groups repeated bins into notated events.
Because the underlying sound is spectrally complex, the resulting notation sometimes uses small pitch clusters rather than a single line.

The package currently supports at least two useful quantization settings.

- ``q16`` for a 16th-note reduction
- ``q32`` for a 32nd-note reduction

Those quantization choices appear directly in the generated output stems so that both versions can coexist in the build directory.

Implementation
--------------

The analysis pipeline lives in ``bird_im_migration.analysis``.
The Abjad score builder lives in ``bird_im_migration.score``.
The command-line entry point lives in ``bird_im_migration.cli``.

The analysis module defines the spectral parsing and reduction logic:

.. literalinclude:: ../src/bird_im_migration/analysis.py
   :language: python
   :pyobject: quantize_region_pitches
   :caption: Quantizing bird-like partials into notated pitch bins.

The score module turns those reduced events into an Abjad score with region labels and score metadata:

.. literalinclude:: ../src/bird_im_migration/score.py
   :language: python
   :pyobject: build_lilypond_file
   :caption: Building the Bird Im-Migration LilyPond file from the partials analysis.

Build and Use
-------------

The repository build script now generates both quantized Bird Im-Migration variants alongside the other case studies.
The package can also be invoked directly:

.. code-block:: sh

   python -m bird_im_migration -o build --quantization 16 --pdf --midi
   python -m bird_im_migration -o build --quantization 32 --pdf --midi

This case study matters because it shows that the Abjad approach can also absorb analysis-driven material rather than only symbolic or algorithmically invented content.
It expands the technical report from score construction alone into the broader territory of spectral reduction and transcription as compositional method.
