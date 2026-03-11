"""Reusable jazz rhythm cells."""

import abjad


def charleston():
    """Return a one-measure Charleston rhythm."""
    return [
        abjad.Note("c'4."),
        abjad.Note("c'8"),
        abjad.Rest("r2"),
    ]


def charleston_extended():
    """Return a Charleston rhythm with a push on the and of 4."""
    return [
        abjad.Note("c'4."),
        abjad.Note("c'8"),
        abjad.Rest("r4"),
        abjad.Rest("r8"),
        abjad.Note("c'8"),
    ]


def anticipation():
    """Return a one-measure anticipation rhythm."""
    return [
        abjad.Rest("r2."),
        abjad.Rest("r8"),
        abjad.Note("c'8"),
    ]


def two_beat():
    """Return a one-measure two-beat comping rhythm."""
    return [
        abjad.Rest("r4"),
        abjad.Note("c'4"),
        abjad.Rest("r4"),
        abjad.Note("c'4"),
    ]


def syncopated():
    """Return a one-measure syncopated rhythm."""
    return [
        abjad.Rest("r8"),
        abjad.Note("c'8"),
        abjad.Rest("r8"),
        abjad.Note("c'8"),
        abjad.Rest("r2"),
    ]
