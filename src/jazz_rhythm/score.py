import abjad


def make_rhythm_staff(rhythm_name, rhythm_container):
    voice = abjad.Voice(rhythm_container, name=f"{rhythm_name.replace(' ', '')}Voice")
    staff = abjad.Staff([voice], name=f"{rhythm_name.replace(' ', '')}Staff")
    abjad.attach(abjad.Clef("percussion"), staff)
    abjad.attach(abjad.TimeSignature((4, 4)), staff)
    abjad.attach(
        abjad.MetronomeMark(
            reference_duration=abjad.Duration(1, 4),
            units_per_minute=120,
            textual_indication=rhythm_name,
        ),
        staff,
    )
    abjad.override(staff).Staff.explicitClefVisibility = True
    return staff


def charleston():
    """
    Returns a one-measure Charleston rhythm (dotted quarter + eighth).
    """
    return abjad.Container(
        [
            abjad.Note("c'4."),
            abjad.Note("c'8"),
            abjad.Rest("r2"),
        ]
    )


def charleston_extended():
    """
    Returns a one-measure Charleston rhythm (dotted quarter + eighth) plus a push on the 'and' of 4.
    """
    return abjad.Container(
        [
            abjad.Note("c'4."),  # Beat 1 + 2 (start)
            abjad.Note("c'8"),  # Beat 2 'and'
            abjad.Rest("r4"),  # Beat 3
            abjad.Rest("r8"),  # Beat 4
            abjad.Note("c'8"),  # Beat 4 'and'
        ]
    )


def anticipation():
    """
    Returns a one-measure rhythm with an anticipation on the 'and' of beat 4.
    """
    return abjad.Container(
        [
            abjad.Rest("r2."),
            abjad.Rest("r8"),
            abjad.Note("c'8"),
        ]
    )


def two_beat():
    """
    Returns a one-measure rhythm with quarter notes on beats 2 and 4.
    """
    return abjad.Container(
        [
            abjad.Rest("r4"),
            abjad.Note("c'4"),
            abjad.Rest("r4"),
            abjad.Note("c'4"),
        ]
    )


def syncopated():
    """
    Returns a one-measure syncopated rhythm (off-beats on 1 and 2).
    """
    return abjad.Container(
        [
            abjad.Rest("r8"),
            abjad.Note("c'8"),
            abjad.Rest("r8"),
            abjad.Note("c'8"),
            abjad.Rest("r2"),
        ]
    )


def build_lilypond_file():
    """Assemble the full LilyPondFile from all jazz rhythms."""
    header = abjad.Block("header")
    header.items.append(r'title = "Jazz Rhythm Patterns"')
    header.items.append(r'composer = "Various"')
    header.items.append(r'subtitle = "Common Jazz Rhythms"')
    header.items.append(r"tagline = ##f")

    # Create individual rhythm staves
    charleston_staff = make_rhythm_staff("Charleston", charleston())
    charleston_extended_staff = make_rhythm_staff(
        "Charleston Extended", charleston_extended()
    )
    anticipation_staff = make_rhythm_staff("Anticipation", anticipation())
    two_beat_staff = make_rhythm_staff("Two Beat", two_beat())
    syncopated_staff = make_rhythm_staff("Syncopated", syncopated())

    return abjad.LilyPondFile(
        items=[
            header,
            # abjad.GlobalContext(),  # Ensure global context for page breaks and other settings
            charleston_staff,
            r"\pageBreak",
            charleston_extended_staff,
            r"\pageBreak",
            anticipation_staff,
            r"\pageBreak",
            two_beat_staff,
            r"\pageBreak",
            syncopated_staff,
        ],
    )
