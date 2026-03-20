System Architecture
===================

The repository is organized as a multi-package Python project under ``../src``. Each major score path is implemented as its own package with a CLI entry point. This is a better fit than a single monolithic script. It keeps each score family readable, allows each package to evolve at its own pace, and makes the build process consistent across the repository.

There are five active package paths. ``modus_operandi_abjad`` contains a fixed three-movement piano work. ``jazz_rhythm`` contains reusable rhythmic studies. ``algorithmic_piano_quartet`` contains the first config-driven quartet generator. ``algorithmic_piano_quartet_no2`` contains the forked and more experimental second quartet generator. ``algorithmic`` is a placeholder package for future work. The package entry points are defined in ``../pyproject.toml`` and exposed both as ``python -m ...`` module invocations and as installed console scripts.

Within each score package, the code usually separates into three layers. The CLI layer handles arguments, output selection, and compilation. The generation layer defines musical material or event logic. The score layer turns that material into Abjad objects and then into LilyPond source. Quartet packages add a fourth layer for configuration loading and a fifth layer for SoundFont handling.

The architecture also separates stable work from exploratory work. ``Algo Rhythms Quartet No. 1`` stays fixed as a proof-of-concept score. ``Algorithmic Piano Quartet No. 2`` is allowed to diverge. This is a software architecture decision, but it is also a compositional one. It lets the repository preserve finished work without blocking further musical experiments.

One small but important detail is the use of entry points instead of one-off scripts:

.. literalinclude:: ../pyproject.toml
   :language: toml
   :lines: 16-21
   :caption: Console script entry points defined in the project metadata.
