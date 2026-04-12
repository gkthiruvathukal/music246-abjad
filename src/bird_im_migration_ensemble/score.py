"""Score assembly for Bird Im-Migration Ensemble."""

from __future__ import annotations

import abjad
from fractions import Fraction

from .generator import (
    EnsembleEvent,
    EnsemblePiece,
    InstrumentPart,
    MeasureAnnotation,
    MovementMaterial,
)


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


def _midi_to_pitch_name(midi_note: int) -> str:
    pitch_class = PITCH_CLASS_NAMES[midi_note % 12]
    octave = midi_note // 12 - 1
    if octave >= 4:
        octave_marks = "'" * (octave - 3)
    else:
        octave_marks = "," * (3 - octave)
    return f"{pitch_class}{octave_marks}"


def _split_duration_units(total_units: int, measure_units: int) -> list[int]:
    values = []
    power = 1
    while power <= max(16, measure_units):
        values.append(power)
        power *= 2
    values.sort(reverse=True)

    result: list[int] = []
    remaining = total_units
    for value in values:
        while remaining >= value:
            result.append(value)
            remaining -= value
    if remaining:
        raise ValueError(f"Could not split {total_units} sixteenth units.")
    return result


def _split_event_at_measure_boundaries(
    event: EnsembleEvent,
    *,
    measure_units: int,
) -> list[EnsembleEvent]:
    result: list[EnsembleEvent] = []
    start = event.start_unit
    remaining = event.duration_units
    while remaining > 0:
        measure_stop = ((start // measure_units) + 1) * measure_units
        available = measure_stop - start
        duration = min(remaining, available)
        result.append(
            EnsembleEvent(
                start_unit=start,
                duration_units=duration,
                pitches=event.pitches,
            )
        )
        start += duration
        remaining -= duration
    return result


def _make_leaves_for_event(
    event: EnsembleEvent,
    *,
    measure_units: int,
    percussion: bool,
) -> list[abjad.Leaf]:
    duration_chunks = _split_duration_units(event.duration_units, measure_units)
    leaves: list[abjad.Leaf] = []
    for chunk in duration_chunks:
        duration = abjad.Duration(chunk, 16)
        if event.pitches is None:
            pitch_lists = [[]]
        elif percussion:
            pitch_lists = [[abjad.NamedPitch("c'")]]
        elif len(event.pitches) == 1:
            pitch_lists = [[abjad.NamedPitch(_midi_to_pitch_name(event.pitches[0]))]]
        else:
            pitch_lists = [
                [abjad.NamedPitch(_midi_to_pitch_name(pitch)) for pitch in event.pitches]
            ]
        chunk_leaves = abjad.makers.make_leaves(pitch_lists, [duration])
        leaves.extend(chunk_leaves)
    if event.pitches is not None and not percussion and len(leaves) > 1:
        abjad.tie(leaves)
    return leaves


def _attach_staff_indicators(
    staff: abjad.Staff,
    part: InstrumentPart,
    movement: MovementMaterial,
) -> None:
    first_leaf = abjad.select.leaf(staff, 0)
    abjad.attach(abjad.Clef(part.clef), first_leaf)
    abjad.attach(abjad.TimeSignature(movement.config.time_signature), first_leaf)
    abjad.setting(staff).instrumentName = rf'\markup {{ "{part.name}" }}'
    abjad.setting(staff).shortInstrumentName = rf'\markup {{ "{part.short_name}" }}'
    abjad.attach(abjad.LilyPondLiteral(movement.config.key_literal, site="before"), first_leaf)
    if part.staff_id != "percussion":
        abjad.setting(staff).midiInstrument = rf'"{part.midi_instrument}"'


def _style_as_jazz_hits(staff: abjad.Staff) -> None:
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


def _build_staff(part: InstrumentPart, movement: MovementMaterial) -> abjad.Staff:
    voice = abjad.Voice(name=f"{part.staff_id}_voice")
    measures: list[abjad.Container] = []
    split_events = []
    for event in part.events:
        split_events.extend(
            _split_event_at_measure_boundaries(event, measure_units=movement.measure_units)
        )
    event_iter = iter(split_events)
    current = next(event_iter, None)

    for measure_index in range(movement.measures):
        measure_start = measure_index * movement.measure_units
        measure_stop = measure_start + movement.measure_units
        container = abjad.Container()
        while current is not None and current.start_unit < measure_stop:
            for leaf in _make_leaves_for_event(
                current,
                measure_units=movement.measure_units,
                percussion=part.staff_id == "percussion",
            ):
                container.append(leaf)
            current = next(event_iter, None)
        voice.append(container)
        measures.append(container)

    staff = abjad.Staff([voice], name=part.staff_id)
    _attach_staff_indicators(staff, part, movement)
    if part.staff_id == "percussion":
        _style_as_jazz_hits(staff)
    if movement.annotation_staff_id == part.staff_id:
        _attach_measure_annotations(staff, measures, movement.measure_annotations)
        _attach_system_breaks(staff, measures, movement.system_break_after_measures)
        _attach_page_breaks(staff, measures, movement.page_break_after_measures)
    return staff


def _annotation_markup(annotation: MeasureAnnotation) -> str:
    if len(annotation.text_lines) > 1:
        title = annotation.text_lines[0]
        subtitle = annotation.text_lines[1]
        return (
            r"\markup \override #'(baseline-skip . 3.2) \column { "
            r"\vspace #1 "
            rf'\line {{ \bold "{title}" }} '
            rf'\line {{ \italic "{subtitle}" }} '
            r"}"
        )
    lines = " ".join(rf'"{line}"' for line in annotation.text_lines)
    return rf"\markup \column {{ {lines} }}"


def _attach_measure_annotations(
    staff: abjad.Staff,
    measures: list[abjad.Container],
    annotations: tuple[MeasureAnnotation, ...],
) -> None:
    for annotation in annotations:
        if annotation.measure_index >= len(measures):
            continue
        first_leaf = abjad.select.leaf(measures[annotation.measure_index], 0)
        if first_leaf is None:
            continue
        abjad.attach(
            abjad.Markup(_annotation_markup(annotation)),
            first_leaf,
            direction=abjad.UP,
        )


def _attach_system_breaks(
    staff: abjad.Staff,
    measures: list[abjad.Container],
    break_after_measures: tuple[int, ...],
) -> None:
    for measure_number in break_after_measures:
        measure_index = measure_number - 1
        if measure_index < 0 or measure_index >= len(measures):
            continue
        last_leaf = abjad.select.leaf(measures[measure_index], -1)
        if last_leaf is None:
            continue
        abjad.attach(abjad.LilyPondLiteral(r"\break", site="after"), last_leaf)


def _attach_page_breaks(
    staff: abjad.Staff,
    measures: list[abjad.Container],
    break_after_measures: tuple[int, ...],
) -> None:
    for measure_number in break_after_measures:
        measure_index = measure_number - 1
        if measure_index < 0 or measure_index >= len(measures):
            continue
        last_leaf = abjad.select.leaf(measures[measure_index], -1)
        if last_leaf is None:
            continue
        abjad.attach(abjad.LilyPondLiteral(r"\pageBreak", site="after"), last_leaf)


def _transpose_score(score: abjad.Score, semitones: int) -> None:
    if semitones:
        abjad.mutate.transpose(score, semitones)


def _build_piano_staff(movement: MovementMaterial) -> abjad.StaffGroup | None:
    part_lookup = {part.staff_id: part for part in movement.parts}
    piano_rh = part_lookup.get("piano_rh")
    piano_lh = part_lookup.get("piano_lh")
    if piano_rh is None or piano_lh is None:
        return None
    rh_staff = _build_staff(piano_rh, movement)
    lh_staff = _build_staff(piano_lh, movement)
    piano_group = abjad.StaffGroup(
        [rh_staff, lh_staff],
        lilypond_type="PianoStaff",
        name="piano_group",
    )
    abjad.setting(piano_group).instrumentName = r'\markup { "Piano" }'
    abjad.setting(piano_group).shortInstrumentName = r'\markup { "Pno." }'
    abjad.setting(rh_staff).instrumentName = None
    abjad.setting(rh_staff).shortInstrumentName = None
    abjad.setting(lh_staff).instrumentName = None
    abjad.setting(lh_staff).shortInstrumentName = None
    return piano_group


def _movement_markup_literal(config) -> str:
    return rf'\mark \markup "{config.title}"'


def _apply_opening_markup(score: abjad.Score, movement: MovementMaterial) -> None:
    first_leaf = abjad.select.leaf(score, 0)
    abjad.attach(
        abjad.LilyPondLiteral(
            r"\once \override Score.RehearsalMark.self-alignment-X = #LEFT",
            site="before",
        ),
        first_leaf,
    )
    abjad.attach(
        abjad.LilyPondLiteral(_movement_markup_literal(movement.config), site="before"),
        first_leaf,
    )
    abjad.attach(
        abjad.MetronomeMark(abjad.Duration(1, 4), movement.config.tempo_bpm),
        first_leaf,
    )


def _apply_closing_indicators(score: abjad.Score, movement: MovementMaterial) -> None:
    if not movement.include_closing_indicators:
        abjad.attach(abjad.BarLine("|."), abjad.select.leaf(score, -1))
        return
    all_pitched = [
        leaf
        for leaf in abjad.select.leaves(score)
        if isinstance(leaf, (abjad.Note, abjad.Chord))
    ]
    if not all_pitched:
        return
    start_measure = max(movement.measures - movement.config.closing_measures, 0)
    closing_offset = abjad.Offset(Fraction(start_measure * movement.measure_units, 16))
    closing_leaves = [
        leaf for leaf in all_pitched if abjad.get.timespan(leaf).start_offset >= closing_offset
    ]
    if not closing_leaves:
        closing_leaves = [all_pitched[-1]]
    abjad.attach(abjad.Dynamic("p"), closing_leaves[0])
    abjad.attach(
        abjad.Markup(r'\markup \italic "steadily fading"'),
        closing_leaves[0],
        direction=abjad.UP,
    )
    abjad.attach(abjad.Dynamic("ppp"), closing_leaves[-1])
    abjad.attach(abjad.BarLine("|."), abjad.select.leaf(score, -1))


def _build_movement_score(movement: MovementMaterial) -> abjad.Score:
    non_piano_parts = [
        part for part in movement.parts if part.staff_id not in {"piano_rh", "piano_lh"}
    ]
    staves = [_build_staff(part, movement) for part in non_piano_parts]
    piano_group = _build_piano_staff(movement)
    if piano_group is not None:
        staves.append(piano_group)
    score = abjad.Score(staves, name=f"movement_{movement.config.number}_score")
    _transpose_score(score, movement.score_transpose_semitones)
    _apply_opening_markup(score, movement)
    _apply_closing_indicators(score, movement)
    return score


def _layout_block_for_movement(movement: MovementMaterial) -> abjad.Block:
    layout_block = abjad.Block(name="layout")
    if movement.annotation_staff_id == "bird_study":
        layout_block.items.append(r"indent = 0\mm")
    return layout_block


def build_lilypond_file(piece: EnsemblePiece) -> abjad.LilyPondFile:
    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{piece.title}"')
    header_block.items.append(rf'subtitle = "{piece.subtitle}"')
    header_block.items.append(rf'composer = "{piece.composer}"')
    header_block.items.append(r"tagline = ##f")

    paper_block = abjad.Block(name="paper")
    paper_block.items.append(r"system-system-spacing.basic-distance = #18")

    items: list[object] = [header_block, paper_block]
    for index, movement in enumerate(piece.movements):
        score_block = abjad.Block(name="score")
        score_block.items.append(_build_movement_score(movement))
        score_block.items.append(_layout_block_for_movement(movement))
        score_block.items.append(abjad.Block(name="midi"))
        items.append(score_block)
        next_movement = piece.movements[index + 1] if index < len(piece.movements) - 1 else None
        if (
            next_movement is not None
            and movement.annotation_staff_id == "bird_study"
            and next_movement.annotation_staff_id == "bird_study"
        ):
            items.append(r"\markup \vspace #2")
        should_page_break = (
            next_movement is not None
            and not (
                movement.annotation_staff_id == "bird_study"
                and next_movement.annotation_staff_id == "bird_study"
            )
        )
        if should_page_break:
            items.append(r"\pageBreak")
    return abjad.LilyPondFile(items=items)
