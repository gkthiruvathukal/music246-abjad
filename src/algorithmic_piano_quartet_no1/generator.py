"""Generate Algo Rhythms Quartet No. 1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random

from .config import PartConfig, ProjectConfig


@dataclass(frozen=True)
class Event:
    start_quantum: int
    duration_quanta: int
    pitch: int | None


@dataclass(frozen=True)
class VoiceMaterial:
    staff_id: str
    part_id: str
    name: str
    short_name: str
    clef: str
    midi_instrument: str
    events: tuple[Event, ...]


@dataclass(frozen=True)
class Piece:
    title: str
    composer: str
    time_signature: tuple[int, int]
    tempo_bpm: int
    measure_quanta: int
    measures: int
    voices: tuple[VoiceMaterial, ...]
    generation_note_lines: tuple[str, ...]


class OccupancyTracker:
    """Track sounding-note density on a quantized timeline."""

    def __init__(self, total_quanta: int, limit: int):
        self._counts = [0] * total_quanta
        self._limit = limit

    def count(self, quantum: int) -> int:
        return self._counts[quantum]

    def can_place(self, start: int, duration: int, tones: int = 1) -> bool:
        stop = start + duration
        return all(self._counts[index] + tones <= self._limit for index in range(start, stop))

    def occupy(self, start: int, duration: int, tones: int = 1) -> None:
        stop = start + duration
        for index in range(start, stop):
            self._counts[index] += tones


def _powers_of_two(minimum: int, maximum: int, remaining: int) -> list[int]:
    values = []
    value = 1
    while value <= maximum:
        if minimum <= value <= remaining:
            values.append(value)
        value *= 2
    return values


def _split_piano_part(part: PartConfig) -> list[tuple[str, str, str, str, int, int, str]]:
    midpoint = 60
    rh_low = max(part.range_low, midpoint)
    rh_high = part.range_high
    lh_low = part.range_low
    lh_high = min(part.range_high, midpoint)
    return [
        ("piano_rh", "piano", "Piano RH", "Pno.", "treble", rh_low, rh_high, part.midi_instrument),
        ("piano_lh", "piano", "Piano LH", "Pno.", "bass", lh_low, lh_high, part.midi_instrument),
    ]


def _candidate_pitches(
    low: int,
    high: int,
    pitch_classes: tuple[int, ...],
    anchor: int,
    last_pitch: int | None,
    max_pitch_leap: int,
) -> list[int]:
    pitches = [pitch for pitch in range(low, high + 1) if pitch % 12 in pitch_classes]
    if last_pitch is not None:
        close = [pitch for pitch in pitches if abs(pitch - last_pitch) <= max_pitch_leap]
        if close:
            return sorted(close, key=lambda pitch: (abs(pitch - anchor), abs(pitch - last_pitch)))
    return sorted(pitches, key=lambda pitch: abs(pitch - anchor))


def _rest_probability(role: str, current_density: int, limit: int) -> float:
    base = 0.2 if role != "bass" else 0.3
    if current_density >= limit - 1:
        base += 0.35
    return min(base, 0.85)


def _ending_rest_boost(cursor: int, total_quanta: int, measure_quanta: int) -> float:
    measures_remaining = (total_quanta - cursor) / measure_quanta
    if measures_remaining <= 1:
        return 0.45
    if measures_remaining <= 2:
        return 0.2
    return 0.0


def _duration_candidates(role: str, minimum: int, maximum: int, remaining: int) -> list[int]:
    values = _powers_of_two(minimum, maximum, remaining)
    if role == "bass":
        return sorted(values, reverse=True)
    return sorted(values)


def _merge_adjacent_rests(events: list[Event], measure_quanta: int) -> list[Event]:
    if not events:
        return events
    merged: list[Event] = [events[0]]
    for event in events[1:]:
        previous = merged[-1]
        same_measure = (
            previous.start_quantum // measure_quanta == event.start_quantum // measure_quanta
        )
        contiguous = previous.start_quantum + previous.duration_quanta == event.start_quantum
        if (
            previous.pitch is None
            and event.pitch is None
            and same_measure
            and contiguous
        ):
            merged[-1] = Event(
                start_quantum=previous.start_quantum,
                duration_quanta=previous.duration_quanta + event.duration_quanta,
                pitch=None,
            )
        else:
            merged.append(event)
    return merged


def _pitch_class_names(pitch_classes: tuple[int, ...]) -> str:
    names = {
        0: "C",
        1: "Db",
        2: "D",
        3: "Eb",
        4: "E",
        5: "F",
        6: "Gb",
        7: "G",
        8: "Ab",
        9: "A",
        10: "Bb",
        11: "B",
    }
    return ", ".join(names[value] for value in pitch_classes)


def _soundfont_name(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).expanduser().name


def _build_generation_note_lines(config: ProjectConfig) -> tuple[str, ...]:
    lines = [
        "Compositional Parameters:",
        f"Measures: {config.generation.measures}",
        f"Tempo: {config.generation.tempo_bpm} BPM",
        f"Seed: {config.generation.seed}",
        f"Pitch classes: {_pitch_class_names(config.pitch_classes)}",
        "Instrumentation: piano, violin, viola, cello",
    ]

    piano_soundfont = _soundfont_name(config.render.piano_soundfont)
    strings_soundfont = _soundfont_name(config.render.strings_soundfont)
    if piano_soundfont and strings_soundfont:
        lines.append(
            f"Render: piano={piano_soundfont}; strings={strings_soundfont}"
        )
    elif config.render.soundfont:
        lines.append(f"Render: {_soundfont_name(config.render.soundfont)}")

    return tuple(lines)


def _generate_voice(
    staff_id: str,
    part_id: str,
    name: str,
    short_name: str,
    clef: str,
    midi_instrument: str,
    low: int,
    high: int,
    role: str,
    config: ProjectConfig,
    tracker: OccupancyTracker,
    rng: random.Random,
) -> VoiceMaterial:
    total_quanta = config.generation.measures * config.generation.measure_quanta
    note_min = config.generation.min_note_quanta
    note_max = config.generation.max_note_quanta
    rest_min = config.generation.min_rest_quanta
    rest_max = config.generation.max_rest_quanta
    max_pitch_leap = config.generation.max_pitch_leap + (2 if role == "bass" else 0)
    anchor = (low + high) // 2
    last_pitch: int | None = None
    cursor = 0
    events: list[Event] = []

    while cursor < total_quanta:
        measure_offset = cursor % config.generation.measure_quanta
        measure_remaining = config.generation.measure_quanta - measure_offset
        current_density = tracker.count(cursor)
        choose_rest = current_density >= config.generation.max_simultaneous_tones_per_quantum
        if not choose_rest:
            rest_probability = _rest_probability(
                role,
                current_density,
                config.generation.max_simultaneous_tones_per_quantum,
            )
            rest_probability += _ending_rest_boost(
                cursor=cursor,
                total_quanta=total_quanta,
                measure_quanta=config.generation.measure_quanta,
            )
            choose_rest = rng.random() < min(rest_probability, 0.95)

        if choose_rest:
            durations = _duration_candidates(role, rest_min, rest_max, measure_remaining)
            duration = rng.choice(durations)
            events.append(Event(start_quantum=cursor, duration_quanta=duration, pitch=None))
            cursor += duration
            continue

        durations = _duration_candidates(role, note_min, note_max, measure_remaining)
        if role == "bass":
            durations = [value for value in durations if value >= 2] or durations
        duration = rng.choice(durations)
        if not tracker.can_place(cursor, duration):
            rest_duration = min(measure_remaining, max(rest_min, 1))
            events.append(Event(start_quantum=cursor, duration_quanta=rest_duration, pitch=None))
            cursor += rest_duration
            continue

        candidates = _candidate_pitches(
            low=low,
            high=high,
            pitch_classes=config.pitch_classes,
            anchor=anchor,
            last_pitch=last_pitch,
            max_pitch_leap=max_pitch_leap,
        )
        window = min(6, len(candidates))
        pitch = rng.choice(candidates[:window]) if candidates else anchor
        tracker.occupy(cursor, duration)
        events.append(Event(start_quantum=cursor, duration_quanta=duration, pitch=pitch))
        last_pitch = pitch
        cursor += duration

    return VoiceMaterial(
        staff_id=staff_id,
        part_id=part_id,
        name=name,
        short_name=short_name,
        clef=clef,
        midi_instrument=midi_instrument,
        events=tuple(_merge_adjacent_rests(events, config.generation.measure_quanta)),
    )


def compose_piece(config: ProjectConfig) -> Piece:
    tracker = OccupancyTracker(
        total_quanta=config.generation.measures * config.generation.measure_quanta,
        limit=config.generation.max_simultaneous_tones_per_quantum,
    )
    rng = random.Random(config.generation.seed)
    voices: list[VoiceMaterial] = []

    for part in config.parts:
        if part.staff_type == "grand":
            for staff_id, part_id, name, short_name, clef, low, high, midi_instrument in _split_piano_part(part):
                role = "bass" if clef == "bass" else "melodic"
                voices.append(
                    _generate_voice(
                        staff_id=staff_id,
                        part_id=part_id,
                        name=name,
                        short_name=short_name,
                        clef=clef,
                        midi_instrument=midi_instrument,
                        low=low,
                        high=high,
                        role=role,
                        config=config,
                        tracker=tracker,
                        rng=rng,
                    )
                )
        else:
            voices.append(
                _generate_voice(
                    staff_id=part.id,
                    part_id=part.id,
                    name=part.name,
                    short_name=part.short_name,
                    clef=part.clef,
                    midi_instrument=part.midi_instrument,
                    low=part.range_low,
                    high=part.range_high,
                    role=part.role,
                    config=config,
                    tracker=tracker,
                    rng=rng,
                )
            )

    return Piece(
        title=config.title,
        composer=config.composer,
        time_signature=config.generation.time_signature,
        tempo_bpm=config.generation.tempo_bpm,
        measure_quanta=config.generation.measure_quanta,
        measures=config.generation.measures,
        voices=tuple(voices),
        generation_note_lines=_build_generation_note_lines(config),
    )
