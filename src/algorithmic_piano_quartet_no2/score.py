"""Abjad score assembly for algorithmic piano quartet No. 2."""

from __future__ import annotations

import abjad
from fractions import Fraction

from .generator import Event, Piece, VoiceMaterial


PITCH_CLASS_NAMES = {
    0: "c",
    1: "df",
    2: "d",
    3: "ef",
    4: "e",
    5: "f",
    6: "gf",
    7: "g",
    8: "af",
    9: "a",
    10: "bf",
    11: "b",
}

OTTAVA_THRESHOLDS = {
    "violin": {"up": 88, "down": None},
    "viola": {"up": 79, "down": 48},
    "cello": {"up": 67, "down": 35},
    "piano_rh": {"up": 84, "down": 55},
    "piano_lh": {"up": 65, "down": 35},
}


def _midi_to_pitch_name(midi_note: int) -> str:
    pitch_class = PITCH_CLASS_NAMES[midi_note % 12]
    octave = midi_note // 12 - 1
    if octave >= 4:
        octave_marks = "'" * (octave - 3)
    else:
        octave_marks = "," * (3 - octave)
    return f"{pitch_class}{octave_marks}"


def _make_leaf(event: Event):
    if event.pitches is None:
        pitch_lists = [[]]
    else:
        pitch_lists = [[abjad.NamedPitch(_midi_to_pitch_name(pitch)) for pitch in event.pitches]]
    leaves = abjad.makers.make_leaves(
        pitch_lists,
        [abjad.Duration(event.duration_quanta, 16)],
    )
    return leaves


def _ottava_state_for_pitch(staff_id: str, pitches: tuple[int, ...] | None) -> int:
    if pitches is None:
        return 0
    thresholds = OTTAVA_THRESHOLDS.get(staff_id)
    if not thresholds:
        return 0
    highest_pitch = max(pitches)
    lowest_pitch = min(pitches)
    if thresholds["up"] is not None and highest_pitch >= thresholds["up"] + 12:
        return 2
    if thresholds["up"] is not None and highest_pitch >= thresholds["up"]:
        return 1
    if thresholds["down"] is not None and lowest_pitch <= thresholds["down"]:
        return -1
    return 0


def _apply_ottava(staff: abjad.Staff, voice_material: VoiceMaterial) -> None:
    leaves = list(abjad.select.leaves(staff))
    events = list(voice_material.events)
    active_state = 0
    active_start = None
    active_stop = None

    for leaf, event in zip(leaves, events):
        state = _ottava_state_for_pitch(voice_material.staff_id, event.pitches)
        if state == active_state:
            if state != 0:
                active_stop = leaf
            continue
        if active_state != 0 and active_start is not None and active_stop is not None:
            abjad.attach(abjad.Ottava(n=active_state), active_start)
            abjad.attach(abjad.Ottava(n=0, site="after"), active_stop)
        active_state = state
        if state != 0:
            active_start = leaf
            active_stop = leaf
        else:
            active_start = None
            active_stop = None

    if active_state != 0 and active_start is not None and active_stop is not None:
        abjad.attach(abjad.Ottava(n=active_state), active_start)
        abjad.attach(abjad.Ottava(n=0, site="after"), active_stop)


def _voice_to_staff(voice_material: VoiceMaterial, piece: Piece) -> abjad.Staff:
    voice = abjad.Voice(name=f"{voice_material.staff_id}_voice")
    event_iter = iter(voice_material.events)
    current = next(event_iter, None)

    for measure_index in range(piece.measures):
        container = abjad.Container()
        measure_start = measure_index * piece.measure_quanta
        measure_stop = measure_start + piece.measure_quanta
        while current is not None and current.start_quantum < measure_stop:
            container.extend(_make_leaf(current))
            current = next(event_iter, None)
        voice.append(container)

    staff = abjad.Staff([voice], name=voice_material.staff_id)
    abjad.attach(abjad.Clef(voice_material.clef), abjad.select.leaf(staff, 0))
    abjad.attach(
        abjad.TimeSignature(piece.time_signature),
        abjad.select.leaf(staff, 0),
    )
    abjad.setting(staff).midiInstrument = rf'"{voice_material.midi_instrument}"'
    _apply_ottava(staff, voice_material)
    return staff


def _pitched_leaves(component) -> list:
    return [
        leaf
        for leaf in abjad.select.leaves(component)
        if isinstance(leaf, (abjad.Note, abjad.Chord))
    ]


