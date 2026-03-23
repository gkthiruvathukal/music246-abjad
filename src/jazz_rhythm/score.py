"""Score construction for jazz rhythm studies."""

import abjad

from . import rhythms

TITLE = "Jazz Rhythmic Patterns using Abjad Python"
COMPOSER = "George K. Thiruvathukal"


def _style_as_jazz_hits(staff):
    """Format one staff as a five-line jazz hits staff."""
    literal = abjad.LilyPondLiteral(
        r"""
        \omit Clef
        \override NoteHead.style = #'slash
        \override Stem.direction = #up
        \override Rest.staff-position = #0
        """,
        site="before",
    )
    first_leaf = abjad.select.leaf(staff, 0)
    if first_leaf is not None:
        abjad.attach(literal, first_leaf)


def _make_staff(name, markup, rhythm_maker, measures=4):
    """Build one rhythmic staff showing repeated instances of a pattern."""
    staff = abjad.Staff(name=name)
    leaves = []
    for _ in range(measures):
        leaves.extend(rhythm_maker())
    staff.extend(leaves)
    if leaves:
        abjad.attach(abjad.TimeSignature((4, 4)), leaves[0])
        abjad.attach(abjad.Markup(rf'\markup "{markup}"'), leaves[0], direction=abjad.UP)
    _style_as_jazz_hits(staff)
    return staff


def _make_lyric_staff(name, markup, rhythm_maker, lyric_text, measures=4):
    """Build one rhythmic staff with a lyric line aligned to its notes."""
    staff = _make_staff(name, markup, rhythm_maker, measures=measures)
    lyric_line = " ".join([lyric_text] * measures)
    abjad.attach(
        abjad.LilyPondLiteral(
            rf"\addlyrics {{ \override LyricText.font-size = #-1 {lyric_line} }}",
            site="after",
        ),
        staff,
    )
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
    score.append(
        _make_lyric_staff(
            "Swing Two Four Staff",
            "Swing on 2 and 4",
            rhythms.swing_two_four,
            "doodle LA doodle LA",
        )
    )

    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{TITLE}"')
    header_block.items.append(rf'composer = "{COMPOSER}"')
    header_block.items.append(r"tagline = ##f")

    layout_block = abjad.Block(name="layout")
    layout_block.items.append(r"indent = 2.0\cm")
    layout_block.items.append(
        r"""
        \context {
            \Score
            \override VerticalAxisGroup.default-staff-staff-spacing.basic-distance = #14
            \override VerticalAxisGroup.default-staff-staff-spacing.minimum-distance = #10
            \override VerticalAxisGroup.default-staff-staff-spacing.padding = #3
        }
        """
    )

    midi_block = abjad.Block(name="midi")

    score_block = abjad.Block(name="score")
    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    return abjad.LilyPondFile(items=[header_block, score_block])
