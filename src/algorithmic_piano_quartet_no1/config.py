"""Configuration loading for Algo Rhythms Quartet No. 1."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


@dataclass(frozen=True)
class PartConfig:
    id: str
    name: str
    short_name: str
    family: str
    clef: str
    midi_channel: int
    midi_program: int
    midi_instrument: str
    range_low: int
    range_high: int
    staff_type: str = "single"
    role: str = "melodic"


@dataclass(frozen=True)
class GenerationConfig:
    measures: int
    time_signature: tuple[int, int]
    min_note_quanta: int
    max_note_quanta: int
    min_rest_quanta: int
    max_rest_quanta: int
    max_simultaneous_tones_per_quantum: int
    max_pitch_leap: int
    seed: int
    tempo_bpm: int
    measure_quanta: int


@dataclass(frozen=True)
class RenderConfig:
    soundfont: str | None
    piano_soundfont: str | None
    strings_soundfont: str | None
    sample_rate: int


@dataclass(frozen=True)
class OutputConfig:
    basename: str
    label: str | None
    include_measures: bool
    include_tempo: bool
    include_seed: bool
    include_timestamp: bool
    timestamp_format: str


@dataclass(frozen=True)
class ProjectConfig:
    title: str
    composer: str
    output: OutputConfig
    pitch_classes: tuple[int, ...]
    generation: GenerationConfig
    render: RenderConfig
    parts: tuple[PartConfig, ...]


def _parse_duration_to_quanta(value: str, base_unit: Fraction) -> int:
    duration = Fraction(value)
    quanta = duration / base_unit
    if quanta.denominator != 1:
        raise ValueError(f"Duration {value!r} is not aligned to the minimum note duration.")
    return quanta.numerator


def _parse_midi_pitch(value: str) -> int:
    note_names = {
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7,
        "A": 9,
        "B": 11,
    }
    name = value.strip()
    letter = name[0].upper()
    accidental = 0
    index = 1
    if len(name) > 2 and name[1] in {"b", "#"}:
        accidental = -1 if name[1] == "b" else 1
        index = 2
    octave = int(name[index:])
    return (octave + 1) * 12 + note_names[letter] + accidental


def _default_midi_instrument(part_id: str, family: str, staff_type: str) -> str:
    if staff_type == "grand":
        return "acoustic grand"
    if part_id in {"violin", "viola", "cello"}:
        return part_id
    if family == "keyboard":
        return "acoustic grand"
    return "acoustic grand"


def load_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path)
    with config_path.open("rb") as file_pointer:
        data = tomllib.load(file_pointer)

    generation_data = data["generation"]
    time_signature = tuple(generation_data.get("time_signature", [4, 4]))
    base_unit = Fraction(generation_data.get("min_note_duration", "1/16"))
    measure_length = Fraction(time_signature[0], time_signature[1])
    measure_quanta = _parse_duration_to_quanta(str(measure_length), base_unit)

    parts = []
    for entry in data["parts"]:
        pitch_range = entry["range"]
        parts.append(
            PartConfig(
                id=entry["id"],
                name=entry["name"],
                short_name=entry["short_name"],
                family=entry["family"],
                clef=entry.get("clef", "treble"),
                midi_channel=entry.get("midi_channel", 1),
                midi_program=entry.get("midi_program", 1),
                midi_instrument=entry.get(
                    "midi_instrument",
                    _default_midi_instrument(
                        entry["id"],
                        entry["family"],
                        entry.get("staff_type", "single"),
                    ),
                ),
                range_low=_parse_midi_pitch(pitch_range[0]),
                range_high=_parse_midi_pitch(pitch_range[1]),
                staff_type=entry.get("staff_type", "single"),
                role=entry.get("role", "melodic"),
            )
        )

    generation = GenerationConfig(
        measures=generation_data.get("measures", 4),
        time_signature=time_signature,
        min_note_quanta=_parse_duration_to_quanta(
            generation_data.get("min_note_duration", "1/16"),
            base_unit,
        ),
        max_note_quanta=_parse_duration_to_quanta(
            generation_data.get("max_note_duration", str(measure_length)),
            base_unit,
        ),
        min_rest_quanta=_parse_duration_to_quanta(
            generation_data.get("min_rest_duration", "1/16"),
            base_unit,
        ),
        max_rest_quanta=_parse_duration_to_quanta(
            generation_data.get("max_rest_duration", "1/4"),
            base_unit,
        ),
        max_simultaneous_tones_per_quantum=generation_data.get(
            "max_simultaneous_tones_per_quantum", 4
        ),
        max_pitch_leap=generation_data.get("max_pitch_leap", 5),
        seed=generation_data.get("seed", 17),
        tempo_bpm=generation_data.get("tempo_bpm", 72),
        measure_quanta=measure_quanta,
    )

    materials = data.get("materials", {})
    pitch_classes = tuple(materials.get("pitch_classes", [0, 1, 3, 6, 8, 10]))
    render_data = data.get("render", {})

    output_data = data.get("output", {})

    return ProjectConfig(
        title=data.get("title", "Untitled Piano Quartet"),
        composer=data.get("composer", "Unknown Composer"),
        output=OutputConfig(
            basename=output_data.get("basename", "algo-rhythms-quartet-no-1"),
            label=output_data.get("label"),
            include_measures=output_data.get("include_measures", True),
            include_tempo=output_data.get("include_tempo", True),
            include_seed=output_data.get("include_seed", True),
            include_timestamp=output_data.get("include_timestamp", True),
            timestamp_format=output_data.get("timestamp_format", "%Y%m%d-%H%M%S"),
        ),
        pitch_classes=pitch_classes,
        generation=generation,
        render=RenderConfig(
            soundfont=render_data.get("soundfont"),
            piano_soundfont=render_data.get("piano_soundfont"),
            strings_soundfont=render_data.get("strings_soundfont"),
            sample_rate=render_data.get("sample_rate", 44100),
        ),
        parts=tuple(parts),
    )
