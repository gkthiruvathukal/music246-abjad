Appendix C: Selected Code Listings
==================================

This appendix is reserved for code listings that are too long for the main body.
The main paper should use short excerpts when a small example is enough.
Longer listings belong here, where they can support reproducibility without breaking the flow of the argument.

One useful example is the second quartet chord builder, which contains much of the recent experimental work on left-hand and right-hand spacing:

.. literalinclude:: ../src/algorithmic_piano_quartet_no2/generator.py
   :language: python
   :pyobject: _build_piano_chord
   :caption: Full chord-construction function for Quartet No. 2.

Another useful example is the first quartet score assembly layer:

.. literalinclude:: ../src/algorithmic_piano_quartet/score.py
   :language: python
   :lines: 200-263
   :caption: Final score assembly for Quartet No. 1.
