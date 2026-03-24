Configuration and Parameterization
==================================

Configuration is central to the quartet work.
The repository uses TOML because it is readable, easy to version, and structured enough to separate different kinds of choices.
In the quartet packages, configuration controls three main areas.
The first is output and metadata.
The second is rendering.
The third is musical generation.

The output section controls naming and filename construction.
The render section controls SoundFonts and sample rate.
The generation section controls measure count, note and rest durations, leap bounds, density, tempo, and seed.
The materials section defines the pitch-class pool.
The parts section defines instrumentation, ranges, MIDI channel assignments, clefs, and roles.

This design is important for two reasons.
First, it makes generated scores reproducible.
Second, it turns the quartet packages into research interfaces rather than fixed scripts.
The config is the place where an experiment can be defined, rerun, and compared.

No. 2 extends this model rather than replacing it.
The second quartet adds hand-specific piano parameters, separate piano occupancy, and more detailed chord controls.
This is one of the best examples in the project of how technical design and musical design work together.

The first quartet config is compact enough to show the overall model:

.. literalinclude:: ../configs/algorithmic-piano-quartet-no1.toml
   :language: toml
   :lines: 1-63
   :caption: Core configuration for Quartet No. 1.

The second quartet config shows how the same structure can grow to support more detailed piano behavior:

.. literalinclude:: ../configs/algorithmic-piano-quartet-no2.toml
   :language: toml
   :lines: 1-40
   :caption: Extended generation controls in Quartet No. 2.
