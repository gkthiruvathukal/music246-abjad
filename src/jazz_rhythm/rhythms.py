"""Reusable jazz rhythm cells."""

import abjad


def charleston():
    """Return a one-measure Charleston rhythm."""
    return [
        abjad.Note("b'4."),
        abjad.Note("b'8"),
        abjad.Rest("r4"),
        abjad.Rest("r4"),
    ]


def charleston_extended():
    """Return a Charleston rhythm with a push on the and of 4."""
    return [
        abjad.Note("b'4."),
        abjad.Note("b'8"),
        abjad.Rest("r4"),
        abjad.Rest("r8"),
        abjad.Note("b'8"),
    ]


def anticipation():
    """Return a one-measure anticipation rhythm."""
    return [
        abjad.Rest("r4"),
        abjad.Rest("r4"),
        abjad.Rest("r4"),
        abjad.Rest("r8"),
        abjad.Note("b'8"),
    ]


def two_beat():
    """Return a one-measure two-beat comping rhythm."""
    return [
        abjad.Rest("r4"),
        abjad.Note("b'4"),
        abjad.Rest("r4"),
        abjad.Note("b'4"),
    ]


def syncopated():
    """Return a one-measure syncopated rhythm."""
    return [
        abjad.Rest("r8"),
        abjad.Note("b'8"),
        abjad.Rest("r8"),
        abjad.Note("b'8"),
        abjad.Rest("r4"),
        abjad.Rest("r4"),
    ]


def swing_two_four():
    """Return a swung one-measure pattern on beats 2 and 4."""
    return [
        abjad.Rest("r4"),
        abjad.Tuplet("3:2", [abjad.Note("b'4"), abjad.Note("b'8")]),
        abjad.Rest("r4"),
        abjad.Tuplet("3:2", [abjad.Note("b'4"), abjad.Note("b'8")]),
    ]
