Background and Tooling
======================

The project uses Abjad [#abjad]_ as the Python [#python]_ layer for score construction. Abjad does not try to be a notation editor. Instead, it gives direct control over score objects such as staves, voices, measures, articulations, dynamics, tempo marks, and other notation features. That makes it well suited for work where the score is built from algorithms or data structures rather than from mouse-driven editing.

LilyPond [#lilypond]_ is used as the engraving backend. Abjad emits LilyPond source, and LilyPond then produces the engraved PDF and MIDI output. This separation is important. Python handles the compositional and structural side of the work, while LilyPond handles the engraving layer. That keeps the implementation clean and makes it easy to inspect the generated ``.ly`` files when debugging or refining notation.

Audio rendering is handled separately from score engraving. For the solo piano work, MIDI can be rendered with FluidSynth and a cached piano SoundFont. For the quartet work, the render path is more involved because the best available piano and string sounds come from different SoundFonts. The quartet system therefore renders piano and strings separately and combines the results with ``ffmpeg``. This gives better output than forcing all instruments through a single SoundFont.

The broader tooling choice is pragmatic. Python is the control layer. Abjad is the score API. LilyPond is the engraver. FluidSynth and ``ffmpeg`` fill in the audio path. Shell and GitHub Actions provide local and CI automation. None of these tools is unusual on its own. The value comes from using them together in one repeatable composition workflow.

.. [#python] Python Software Foundation, `Python <https://www.python.org/>`_.
.. [#abjad] Abjad Project, `Abjad documentation <https://abjad.github.io/>`_.
.. [#lilypond] LilyPond Developers, `LilyPond music engraving <https://lilypond.org/>`_.
