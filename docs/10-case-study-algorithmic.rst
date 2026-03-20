Case Study V: Algorithmic Scaffold
==================================

The ``algorithmic`` package is deliberately incomplete. It exists to hold the place for future work that has not yet become a full score package. In a technical report this may look minor, but it is worth including because it shows a normal pattern in research software. Infrastructure often appears before the final content that will use it.

Right now the package is only a stub. It can generate a placeholder score, run through the same CLI path as the other packages, and produce LilyPond, PDF, and MIDI outputs. That is enough to keep the project metadata, build script, and release workflow ready for future algorithmic material.

Download
--------

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `algorithmic.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.pdf>`_
   * - LilyPond
     - `algorithmic.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.ly>`_
   * - MIDI
     - `algorithmic.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/algorithmic.midi>`_
   * - WAV
     - Not published for this score

Listen
------

.. note::

   A WAV player is not available for this score yet. Audio support for this case study is planned.

The placeholder score code is intentionally small:

.. literalinclude:: ../src/algorithmic/score.py
   :language: python
   :pyobject: build_lilypond_file
   :caption: Placeholder score generation in the algorithmic scaffold package.

This section matters because the report is not only about finished compositions. It is also about building a technical environment that can support future composition work cleanly.
