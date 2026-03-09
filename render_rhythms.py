import abjad
import os
import sys

# Add src to path so we can import jazz_rhythm
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from jazz_rhythm import rhythms


def main():
    # Create a score
    score = abjad.Score([], name="Score")

    # 1. Charleston
    staff1 = abjad.Staff(lilypond_type="RhythmicStaff", name="Charleston Staff")
    notes1 = []
    for _ in range(4):  # 4 measures
        notes1.extend(rhythms.charleston())
    staff1.extend(notes1)
    # attach markup to first note
    if notes1:
        abjad.attach(
            abjad.Markup(r'\markup "Charleston"'), notes1[0], direction=abjad.UP
        )

    # 2. Charleston Extended
    staff_extended = abjad.Staff(
        lilypond_type="RhythmicStaff", name="Charleston Extended Staff"
    )
    notes_extended = []
    for _ in range(4):
        notes_extended.extend(rhythms.charleston_extended())
    staff_extended.extend(notes_extended)
    if notes_extended:
        abjad.attach(
            abjad.Markup(r'\markup "Charleston Extended (and of 4)"'),
            notes_extended[0],
            direction=abjad.UP,
        )

    # 3. Anticipation
    staff2 = abjad.Staff(lilypond_type="RhythmicStaff", name="Anticipation Staff")
    notes2 = []
    for _ in range(4):
        notes2.extend(rhythms.anticipation())
    staff2.extend(notes2)
    if notes2:
        abjad.attach(
            abjad.Markup(r'\markup "Anticipation (push to 1)"'),
            notes2[0],
            direction=abjad.UP,
        )

    # 3. Two Beat
    staff3 = abjad.Staff(lilypond_type="RhythmicStaff", name="Two Beat Staff")
    notes3 = []
    for _ in range(4):
        notes3.extend(rhythms.two_beat())
    staff3.extend(notes3)
    if notes3:
        abjad.attach(
            abjad.Markup(r'\markup "Two Beat Comping"'), notes3[0], direction=abjad.UP
        )

    # 4. Syncopated
    staff4 = abjad.Staff(lilypond_type="RhythmicStaff", name="Syncopated Staff")
    notes4 = []
    for _ in range(4):
        notes4.extend(rhythms.syncopated())
    staff4.extend(notes4)
    if notes4:
        abjad.attach(
            abjad.Markup(r'\markup "Syncopated (off-beats)"'),
            notes4[0],
            direction=abjad.UP,
        )

    # Add staves to score
    score.append(staff1)
    score.append(staff_extended)
    score.append(staff2)
    score.append(staff3)
    score.append(staff4)

    # Create LilyPond file structure
    header_block = abjad.Block(name="header")
    header_block.items.append(r'title = "Jazz Rhythmic Patterns"')
    header_block.items.append(r'composer = "Abjad Generated"')

    score_block = abjad.Block(name="score")
    score_block.items.append(score)

    layout_block = abjad.Block(name="layout")
    layout_block.items.append(r"indent = 2.0\cm")

    score_block.items.append(layout_block)

    lilypond_file = abjad.LilyPondFile(
        items=[
            header_block,
            score_block,
        ]
    )

    # Render
    output_path = "build/jazz-rhythms.pdf"
    os.makedirs("build", exist_ok=True)

    print(f"Persisting to {output_path}...")
    abjad.persist.as_pdf(lilypond_file, output_path)
    print("Done.")


if __name__ == "__main__":
    main()
