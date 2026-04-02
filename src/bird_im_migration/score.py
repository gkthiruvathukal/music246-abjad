"""Score construction for Bird Im-Migration."""

from __future__ import annotations

from pathlib import Path

import abjad

from .analysis import (
    CURATED_BIRD_REGIONS,
    DEFAULT_PARTIALS_PATH,
    events_to_lilypond_string,
    format_region,
    group_quantized_events,
    parse_spear_partials,
    quantize_region_pitches,
)

TITLE = "Bird Im-Migration"
COMPOSER = "George K. Thiruvathukal"
SUBTITLE = "Spectral bird partials reduced to performable notation"


def _attach_common_indicators(voice, *, tempo_bpm: int, midi_instrument: str) -> None:
    first_leaf = voice[0]
    last_leaf = voice[-1]
    abjad.attach(abjad.Clef("treble"), first_leaf)
    abjad.attach(abjad.TimeSignature((4, 4)), first_leaf)
    abjad.attach(abjad.MetronomeMark(abjad.Duration(1, 4), tempo_bpm), first_leaf)
    abjad.attach(
        abjad.LilyPondLiteral(
            f'\\set Staff.midiInstrument = "{midi_instrument}"',
            site="before",
        ),
        first_leaf,
    )
    abjad.attach(abjad.LilyPondLiteral(r"\ottava #1", site="before"), first_leaf)
    abjad.attach(abjad.LilyPondLiteral(r"\ottava #0", site="before"), last_leaf)


def _make_measure_string(partials, region, *, bins_per_measure: int, denominator: int) -> str:
    note_bins = quantize_region_pitches(partials, region, bins_per_measure=bins_per_measure)
    events = group_quantized_events(note_bins)
    return events_to_lilypond_string(events, denominator=denominator)


def build_score(
    partials,
    *,
    quantization: int = 32,
    tempo_bpm: int = 90,
    midi_instrument: str = "acoustic grand",
):
    bins_per_measure = quantization
    measure_strings = [
        _make_measure_string(
            partials,
            region,
            bins_per_measure=bins_per_measure,
            denominator=quantization,
        )
        for _, region in CURATED_BIRD_REGIONS
    ]
    voice_source = " |\n".join(measure_strings)
    voice = abjad.Voice(voice_source, name="BirdImMigrationVoice")
    staff = abjad.Staff([voice], name="BirdImMigrationStaff")
    score = abjad.Score([staff], name="BirdImMigrationScore")
    _attach_common_indicators(voice, tempo_bpm=tempo_bpm, midi_instrument=midi_instrument)

    measures = abjad.select.group_by_measure(voice)
    for measure, (title, region) in zip(measures, CURATED_BIRD_REGIONS):
        first_leaf = abjad.select.leaf(measure, 0)
        abjad.attach(
            abjad.LilyPondLiteral(
                r"\once \override TextScript.self-alignment-X = #LEFT",
                site="before",
            ),
            first_leaf,
        )
        markup = abjad.Markup(
            rf'\markup \column {{ "{title}" "WAV {format_region(region)}" }}'
        )
        abjad.attach(markup, first_leaf)
    return score


def build_lilypond_file(
    *,
    partials_path: str | Path = DEFAULT_PARTIALS_PATH,
    quantization: int = 32,
    tempo_bpm: int = 90,
    midi_instrument: str = "acoustic grand",
):
    partials = parse_spear_partials(partials_path)
    score = build_score(
        partials,
        quantization=quantization,
        tempo_bpm=tempo_bpm,
        midi_instrument=midi_instrument,
    )

    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{TITLE}"')
    header_block.items.append(rf'subtitle = "{SUBTITLE}"')
    header_block.items.append(rf'composer = "{COMPOSER}"')
    header_block.items.append(r"tagline = ##f")

    layout_block = abjad.Block(name="layout")
    layout_block.items.append(
        r"""
\context {
  \Staff
  ottavation = "8va"
}
""".strip()
    )
    midi_block = abjad.Block(name="midi")

    score_block = abjad.Block(name="score")
    score_block.items.append(score)
    score_block.items.append(layout_block)
    score_block.items.append(midi_block)
    return abjad.LilyPondFile(items=[header_block, score_block])