def _apply_staff_dynamics(staff: abjad.Staff, piece: Piece, opening: str) -> None:
    pitched = _pitched_leaves(staff)
    if not pitched:
        return

    first_leaf = pitched[0]
    abjad.attach(abjad.Dynamic(opening), first_leaf)

    halfway_measure_index = max(piece.measures // 2, 1)
    halfway_offset = abjad.Offset(Fraction(halfway_measure_index * piece.measure_quanta, 16))
    later_pitched = [
        leaf for leaf in pitched if abjad.get.timespan(leaf).start_offset >= halfway_offset
    ]
    if later_pitched:
        abjad.attach(abjad.Dynamic("mf"), later_pitched[0])


def _apply_dynamics(
    violin_staff: abjad.Staff,
    viola_staff: abjad.Staff,
    cello_staff: abjad.Staff,
    piano_rh_staff: abjad.Staff,
    piano_lh_staff: abjad.Staff,
    piece: Piece,
) -> None:
    _apply_staff_dynamics(violin_staff, piece, "mp")
    _apply_staff_dynamics(viola_staff, piece, "mp")
    _apply_staff_dynamics(cello_staff, piece, "p")
    _apply_staff_dynamics(piano_rh_staff, piece, "mp")
    _apply_staff_dynamics(piano_lh_staff, piece, "p")


def _apply_ending(score: abjad.Score, piece: Piece) -> None:
    all_pitched = _pitched_leaves(score)
    if not all_pitched:
        return

    penultimate_measure_index = max(piece.measures - 2, 0)
    start_offset = abjad.Offset(Fraction(penultimate_measure_index * piece.measure_quanta, 16))
    ending_pitched = [
        leaf
        for leaf in all_pitched
        if abjad.get.timespan(leaf).start_offset >= start_offset
    ]
    if not ending_pitched:
        ending_pitched = [all_pitched[-1]]

    first_ending_leaf = ending_pitched[0]
    last_ending_leaf = ending_pitched[-1]
    abjad.attach(abjad.Dynamic("p"), first_ending_leaf)
    abjad.attach(
        abjad.Markup(r"\markup \italic morendo"),
        first_ending_leaf,
        direction=abjad.UP,
    )
    abjad.attach(abjad.Dynamic("ppp"), last_ending_leaf)

    final_leaf = abjad.select.leaf(score, -1)
    abjad.attach(abjad.BarLine("|."), final_leaf)


def _quote_markup_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _build_generation_note_markup(piece: Piece) -> abjad.Markup | None:
    if not piece.generation_note_lines:
        return None

    lines = " ".join(
        rf'\line {{ "{_quote_markup_text(line)}" }}'
        for line in piece.generation_note_lines
    )
    return abjad.Markup(rf'\markup \column {{ {lines} }}')


def build_lilypond_file(piece: Piece) -> abjad.LilyPondFile:
    voice_lookup = {voice.staff_id: voice for voice in piece.voices}

    violin_staff = _voice_to_staff(voice_lookup["violin"], piece)
    viola_staff = _voice_to_staff(voice_lookup["viola"], piece)
    cello_staff = _voice_to_staff(voice_lookup["cello"], piece)
    piano_rh_staff = _voice_to_staff(voice_lookup["piano_rh"], piece)
    piano_lh_staff = _voice_to_staff(voice_lookup["piano_lh"], piece)

    piano_staff = abjad.StaffGroup(
        [piano_rh_staff, piano_lh_staff],
        lilypond_type="PianoStaff",
        name="PianoStaff",
    )
    strings_group = abjad.StaffGroup(
        [violin_staff, viola_staff, cello_staff],
        lilypond_type="StaffGroup",
        name="Strings",
    )

    score = abjad.Score([strings_group, piano_staff], name="Score")
    _apply_dynamics(
        violin_staff=violin_staff,
        viola_staff=viola_staff,
        cello_staff=cello_staff,
        piano_rh_staff=piano_rh_staff,
        piano_lh_staff=piano_lh_staff,
        piece=piece,
    )
    _apply_ending(score, piece)

    instrument_names = [
        (violin_staff, "Violin", "Vln."),
        (viola_staff, "Viola", "Vla."),
        (cello_staff, "Cello", "Vc."),
        (piano_staff, "Piano", "Pno."),
    ]
    for component, full_name, short_name in instrument_names:
        abjad.setting(component).instrumentName = rf'\markup "{full_name}"'
        abjad.setting(component).shortInstrumentName = rf'\markup "{short_name}"'

    tempo = abjad.MetronomeMark(
        reference_duration=abjad.Duration(1, 4),
        units_per_minute=piece.tempo_bpm,
    )
    abjad.attach(tempo, abjad.select.leaf(violin_staff, 0))

    header_block = abjad.Block("header")
    header_block.items.append(rf'title = "{piece.title}"')
    header_block.items.append(rf'composer = "{piece.composer}"')
    header_block.items.append(r"tagline = ##f")

    layout_block = abjad.Block("layout")
    layout_block.items.append(r"indent = 2.0\cm")

    midi_block = abjad.Block("midi")

    score_block = abjad.Block("score")
    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)

    items: list = [header_block, score_block]
    generation_note_markup = _build_generation_note_markup(piece)
    if generation_note_markup is not None:
        items.append(generation_note_markup)

    return abjad.LilyPondFile(items=items)
