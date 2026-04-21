from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "_static" / "art-song-production-timeline.svg"


SECTIONS = [
    {
        "name": "Intro",
        "duration": 18,
        "text": "abstract liftoff; sub drone, radio noise, ignition swell",
        "color": "#44546a",
    },
    {
        "name": "Verse 1",
        "duration": 32,
        "text": "speech-forward Kennedy declaration; sparse piano and low pulse",
        "color": "#6f7f94",
    },
    {
        "name": "Refrain",
        "duration": 34,
        "text": "organized telemetry groove; harmonized refrain",
        "color": "#3f8f8c",
    },
    {
        "name": "Verse 2",
        "duration": 34,
        "text": "new-sea expansion; wider pads, guitar harmonics, fluid pulse",
        "color": "#6aa36f",
    },
    {
        "name": "Short Refrain",
        "duration": 22,
        "text": "Kennedy signal returns; filtered refrain pattern",
        "color": "#7aa7a4",
    },
    {
        "name": "Bridge",
        "duration": 40,
        "text": "Artemis response; close voice, suspended harmony, cold ambience",
        "color": "#b08a45",
    },
    {
        "name": "Loss of Signal",
        "duration": 14,
        "text": "far side blackout; mono narrowing, static cutoff, near silence",
        "color": "#2f343b",
    },
    {
        "name": "Final Verse/Refrain",
        "duration": 54,
        "text": "history heard again; human band and machine pulse combine",
        "color": "#8a5f7d",
    },
    {
        "name": "Coda",
        "duration": 30,
        "text": "We choose Earth / each other; communal vocal stack",
        "color": "#c06f50",
    },
    {
        "name": "Outro",
        "duration": 26,
        "text": "silence, radio crackle, reentry rumble, triumphant return",
        "color": "#d39a3d",
    },
]


def text_lines(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if current and len(candidate) > max_chars:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def format_time(seconds: int) -> str:
    return f"{seconds // 60}:{seconds % 60:02d}"


def main() -> None:
    total = sum(section["duration"] for section in SECTIONS)
    width = 1400
    height = 1050
    left = 86
    timeline_left = 260
    timeline_right = 970
    notes_left = 1008
    top = 198
    lane_height = 44
    row_gap = 78
    bar_width = timeline_right - timeline_left
    minute_marks = range(0, total + 1, 60)

    def x_for(seconds: float) -> float:
        return timeline_left + (seconds / total) * bar_width

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">Production timeline for We Choose the Moon, We Choose Earth</title>",
        "<desc id=\"desc\">A Python-generated lead-sheet timeline mapping the song sections to sound design and arrangement gestures.</desc>",
        "<style>",
        "text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; fill: #1f2933; }",
        ".small { font-size: 18px; }",
        ".time { font-size: 15px; font-weight: 700; }",
        ".label { font-size: 20px; font-weight: 700; }",
        ".column { font-size: 16px; font-weight: 800; fill: #5a6573; text-transform: uppercase; }",
        ".title { font-size: 34px; font-weight: 800; }",
        ".subtitle { font-size: 18px; fill: #5a6573; }",
        ".tick { stroke: #d9dee7; stroke-width: 1; stroke-dasharray: 4 8; }",
        ".axis { stroke: #7d8794; stroke-width: 2; }",
        "</style>",
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#f7f8f6"/>',
        '<text class="title" x="86" y="58">Production Timeline</text>',
        '<text class="subtitle" x="86" y="88">We Choose the Moon, We Choose Earth: lead-sheet form for Logic-based realization</text>',
        f'<text class="column" x="{left}" y="{top - 24}">Section</text>',
        f'<text class="column" x="{timeline_left}" y="{top - 24}">Time</text>',
        f'<text class="column" x="{notes_left}" y="{top - 24}">Sound cue</text>',
    ]

    axis_y = top - 52
    lines.append(f'<line class="axis" x1="{timeline_left}" y1="{axis_y}" x2="{timeline_right}" y2="{axis_y}"/>')
    for mark in minute_marks:
        x = x_for(mark)
        label = format_time(mark)
        lines.append(f'<line class="tick" x1="{x:.1f}" y1="{axis_y - 10}" x2="{x:.1f}" y2="{height - 50}"/>')
        lines.append(f'<text class="small" x="{x - 20:.1f}" y="{axis_y - 18}">{label}</text>')

    elapsed = 0
    for index, section in enumerate(SECTIONS):
        y = top + index * row_gap
        x = x_for(elapsed)
        w = (section["duration"] / total) * bar_width
        elapsed += section["duration"]
        lines.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{lane_height}" rx="6" '
            f'fill="{section["color"]}"/>'
        )
        lines.append(f'<text class="label" x="{left}" y="{y + 28}">{escape(section["name"])}</text>')
        lines.append(
            f'<text class="time" x="{x + 8:.1f}" y="{y + lane_height + 18:.1f}">'
            f'{format_time(elapsed - section["duration"])} +{section["duration"]}s</text>'
        )
        section_lines = text_lines(section["text"], 38)[:2]
        text_x = notes_left
        text_y = y + 16
        for line_index, line in enumerate(section_lines):
            lines.append(
                f'<text class="small" x="{text_x:.1f}" y="{text_y + (line_index * 19):.1f}" '
                f'fill="#1f2933">{escape(line)}</text>'
            )

    lines.append(f'<text class="subtitle" x="86" y="{height - 30}">Approximate durations are placeholders; the graphic describes compositional pacing rather than a fixed click track.</text>')
    lines.append("</svg>")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
