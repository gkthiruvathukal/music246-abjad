"""Analysis helpers for Bird Im-Migration."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re


DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_AUDIO_PATH = DATA_DIR / "DL_parkbirds.wav"
DEFAULT_PARTIALS_PATH = DATA_DIR / "DL_parkbirds_partials.txt"

PARTIAL_HEADER = re.compile(r"^(\d+)\s+(\d+)\s+([0-9.]+)\s+([0-9.]+)$")


@dataclass(frozen=True)
class Partial:
    index: int
    point_count: int
    start: float
    end: float
    peak_time: float
    peak_frequency: float
    peak_amplitude: float


@dataclass(frozen=True)
class Region:
    start: float
    end: float


@dataclass(frozen=True)
class Bin:
    time: float
    count: int
    total_amplitude: float
    strength: float


@dataclass(frozen=True)
class QuantizedEvent:
    notes: tuple[str, ...]
    duration_units: int


def parse_spear_partials(path: str | Path) -> list[Partial]:
    lines = Path(path).read_text().splitlines()
    partials: list[Partial] = []
    in_data = False
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if line == "partials-data":
            in_data = True
            continue
        if not in_data:
            continue
        match = PARTIAL_HEADER.match(line)
        if not match:
            continue
        partial_index = int(match.group(1))
        point_count = int(match.group(2))
        start = float(match.group(3))
        end = float(match.group(4))
        if index >= len(lines):
            break
        data = lines[index].strip().split()
        index += 1
        peak_amplitude = -1.0
        peak_frequency = 0.0
        peak_time = start
        for offset in range(0, len(data) - 2, 3):
            time = float(data[offset])
            frequency = float(data[offset + 1])
            amplitude = float(data[offset + 2])
            if amplitude > peak_amplitude:
                peak_amplitude = amplitude
                peak_frequency = frequency
                peak_time = time
        partials.append(
            Partial(
                index=partial_index,
                point_count=point_count,
                start=start,
                end=end,
                peak_time=peak_time,
                peak_frequency=peak_frequency,
                peak_amplitude=peak_amplitude,
            )
        )
    return partials


def select_birdlike_partials(
    partials: list[Partial],
    *,
    min_frequency: float = 4500.0,
    max_frequency: float = 6000.0,
    min_amplitude: float = 0.02,
) -> list[Partial]:
    return [
        partial
        for partial in partials
        if min_frequency <= partial.peak_frequency <= max_frequency
        and partial.peak_amplitude >= min_amplitude
    ]


def compute_bird_bins(
    partials: list[Partial],
    *,
    bin_size: float = 0.25,
    strength_count_weight: float = 0.01,
) -> list[Bin]:
    bins: dict[int, list[float]] = {}
    for partial in partials:
        bin_index = int(partial.start / bin_size)
        if bin_index not in bins:
            bins[bin_index] = [0.0, 0.0]
        bins[bin_index][0] += 1.0
        bins[bin_index][1] += partial.peak_amplitude
    return [
        Bin(
            time=bin_index * bin_size,
            count=int(values[0]),
            total_amplitude=values[1],
            strength=values[1] + values[0] * strength_count_weight,
        )
        for bin_index, values in sorted(bins.items())
    ]


def infer_peak_regions(
    bins: list[Bin],
    *,
    bin_size: float = 0.25,
    peak_strength: float = 0.15,
    neighborhood_gap: float = 1.0,
    expansion_strength: float = 0.04,
    expansion_gap: float = 0.5,
) -> list[Region]:
    if not bins:
        return []

    by_time = {round(bin_.time, 6): bin_ for bin_ in bins}
    peaks: list[float] = []
    for i, bin_ in enumerate(bins):
        if bin_.strength < peak_strength:
            continue
        left = bins[i - 1].strength if i > 0 else -1.0
        right = bins[i + 1].strength if i + 1 < len(bins) else -1.0
        if bin_.strength >= left and bin_.strength >= right:
            peaks.append(bin_.time)

    if not peaks:
        return []

    merged_peak_regions: list[Region] = []
    start = peaks[0]
    end = peaks[0]
    for time in peaks[1:]:
        if time - end <= neighborhood_gap:
            end = time
        else:
            merged_peak_regions.append(Region(start, end + bin_size))
            start = time
            end = time
    merged_peak_regions.append(Region(start, end + bin_size))

    expanded_regions: list[Region] = []
    for region in merged_peak_regions:
        left = region.start
        right = region.end
        while True:
            candidate = round(left - bin_size, 6)
            bin_ = by_time.get(candidate)
            if bin_ is None or bin_.strength < expansion_strength or left - candidate > expansion_gap:
                break
            left = candidate
        while True:
            candidate = round(right, 6)
            bin_ = by_time.get(candidate)
            if bin_ is None or bin_.strength < expansion_strength or candidate - right > expansion_gap:
                break
            right = candidate + bin_size
        expanded_regions.append(Region(left, right))

    return merge_overlapping_regions(expanded_regions, merge_gap=0.0)


def merge_overlapping_regions(
    regions: list[Region],
    *,
    merge_gap: float = 0.0,
) -> list[Region]:
    if not regions:
        return []
    regions = sorted(regions, key=lambda region: (region.start, region.end))
    merged: list[Region] = []
    start = regions[0].start
    end = regions[0].end
    for region in regions[1:]:
        if region.start - end <= merge_gap:
            end = max(end, region.end)
        else:
            merged.append(Region(start, end))
            start = region.start
            end = region.end
    merged.append(Region(start, end))
    return merged


def format_region(region: Region) -> str:
    return f"{region.start:.1f}-{region.end:.1f} s"


def midi_to_note_name(midi_number: int) -> str:
    names = ("c", "cs", "d", "ds", "e", "f", "fs", "g", "gs", "a", "as", "b")
    octave = midi_number // 12 - 1
    return f"{names[midi_number % 12]}{octave}"


def note_name_to_lily_pitch(note_name: str) -> str:
    match = re.match(r"^([a-z]+)(-?\d+)$", note_name)
    if not match:
        raise ValueError(f"Bad note name: {note_name}")
    pitch = match.group(1)
    octave = int(match.group(2))
    diff = octave - 5
    if diff > 0:
        return pitch + ("'" * diff)
    if diff < 0:
        return pitch + ("," * (-diff))
    return pitch


def quantize_region_pitches(
    partials: list[Partial],
    region: Region,
    *,
    bins_per_measure: int,
    min_frequency: float = 4500.0,
    max_frequency: float = 6000.0,
    min_amplitude: float = 0.02,
    max_notes_per_bin: int = 2,
) -> list[tuple[str, ...]]:
    buckets: list[dict[str, float]] = [dict() for _ in range(bins_per_measure)]
    span = region.end - region.start
    if span <= 0:
        return [tuple() for _ in range(bins_per_measure)]
    for partial in partials:
        if not (region.start <= partial.start <= region.end):
            continue
        if not (min_frequency <= partial.peak_frequency <= max_frequency):
            continue
        if partial.peak_amplitude < min_amplitude:
            continue
        position = (partial.start - region.start) / span
        bucket_index = min(bins_per_measure - 1, int(position * bins_per_measure))
        midi_number = round(69 + 12 * math.log2(partial.peak_frequency / 440.0))
        note_name = midi_to_note_name(midi_number)
        current = buckets[bucket_index].get(note_name, 0.0)
        if partial.peak_amplitude > current:
            buckets[bucket_index][note_name] = partial.peak_amplitude
    result: list[tuple[str, ...]] = []
    for bucket in buckets:
        top = sorted(bucket.items(), key=lambda item: item[1], reverse=True)[:max_notes_per_bin]
        result.append(tuple(note for note, _ in top))
    return result


def group_quantized_events(note_bins: list[tuple[str, ...]]) -> list[QuantizedEvent]:
    if not note_bins:
        return []
    events: list[QuantizedEvent] = []
    current = note_bins[0]
    duration = 1
    for notes in note_bins[1:]:
        if notes == current:
            duration += 1
        else:
            events.append(QuantizedEvent(current, duration))
            current = notes
            duration = 1
    events.append(QuantizedEvent(current, duration))
    return events


def events_to_lilypond_string(
    events: list[QuantizedEvent],
    *,
    denominator: int,
) -> str:
    allowed_units: list[int] = []
    unit = denominator // 2
    while unit >= 1:
        allowed_units.append(unit)
        unit //= 2

    def split_units(total_units: int) -> list[int]:
        chunks: list[int] = []
        remaining = total_units
        for value in allowed_units:
            while remaining >= value:
                chunks.append(value)
                remaining -= value
        if remaining:
            raise ValueError(f"Could not split duration units: {total_units}")
        return chunks

    tokens: list[str] = []
    for event in events:
        chunks = split_units(event.duration_units)
        if event.notes:
            if len(event.notes) == 1:
                base = note_name_to_lily_pitch(event.notes[0])
            else:
                chord = " ".join(note_name_to_lily_pitch(note) for note in event.notes)
                base = f"<{chord}>"
            note_tokens = []
            for chunk in chunks:
                duration = denominator // chunk
                note_tokens.append(f"{base}{duration}")
            tokens.append(" ~ ".join(note_tokens))
        else:
            rest_tokens = []
            for chunk in chunks:
                duration = denominator // chunk
                rest_tokens.append(f"r{duration}")
            tokens.append(" ".join(rest_tokens))
    return " ".join(tokens)


CURATED_BIRD_REGIONS: tuple[tuple[str, Region], ...] = (
    ("Early birds", Region(0.6, 1.9)),
    ("Middle birds", Region(2.8, 5.6)),
    ("Strong middle/late birds", Region(7.3, 9.1)),
    ("Late birds", Region(10.8, 13.9)),
)

