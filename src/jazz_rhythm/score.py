"""Score construction for jazz rhythm studies."""

import abjad

from . import rhythms

TITLE = "Jazz Rhythmic Patterns using Abjad Python"
COMPOSER = "George K. Thiruvathukal"

def _make_staff(name, markup, rhythm_maker, measures=4):
    """Build one rhythmic staff showing repeated instances of a pattern."""
    staff = abjad.Staff(lilypond_type="RhythmicStaff", name=name)
    leaves = []
    for _ in range(measures):
        leaves.extend(rhythm_maker())
    staff.extend(leaves)
    if leaves:
        abjad.attach(abjad.TimeSignature((4, 4)), leaves[0])
        abjad.attach(abjad.Markup(rf'\markup "{markup}"'), leaves[0], direction=abjad.UP)
    return staff


def build_lilypond_file():
    """Build the LilyPond file for the jazz rhythm score."""
    score = abjad.Score([], name="Score")
    score.append(_make_staff("Charleston Staff", "Charleston", rhythms.charleston))
    score.append(
        _make_staff(
            "Charleston Extended Staff",
            "Charleston Extended (and of 4)",
            rhythms.charleston_extended,
        )
    )
    score.append(
        _make_staff(
            "Anticipation Staff",
            "Anticipation (push to 1)",
            rhythms.anticipation,
        )
    )
    score.append(_make_staff("Two Beat Staff", "Two Beat Comping", rhythms.two_beat))
    score.append(
        _make_staff(
            "Syncopated Staff",
            "Syncopated (off-beats)",
            rhythms.syncopated,
        )
    )

    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{TITLE}"')
    header_block.items.append(rf'composer = "{COMPOSER}"')
    header_block.items.append(r"tagline = ##f")

    layout_block = abjad.Block(name="layout")
    layout_block.items.append(r"indent = 2.0\cm")

    midi_block = abjad.Block(name="midi")

    score_block = abjad.Block(name="score")
    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    return abjad.LilyPondFile(items=[header_block, score_block])
