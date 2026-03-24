Appendix A: Repository Map
==========================

The repository is organized around a small number of score packages, configuration files, and build helpers.

.. code-block:: text

   compositions-abjad/
   ├── configs/
   │   ├── algorithmic-piano-quartet-no1.toml
   │   └── algorithmic-piano-quartet-no2.toml
   ├── docs/
   ├── src/
   │   ├── modus_operandi_abjad/
   │   ├── jazz_rhythm/
   │   ├── algorithmic_piano_quartet_no1/
   │   ├── algorithmic_piano_quartet_no2/
   │   └── algorithmic/
   ├── build.sh
   ├── midi2wav.sh
   ├── pyproject.toml
   └── .github/workflows/build.yml

The top level is intentionally small.
Score packages live in ``src``.
Quartet configuration lives in ``configs``.
Build and release behavior lives at the top level and in the GitHub workflow file.
The ``docs`` directory now holds the technical report source.
