import abjad


def charleston():
    """
    Returns a one-measure Charleston rhythm (dotted quarter + eighth).
    """
    return [
        abjad.Note("c'4."),
        abjad.Note("c'8"),
        abjad.Rest("r2"),
    ]


def charleston_extended():
    """
    Returns a one-measure Charleston rhythm (dotted quarter + eighth) plus a push on the 'and' of 4.
    """
    return [
        abjad.Note("c'4."),  # Beat 1 + 2 (start)
        abjad.Note("c'8"),  # Beat 2 'and'
        abjad.Rest("r4"),  # Beat 3
        abjad.Rest("r8"),  # Beat 4
        abjad.Note("c'8"),  # Beat 4 'and'
    ]


def anticipation():
    """
    Returns a one-measure rhythm with an anticipation on the 'and' of beat 4.
    """
    return [
        abjad.Rest("r2."),
        abjad.Rest("r8"),
        abjad.Note("c'8"),
    ]


def two_beat():
    """
    Returns a one-measure rhythm with quarter notes on beats 2 and 4.
    """
    return [
        abjad.Rest("r4"),
        abjad.Note("c'4"),
        abjad.Rest("r4"),
        abjad.Note("c'4"),
    ]


def syncopated():
    """
    Returns a one-measure syncopated rhythm (off-beats on 1 and 2).
    """
    return [
        abjad.Rest("r8"),
        abjad.Note("c'8"),
        abjad.Rest("r8"),
        abjad.Note("c'8"),
        abjad.Rest("r2"),
    ]
