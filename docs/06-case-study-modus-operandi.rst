Case Study I: Modus Operandi for Piano
======================================

``Modus Operandi for Piano`` is the most fixed composition in the repository. It is a three-movement solo piano work organized around three modes on F: Dorian, Phrygian, and Lydian. Each movement has a clear tempo, meter, and registral profile. The right hand carries the main line, and the left hand provides a slower accompaniment. Even though the score is produced with Abjad and LilyPond, the work itself is not built as an open-ended generator. It is closer to a score written in code than to a random composition system.

This package is important because it shows that the repository is not limited to generative experiments. It can also support a more traditional compositional process in which the musical material is already decided, but the score is still generated and rendered programmatically. That gives the project a wider scope. It is not only about algorithmic output. It is also about representing finished musical decisions cleanly in code.

The implementation reflects that role. The CLI writes a LilyPond file, compiles it, and then merges the per-movement MIDI files that LilyPond emits. This extra step is necessary because the piece is built from multiple score blocks. The WAV render is then handled through a separate script that downloads and caches a piano SoundFont on first use.

Download
--------

.. list-table::
   :header-rows: 1

   * - Format
     - Link
   * - PDF
     - `modus-operandi-abjad.pdf <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.pdf>`_
   * - LilyPond
     - `modus-operandi-abjad.ly <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.ly>`_
   * - MIDI
     - `modus-operandi-abjad.midi <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.midi>`_
   * - WAV
     - `modus-operandi-abjad.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.wav>`_

Listen
------

.. only:: html

   .. raw:: html

      <audio controls preload="none">
        <source src="https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.wav" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

.. only:: not html

   Audio:
   `modus-operandi-abjad.wav <https://github.com/gkthiruvathukal/compositions-abjad/releases/latest/download/modus-operandi-abjad.wav>`_

The movement-building code is direct enough to read almost like score notation. It is still too long to reproduce in full in the body of the paper, so only the opening of the movement is shown here:

.. literalinclude:: ../src/modus_operandi_abjad/score.py
   :language: python
   :lines: 56-104
   :caption: Opening construction pattern for the first movement of Modus Operandi.

That directness is one of the useful contrasts in the report. ``Modus Operandi`` shows what the system looks like when the composition is fixed. The quartet packages show what the same repository looks like when the composition logic is open to controlled variation.
