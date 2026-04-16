"""Score construction for an activist art song scaffold."""

import abjad

TITLE = "Art Song"
COMPOSER = "George K. Thiruvathukal"
SUBTITLE = "Activist song scaffold for voice and piano"


def _add_opening_markup(staff: abjad.Staff, text: str) -> None:
    first_leaf = abjad.select.leaf(staff, 0)
    if first_leaf is None:
        return
    abjad.attach(
        abjad.Markup(rf'\markup \italic "{text}"'),
        first_leaf,
        direction=abjad.UP,
    )


def build_lilypond_file():
    """Build a placeholder LilyPond file for future art-song work."""
    voice_staff = abjad.Staff(name="Voice")
    voice_staff.append(abjad.Rest("r1"))
    voice_leaf = abjad.select.leaf(voice_staff, 0)
    abjad.attach(abjad.Clef("treble"), voice_leaf)
    abjad.attach(abjad.TimeSignature((4, 4)), voice_leaf)
    abjad.attach(abjad.InstrumentName(r"\markup Voice"), voice_leaf)
    abjad.attach(abjad.ShortInstrumentName(r"\markup V."), voice_leaf)
    _add_opening_markup(
        voice_staff,
        "Text source placeholder: Lincoln Gettysburg Address or Kennedy moon speech.",
    )

    piano_rh = abjad.Staff(name="Piano_RH")
    piano_rh.append(abjad.Rest("r1"))
    piano_rh_leaf = abjad.select.leaf(piano_rh, 0)
    abjad.attach(abjad.Clef("treble"), piano_rh_leaf)

    piano_lh = abjad.Staff(name="Piano_LH")
    piano_lh.append(abjad.Rest("r1"))
    piano_lh_leaf = abjad.select.leaf(piano_lh, 0)
    abjad.attach(abjad.Clef("bass"), piano_lh_leaf)

    piano_group = abjad.StaffGroup(
        [piano_rh, piano_lh],
        lilypond_type="PianoStaff",
        name="Piano",
    )
    abjad.attach(abjad.InstrumentName(r"\markup Piano"), piano_rh_leaf)
    abjad.attach(abjad.ShortInstrumentName(r"\markup Pno."), piano_rh_leaf)
    _add_opening_markup(
        piano_rh,
        "Rock/folk protest-song direction with optional generative variants.",
    )

    score = abjad.Score([voice_staff, piano_group], name="Score")

    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{TITLE}"')
    header_block.items.append(rf'subtitle = "{SUBTITLE}"')
    header_block.items.append(rf'composer = "{COMPOSER}"')
    header_block.items.append(r"tagline = ##f")

    layout_block = abjad.Block(name="layout")
    midi_block = abjad.Block(name="midi")

    score_block = abjad.Block(name="score")
    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    return abjad.LilyPondFile(items=[header_block, score_block])
