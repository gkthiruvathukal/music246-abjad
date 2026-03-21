Introduction
============

This repository began from a personal shift as much as a technical one.
I am a professor of computer science at Loyola University Chicago and have been on the faculty there since 2001.
After many years focused on teaching, research, and administration, including the intense work of serving (in my present life) as department chairperson, I returned to music study in a more serious way and began pursuing postbaccalaureate work in music at the same institution.
This repository is one result of that return.

The immediate context was MUSC 246, a composition course at Loyola taught by `Dongryul Lee <https://www.luc.edu/dfpa/facultyandstaffdirectory/profiles/dongryulleedma.shtml>`_, Assistant Professor of Music and Coordinator of Theory and Composition.
The course covered a wide range of compositional styles and methods.
That breadth was exciting, but it also raised a practical question: how should I write music in a way that fits both my musical goals and my habits as a computer scientist?

My first attempts used standard WYSIWYG notation software.
Dorico is a strong system, and it clearly improves on Finale in many ways, but I still found myself fighting the interface.
I wanted a workflow closer to plain text, version control, and reproducible builds.
That led me first to LilyPond, which has a long history as a GNU project, and then to Python with Abjad as a way to generate LilyPond programmatically.

Most music software assumes that composition begins in a notation editor or a digital audio workstation.
This project starts from a different assumption.
It treats code as a first-class compositional medium.
That choice changes both the workflow and the kinds of musical questions that can be asked.
When a score is built in code, the same source can define pitch material, rhythm, instrumentation, notation details, rendering choices, and release artifacts.
It also becomes much easier to reproduce a result, rerun it with controlled changes, or compare two closely related systems.

This repository was built around that idea.
It uses Python, Abjad, and LilyPond to move from compositional logic to engraved score.
It also uses shell scripts and GitHub Actions so that the same scores can be built locally and in continuous integration.
The result is a repository that functions as both a set of compositions and a software system.

The artistic motivation shows most clearly in the quartet work.
``Algo Rhythms Quartet No. 1`` is a proof of concept for a larger planned system.
``Algorithmic Piano Quartet No. 2`` begins from the same base but is allowed to change more freely so that new musical ideas can be tested without rewriting the original piece.
This makes the repository useful in two ways at once.
It preserves completed work, and it gives a controlled place for technical and musical experiments.

The goal of this report is to describe that combined system in a form closer to a technical paper than to a project README.
The report focuses on architecture, generation methods, rendering, and release workflow.
It also discusses each current score in enough detail to show how the musical ideas and the code design fit together.

About the Author
-----------------

*George K.
Thiruvathukal, PhD* is *Professor and Chairperson* in the `Department of Computer Science <https://www.luc.edu/cs/>`__ at `Loyola University Chicago <https://www.luc.edu/>`__.
He is also a *Visiting Computer Scientist* at `Argonne National Laboratory <https://www.anl.gov/>`__ in the `Leadership Computing Facility (ALCF) <https://www.alcf.anl.gov/>`__.
As of January 2026, he is a *Postbaccalaureate Student* and pianist in `Music/Jazz at Loyola <https://www.luc.edu/music/>`__ at `Loyola University Chicago <https://www.luc.edu/>`__, hoping against all odds to become a serious jazz musician and composer.
Wish him (me) luck!

For more information, please see `gkt.sh <https://gkt.sh>`__.


