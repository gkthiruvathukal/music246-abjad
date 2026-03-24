Common Pipeline
===============

The common pipeline in this repository has five steps.
First, a package defines musical content either directly in code or through a mix of code and configuration.
Second, that material is assembled into Abjad objects.
Third, the Abjad representation is serialized into LilyPond.
Fourth, LilyPond compiles the score into PDF and MIDI.
Fifth, optional audio rendering converts MIDI into WAV.
This last step is not required for score production, but it is part of the normal build path for the finished works and the quartet studies.

The fixed-score packages and the generative packages share the same general output pipeline.
They differ mainly in how the musical material is created.
``modus_operandi_abjad`` and parts of ``jazz_rhythm`` are more direct.
The quartet packages are more explicitly generative.
They load configuration, turn it into generation rules, create event streams on a quantized grid, and then convert those events into notation.

Reproducibility matters more in the quartet packages than in the fixed-score packages.
The quartet generators expose a random seed through configuration.
That means a result can be regenerated as long as the code and config stay the same.
Output filenames can also include measures, tempo, seed, and timestamp, which makes it easy to track experimental runs.

The quartet audio path is a good example of the pipeline becoming more specialized when the musical needs require it.
A single piano SoundFont is not enough for a quartet, and a single orchestral SoundFont does not give the best piano result.
The system therefore renders the piano layer and the string layer separately and combines them afterward.
The CLI is still simple from the outside, but the internal render path is more careful.

The end of the main quartet CLI shows this in two steps.
First, it decides which outputs LilyPond needs to compile:

.. literalinclude:: ../src/algorithmic_piano_quartet_no1/cli.py
   :language: python
   :start-after: docs: begin quartet-output-compilation
   :end-before: docs: end quartet-output-compilation
   :caption: Output compilation decisions in the first quartet CLI.

Then it decides how WAV rendering should happen once the MIDI file exists:

.. literalinclude:: ../src/algorithmic_piano_quartet_no1/cli.py
   :language: python
   :start-after: docs: begin quartet-wav-rendering
   :end-before: docs: end quartet-wav-rendering
   :caption: WAV rendering choices in the first quartet CLI.
