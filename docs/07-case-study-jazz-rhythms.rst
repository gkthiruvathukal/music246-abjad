Case Study II: Jazz Rhythmic Patterns
=====================================

``Jazz Rhythmic Patterns`` is structurally smaller than the other projects, but it is useful for a technical report because it shows a different kind of musical abstraction.
Instead of generating a large score from many interlocking parameters, it defines a small library of one-measure rhythmic cells.
Those cells can be repeated, rendered, and reused in other contexts.

This package works as a compositional vocabulary source.
It also works as a simple example of how musical ideas can be encoded as reusable Python functions.
Each pattern returns a short list of notes and rests.
The score builder then places several staves one under another so the patterns can be compared visually.
The notation is now closer to what a jazz player would expect in a rhythm chart: a normal five-line staff, slash noteheads, and hits placed on the middle line.
That makes the page read less like abstract rhythmic study and more like practical ensemble notation.

Download
--------

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `jazz-rhythms.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.pdf>`_
   * - LilyPond
     - `jazz-rhythms.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.ly>`_
   * - MIDI
     - `jazz-rhythms.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.midi>`_
   * - WAV
     - Not published for this score

.. only:: html

   Listen
   ------

   .. note::

      A WAV player is not available for this score yet. Audio support for this case study is planned.

Score Preview
-------------

.. image:: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms-thumbnail.png
   :alt: First page preview of Jazz Rhythmic Patterns
   :target: https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/jazz-rhythms.pdf
   :width: 50%

The pattern functions are intentionally small:

.. literalinclude:: ../src/jazz_rhythm/rhythms.py
   :language: python
   :pyobject: charleston
   :caption: One of the reusable rhythm cells in the jazz rhythm package.

The score layer is equally direct:

.. literalinclude:: ../src/jazz_rhythm/score.py
   :language: python
   :pyobject: build_lilypond_file
   :caption: Assembly of the jazz rhythm comparison score.

This package matters because it shows that the repository does not only support finished scores and large generators.
It also supports smaller compositional tools.
It also shows that presentation matters.
The same rhythms read differently once they are shown in a chart-like notation style instead of a generic rhythm-only staff.
In a technical report, that helps show the full range of the codebase.
