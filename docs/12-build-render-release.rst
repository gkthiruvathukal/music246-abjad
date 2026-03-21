Build, Render, and Release Engineering
======================================

The repository treats build and release behavior as part of the system, not as an afterthought.
Local builds run through ``../build.sh``.
That script creates or reuses a virtual environment, installs the project in editable mode, checks for required tools, and then builds each score path in turn.
When audio tools are available, it also renders WAV output.
This matters because it gives one repeatable command for the full local workflow.

Continuous integration mirrors the same idea.
GitHub Actions builds the score packages, uploads artifacts, and creates tagged releases.
The repository is therefore able to move from source code to a published release without a separate manual packaging process.
That makes the technical report stronger because the output pipeline is not hypothetical.
It is already in regular use.

The quartet render path is the most complex part of this build layer.
The system downloads and caches SoundFonts when needed.
It renders piano and string layers separately.
It uses FluidSynth for synthesis and ``ffmpeg`` for the final mix.
This is a concrete example of a musical requirement driving a more careful software design.

This build-first design also improves debugging.
When a score changes, the same automated path can regenerate notation and audio.
That shortens the loop between compositional change and technical verification.
