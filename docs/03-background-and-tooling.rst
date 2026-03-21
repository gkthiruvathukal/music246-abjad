Background and Tooling
======================

The project uses Abjad [#abjad]_ as the Python [#python]_ layer for score construction.
Abjad does not try to be a notation editor.
Instead, it gives direct control over score objects such as staves, voices, measures, articulations, dynamics, tempo marks, and other notation features.
That makes it well suited for work where the score is built from algorithms or data structures rather than from mouse-driven editing.

LilyPond [#lilypond]_ is used as the engraving backend.
Abjad emits LilyPond source, and LilyPond then produces the engraved PDF and MIDI output.
This separation is important.
Python handles the compositional and structural side of the work, while LilyPond handles the engraving layer.
That keeps the implementation clean and makes it easy to inspect the generated ``.ly`` files when debugging or refining notation.

Audio rendering is handled separately from score engraving.
For the solo piano work, MIDI can be rendered with FluidSynth and the Salamander Grand Piano SoundFont [#salamander]_.
For the quartet work, the render path is more involved because the best available piano and string sounds come from different SoundFonts.
The system uses Salamander Grand Piano for the piano part and Aegean Symphonic Orchestra [#aegean]_ for violin, viola, and cello.
The quartet system therefore renders piano and strings separately and combines the results with ``ffmpeg``.
This gives better output than forcing all instruments through a single SoundFont, and it makes the generated WAV output sound closer to a plausible performance.

The broader tooling choice is pragmatic as opposed to academic:

- Python is the control layer.
- Abjad is the score API.
- LilyPond is the engraver.
- FluidSynth and ``ffmpeg`` fill in the audio path.
- The Unix/Linux shell and GitHub Actions provide local and CI automation.

The value comes from using them together in one repeatable composition workflow.
This workflow may or may not work for you but works well for me as my present course expects music notation as part of the composition process.

.. [#python] Python Software Foundation, `Python <https://www.python.org/>`_.
.. [#abjad] Abjad Project, `Abjad documentation <https://abjad.github.io/>`_.
.. [#lilypond] LilyPond Developers, `LilyPond music engraving <https://lilypond.org/>`_.
.. [#salamander] SFZ Instruments, `Salamander Grand Piano <https://sfzinstruments.github.io/pianos/salamander>`_.
.. [#aegean] HED Sounds, `Aegean Symphonic Orchestra <https://sites.google.com/view/hed-sounds/aegean-symphonic-orchestra>`_.
