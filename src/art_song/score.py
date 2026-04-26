"""Score construction for We Choose the Moon, We Choose Earth."""

from __future__ import annotations

import re
from collections.abc import Sequence

import abjad

TITLE = "We Choose the Moon, We Choose Earth"
COMPOSER = "George K. Thiruvathukal"

PitchToken = str | tuple[str, str] | tuple[str, str, str]

SECTION_LENGTHS = {
    "intro": 8,
    "verse_1": 10,
    "refrain": 19,
    "verse_2": 10,
    "short_refrain": 8,
    "bridge": 12,
    "loss_of_signal": 4,
    "outro": 8,
}

SECTION_DYNAMICS = {
    "voice": {
        8: "p",
        18: "mp",
        22: "mf",
        29: "f",
        37: "mp",
        47: "mf",
        55: "mp",
        63: "p",
        67: "pp",
        71: "p",
        78: "pp",
    },
    "violin": {
        0: "pp",
        18: "mp",
        26: "mf",
        37: "p",
        47: "mp",
        55: "p",
        67: "pp",
        71: "p",
        78: "pp",
    },
    "viola": {
        0: "pp",
        18: "mp",
        26: "mf",
        37: "p",
        47: "mp",
        55: "p",
        67: "pp",
        71: "p",
        78: "pp",
    },
    "trumpet": {
        0: "pp",
        18: "mp",
        26: "mf",
        34: "f",
        37: "p",
        47: "mp",
        55: "p",
        63: "mp",
        67: "pp",
        71: "p",
        78: "pp",
    },
    "piano_right": {
        0: "pp",
        8: "p",
        18: "mp",
        26: "mf",
        37: "p",
        47: "mp",
        55: "p",
        67: "pp",
        71: "p",
        78: "pp",
    },
    "piano_left": {
        0: "pp",
        8: "p",
        18: "mp",
        26: "mf",
        37: "p",
        47: "mp",
        55: "p",
        67: "pp",
        71: "p",
        78: "pp",
    },
}

CRESCENDO_RANGES = {
    "voice": [(18, 29), (37, 47), (55, 63), (71, 75)],
    "violin": [(0, 7), (18, 29), (37, 47), (55, 63), (71, 75)],
    "viola": [(18, 29), (37, 47), (55, 63), (71, 75)],
    "trumpet": [(18, 34), (37, 47), (55, 63), (71, 75)],
    "piano_right": [(18, 29), (37, 47), (55, 63), (71, 75)],
    "piano_left": [(18, 29), (37, 47), (55, 63), (71, 75)],
}

DECRESCENDO_RANGES = {
    "voice": [(63, 67), (75, 78)],
    "violin": [(63, 67), (75, 78)],
    "viola": [(63, 67), (75, 78)],
    "trumpet": [(63, 67), (75, 78)],
    "piano_right": [(63, 67), (75, 78)],
    "piano_left": [(63, 67), (75, 78)],
}

CHORD_LABELS: list[list[tuple[str, str]]] = [
    [("1", "D5")],
    [("1", "Dmaj9/F#")],
    [("1", "Gmaj7(#11)")],
    [("2", "A13sus4"), ("2", "A7")],
    [("1", "D5")],
    [("1", "Dmaj9/F#")],
    [("1", "Gmaj7(#11)")],
    [("1", "A13sus4")],
    [("1", "Dadd9")],
    [("1", "Dmaj9/F#")],
    [("1", "Gadd9")],
    [("1", "Dadd9")],
    [("1", "Bm11")],
    [("1", "Gmaj9")],
    [("1", "Em9")],
    [("2", "A7sus4"), ("2", "A7")],
    [("1", "Gadd9")],
    [("2", "A13sus4"), ("2", "A7")],
    [("1", "Gmaj7(#11)")],
    [("1", "Dmaj9/F#")],
    [("1", "Em9")],
    [("2", "A13sus4"), ("2", "A7")],
    [("1", "Bm11")],
    [("1", "F#m7")],
    [("1", "Gadd9")],
    [("1", "A13")],
    [("1", "Gmaj7(#11)")],
    [("1", "Dmaj9/F#")],
    [("1", "Em9")],
    [("2", "A13sus4"), ("2", "A7")],
    [("1", "Bm11")],
    [("1", "Gadd9")],
    [("2", "D/A"), ("2", "A7sus4")],
    [("1", "Dadd9")],
    [("1", "G/D")],
    [("1", "Dadd9")],
    [("1", "A13sus4")],
]

VOICE_MEASURES: list[list[PitchToken]] = [
    ["r1"],
    ["r1"],
    ["r1"],
    ["r1"],
    ["r1"],
    ["r1"],
    ["r1"],
    ["r1"],
    [
        ("d'8", "spoken: We choose to go to the moon.", "We"),
        ("d'8", "", "choose"),
        ("e'8", "", "to"),
        ("fs'8", "", "go"),
        ("a'8", "", "to"),
        ("a'8", "", "the"),
        "r4",
    ],
    [
        ("d'8", "We choose to go to the moon in this decade", "moon"),
        ("e'8", "", "in"),
        ("fs'8", "", "this"),
        ("a'8", "", "dec-"),
        ("b'8", "", "ade"),
        ("b'8", "", "and"),
        ("a'8", "", "do"),
        ("a'8", "", "the"),
    ],
    [
        ("r4", "and do the other things"),
        ("d'8", "", "oth-"),
        ("e'8", "", "er"),
        ("fs'8", "", "things"),
        ("fs'8", "", "not"),
        ("e'4", "", "be-"),
    ],
    [
        ("d'8", "not because they are easy", "cause"),
        ("d'8", "", "they"),
        ("e'8", "", "are"),
        ("fs'8", "", "ea-"),
        ("a'4", "", "sy"),
        "r4",
    ],
    [
        ("d'8", "", "but"),
        ("e'8", "", "be-"),
        ("fs'8", "", "cause"),
        ("a'8", "", "they"),
        ("b'4", "but because they are hard", "are"),
        ("a'4", "", "hard"),
    ],
    ["r1"],
    [("fs'8", "repeat the public voice, still mostly spoken"), "e'8", "d'8", "e'8", "fs'4", "a'4"],
    ["b'4", "a'4", "fs'4", "e'4"],
    [("g'4", "lean toward song here"), "fs'4", "e'4", "d'4"],
    ["e'2", "fs'2"],
    [("a'4", "sung: Because that goal will serve"), "b'4", "a'4", "fs'4"],
    [("e'4", "to organize and measure"), "fs'4", "a'4", "b'4"],
    [("b'4", "the best of our energies and skills"), "a'4", "fs'4", "e'4"],
    ["fs'4", "a'4", "b'4", "a'4"],
    [("a'4", "because that challenge is one"), "a'4", "b'4", "a'4"],
    [("e'4", "that we are willing to accept"), "fs'4", "a'4", "b'4"],
    ["a'4", "fs'4", "e'2"],
    [("fs'4", "one we are unwilling to postpone"), "a'4", "b'4", "a'4"],
    ["e'4", "fs'4", "a'4", "b'4"],
    ["a'4", "fs'4", "e'2"],
    [("fs'4", "and one we intend"), "a'4", "b'4", "a'4"],
    [("d''2", "to win"), "r2"],
    ["r1"],
    [("a'4", "instrumental breath / prepare next verse"), "b'4", "a'4", "fs'4"],
    ["e'4", "fs'4", "a'4", "b'4"],
    ["a'2", "fs'2"],
    ["d'1"],
    ["r1"],
    ["r1"],
]

VIOLIN_MEASURES: list[list[PitchToken]] = [
    [("<a'' e'''>1", "high shimmer: slow natural harmonics")],
    ["<a'' e'''>2", "r2"],
    ["b''16", "a''16", "e''16", "a''16", "b''16", "a''16", "e''16", "a''16", "b''16", "a''16", "e''16", "a''16", "b''16", "a''16", "e''16", "a''16"],
    ["r2", "a''8", "b''8", "e'''8", "a'''8"],
    ["<a'' e'''>1"],
    ["r2", "e''16", "a''16", "b''16", "a''16", "e''16", "a''16", "b''16", "a''16"],
    ["b''1"],
    ["r1"],
    ["r1"],
    [("a''2", "thin halo around speech"), "fs''2"],
    ["e''1"],
    ["r1"],
    ["b''2", "a''2"],
    ["fs''1"],
    ["r1"],
    ["e''2", "fs''2"],
    ["g''1"],
    ["r1"],
    [("b''2", "refrain: sustained upper chord tones"), "a''2"],
    ["fs''1"],
    ["e''2", "fs''2"],
    ["a''1"],
    ["d'''2", "b''2"],
    ["a''1"],
    ["g''2", "fs''2"],
    ["e''1"],
    ["b''2", "a''2"],
    ["fs''1"],
    ["e''2", "fs''2"],
    ["a''1"],
    ["d'''2", "b''2"],
    ["a''2", "fs''2"],
    ["e''1"],
    ["fs''2", "a''2"],
    ["d'''1"],
    ["d'''1"],
    ["r1"],
]

VIOLA_MEASURES: list[list[PitchToken]] = [
    [("d'1", "D/A pedal: gravity")],
    ["a1"],
    ["b1"],
    ["e'1"],
    ["d'1"],
    ["a1"],
    ["b1"],
    ["e'1"],
    ["d'1"],
    ["fs'1"],
    ["g'1"],
    ["d'1"],
    ["b1"],
    ["g1"],
    ["e'1"],
    ["a1"],
    ["g1"],
    ["a1"],
    [("g2", "slow inner line, not accompaniment filler"), "a2"],
    ["fs1"],
    ["e2", "g2"],
    ["a1"],
    ["b2", "a2"],
    ["fs1"],
    ["g2", "e2"],
    ["a1"],
    ["g2", "a2"],
    ["fs1"],
    ["e2", "g2"],
    ["a1"],
    ["b2", "a2"],
    ["g1"],
    ["a1"],
    ["d2", "fs2"],
    ["g1"],
    ["a1"],
    ["a1"],
]

TRUMPET_MEASURES: list[list[PitchToken]] = [
    [("r2", "cup mute if available; distant mission signal"), "a'4", "d''8", "e''8"],
    ["r2", "fs''8", "e''8", "d''4"],
    ["r2", "b'8", "cs''8", "d''8", "e''8"],
    ["fs''2", "e''2"],
    ["r2", "a'4", "d''8", "e''8"],
    ["fs''4", "e''8", "d''8", "cs''4", "b'4"],
    ["r2", "e''4", "fs''8", "a''8"],
    ["e''1"],
    ["r1"],
    [("r2", "small responses, never covering the text"), "a'4", "d''8", "e''8"],
    ["fs''4", "e''8", "d''8", "cs''4", "b'4"],
    ["r2", "e''4", "d''4"],
    ["r1"],
    ["a''4", "fs''8", "e''8", "d''4", "b'4"],
    ["r1"],
    ["e''4", "fs''8", "a''8", "fs''4", "e''4"],
    ["r1"],
    ["a'2.", "r4"],
    ["r1"],
    [("r2", "refrain: lyrical jazz answers around the singer"), "a'8", "b'8", "d''8", "e''8"],
    ["fs''4", "e''8", "d''8", "b'4", "a'4"],
    ["r2", "b'8", "a'8", "fs'8", "e'8"],
    ["d'4", "e'8", "fs'8", "a'4", "g'4"],
    ["fs'8", "a'8", "b'8", "d''8", "e''4", "d''8", "b'8"],
    ["a'4", "fs'4", "e'2"],
    ["r2", "d''8", "b'8", "a'8", "fs'8"],
    ["e'4", "fs'8", "a'8", "b'4", "a'4"],
    ["r2", "a'8", "b'8", "d''8", "e''8"],
    ["fs''4", "e''8", "d''8", "b'4", "a'4"],
    ["r2", "b'8", "a'8", "fs'8", "e'8"],
    ["d'4", "e'8", "fs'8", "a'4", "g'4"],
    ["fs'8", "a'8", "b'8", "d''8", "e''4", "d''8", "b'8"],
    ["a'4", "b'8", "d''8", "fs''4", "e''4"],
    ["d''2", "cs''2"],
    [("d''4", "clear final call"), "e''8", "fs''8", "a''4", "d'''4"],
    ["e'''2", "d'''2"],
    ["a''1"],
]

GUITAR_MEASURES: list[list[PitchToken]] = (
    [
        [("c4", "muted eighths or slow arpeggio"), "c4", "c4", "c4"],
        ["c4", "c4", "c4", "c4"],
        ["c8", "c8", "c8", "c8", "c8", "c8", "c8", "c8"],
        ["c4", "c4", "c4", "c4"],
        ["c4", "c4", "c4", "c4"],
        ["c4", "c4", "c4", "c4"],
        ["c8", "c8", "c8", "c8", "c8", "c8", "c8", "c8"],
        ["c4", "c4", "c4", "c4"],
    ]
    + [[("c4", "stay behind speech"), "c4", "c4", "c4"]]
    + [["c4", "c4", "c4", "c4"] for _ in range(9)]
    + [[("c8", "refrain opens: steady folk-rock motion"), "c8", "c8", "c8", "c8", "c8", "c8", "c8"]]
    + [["c8", "c8", "c8", "c8", "c8", "c8", "c8", "c8"] for _ in range(13)]
    + [["c4", "c4", "c4", "c4"], ["c4", "c4", "c4", "c4"], ["c1"], ["c1"]]
    + [["c1"]]
)

PIANO_RIGHT_MEASURES: list[list[PitchToken]] = [
    [("<a' d''>1", "basic mid-register voicings; pianist may vary")],
    ["<e' a' cs''>1"],
    ["<b' cs'' fs''>1"],
    ["<g' b' d'' fs''>2", "<g' cs'' e''>2"],
    ["<a' d''>1"],
    ["<e' a' cs''>1"],
    ["<b' cs'' fs''>1"],
    ["<g' b' d'' fs''>1"],
    ["<e' fs' a'>1"],
    ["<e' fs' a' cs''>1"],
    ["<a' b' d''>1"],
    ["<e' fs' a'>1"],
    ["<a' cs'' d'' fs''>1"],
    ["<a' b' d'' fs''>1"],
    ["<g' b' d'' fs''>1"],
    ["<g' cs'' e''>2", "<g' cs'' e''>2"],
    ["<a' b' d''>1"],
    ["<g' b' cs'' fs''>2", "<g' cs'' e''>2"],
    ["<b' cs'' fs''>1"],
    ["<e' fs' a' cs''>1"],
    ["<g' b' d'' fs''>1"],
    ["<g' b' cs'' fs''>2", "<g' cs'' e''>2"],
    ["<a' d'' e''>1"],
    ["<e' a' cs''>1"],
    ["<a' b' d''>1"],
    ["<g' b' cs'' fs''>1"],
    ["<b' cs'' fs''>1"],
    ["<e' fs' a' cs''>1"],
    ["<g' b' d'' fs''>1"],
    ["<g' b' cs'' fs''>2", "<g' cs'' e''>2"],
    ["<a' d'' e''>1"],
    ["<a' b' d''>1"],
    ["<fs' a' d''>2", "<g' cs'' e''>2"],
    ["<e' fs' a'>1"],
    ["<b' d'' g''>1"],
    ["<e' fs' a'>1"],
    ["<g' b' cs'' fs''>1"],
]

PIANO_LEFT_MEASURES: list[list[PitchToken]] = [
    ["d,1"],
    ["fs,1"],
    ["g,1"],
    ["a,2", "a,2"],
    ["d,1"],
    ["fs,1"],
    ["g,1"],
    ["a,1"],
    ["d,1"],
    ["fs,1"],
    ["g,1"],
    ["d,1"],
    ["b,1"],
    ["g,1"],
    ["e,1"],
    ["a,2", "a,2"],
    ["g,1"],
    ["a,2", "a,2"],
    ["g,1"],
    ["fs,1"],
    ["e,1"],
    ["a,2", "a,2"],
    ["b,1"],
    ["fs,1"],
    ["g,1"],
    ["a,1"],
    ["g,1"],
    ["fs,1"],
    ["e,1"],
    ["a,2", "a,2"],
    ["b,1"],
    ["g,1"],
    ["d,2", "a,2"],
    ["d,1"],
    ["d,1"],
    ["d,1"],
    ["a,1"],
]

VERSE2_CHORD_LABELS = CHORD_LABELS[8:18]
VERSE2_VOICE_MEASURES: list[list[PitchToken]] = [
    [("d'4", "We set sail on this new sea"), "e'4", "fs'4", "a'4"],
    [("d'4", "because there is new knowledge"), "e'4", "fs'4", "a'4"],
    [("r4", "to be gained,"), "d'8", "e'8", "fs'4", "e'4"],
    [("d'4", "and new rights to be won,"), "e'8", "fs'8", "a'4", "r4"],
    [("d'4", "and they must be won"), "e'4", "fs'4", "a'4"],
    ["r1"],
    [("fs'4", "and used for the progress"), "e'4", "d'4", "e'4"],
    [("g'4", "of all people."), "fs'4", "e'4", "d'4"],
    ["e'2", "fs'2"],
    ["d'1"],
]
VERSE2_VIOLIN_MEASURES = VIOLIN_MEASURES[8:18]
VERSE2_VIOLA_MEASURES = VIOLA_MEASURES[8:18]
VERSE2_TRUMPET_MEASURES = TRUMPET_MEASURES[8:18]
VERSE2_GUITAR_MEASURES = GUITAR_MEASURES[8:18]
VERSE2_PIANO_RIGHT_MEASURES = PIANO_RIGHT_MEASURES[8:18]
VERSE2_PIANO_LEFT_MEASURES = PIANO_LEFT_MEASURES[8:18]

SHORT_REFRAIN_CHORD_LABELS = CHORD_LABELS[18:26]
SHORT_REFRAIN_VOICE_MEASURES: list[list[PitchToken]] = [
    [("a'4", "Because that goal will serve"), "b'4", "a'4", "fs'4"],
    [("e'4", "to organize and measure"), "fs'4", "a'4", "b'4"],
    [("b'4", "the best of our energies and skills"), "a'4", "fs'4", "e'4"],
    ["fs'4", "a'4", "b'4", "a'4"],
    [("a'4", "one we are willing to accept,"), "a'4", "b'4", "a'4"],
    [("e'4", "one we are unwilling to postpone,"), "fs'4", "a'4", "b'4"],
    [("a'4", "and one we intend"), "fs'4", "e'4", "fs'4"],
    [("d''2", "to win."), "r2"],
]
SHORT_REFRAIN_VIOLIN_MEASURES = VIOLIN_MEASURES[18:26]
SHORT_REFRAIN_VIOLA_MEASURES = VIOLA_MEASURES[18:26]
SHORT_REFRAIN_TRUMPET_MEASURES = TRUMPET_MEASURES[18:26]
SHORT_REFRAIN_GUITAR_MEASURES = GUITAR_MEASURES[18:26]
SHORT_REFRAIN_PIANO_RIGHT_MEASURES = PIANO_RIGHT_MEASURES[18:26]
SHORT_REFRAIN_PIANO_LEFT_MEASURES = PIANO_LEFT_MEASURES[18:26]

BRIDGE_CHORD_LABELS: list[list[tuple[str, str]]] = [
    [("1", "Bm11")],
    [("1", "Gmaj7(#11)")],
    [("1", "Dmaj9/A")],
    [("1", "A13sus4")],
    [("1", "Em9")],
    [("1", "Gmaj9")],
    [("1", "Dmaj9/F#")],
    [("1", "A7sus4")],
    [("1", "Gmaj7(#11)")],
    [("1", "A13sus4")],
    [("1", "Dadd9")],
    [("1", "Dadd9")],
]

BRIDGE_VOICE_MEASURES: list[list[PitchToken]] = [
    [("fs'4", "With this burn to the moon,"), "a'4", "b'4", "a'4"],
    [("e'4", "we do not leave Earth."), "fs'4", "a'2"],
    [("d'2", "We choose it."), "r2"],
    [("e'4", "We choose Earth."), "fs'4", "a'2"],
    [("g'4", "We will always choose Earth."), "fs'4", "e'4", "d'4"],
    [("a'4", "We will always choose each other."), "b'4", "a'4", "fs'4"],
    ["e'2", "fs'2"],
    ["a'1"],
    [("b'4", "We choose Earth."), "a'4", "fs'4", "e'4"],
    [("e'4", "We choose each other."), "fs'4", "a'2"],
    [("d''2", "We choose Earth."), "a'2"],
    ["d'1"],
]

BRIDGE_VIOLIN_MEASURES: list[list[PitchToken]] = [
    [("<b'' fs'''>1", "bridge: colder lunar-orbit shimmer")],
    ["<b'' e'''>1"],
    ["a''2", "fs''2"],
    ["e''1"],
    ["g''2", "fs''2"],
    ["b''1"],
    ["a''2", "fs''2"],
    ["e''1"],
    ["b''2", "cs'''2"],
    ["e'''2", "d'''2"],
    ["a''1"],
    ["d'''1"],
]

BRIDGE_VIOLA_MEASURES: list[list[PitchToken]] = [
    [("b1", "bridge: time loosens, warmer inner gravity")],
    ["g1"],
    ["a1"],
    ["a1"],
    ["e1"],
    ["g1"],
    ["fs1"],
    ["a1"],
    ["g2", "a2"],
    ["a1"],
    ["d1"],
    ["d1"],
]

BRIDGE_TRUMPET_MEASURES: list[list[PitchToken]] = [
    ["r1"],
    [("r2", "distant signal; very little vibrato"), "b'4", "d''4"],
    ["r1"],
    ["e''2", "d''2"],
    ["r1"],
    ["b'4", "d''8", "e''8", "fs''4", "e''4"],
    ["r1"],
    ["a'1"],
    ["r2", "b'4", "cs''4"],
    ["e''2", "d''2"],
    [("a''2", "hold back, then clear Earth call"), "fs''2"],
    ["d''1"],
]

BRIDGE_GUITAR_MEASURES: list[list[PitchToken]] = [
    [("c4", "bridge: thinner arpeggio, almost suspended"), "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c2", "c2"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c2", "c2"],
    ["c1"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c2", "c2"],
    ["c1"],
]

BRIDGE_PIANO_RIGHT_MEASURES: list[list[PitchToken]] = [
    [("<a' d'' e''>1", "bridge: sparse, open voicings")],
    ["<b' cs'' fs''>1"],
    ["<e' fs' a' cs''>1"],
    ["<g' b' cs'' fs''>1"],
    ["<g' b' d'' fs''>1"],
    ["<a' b' d'' fs''>1"],
    ["<e' fs' a' cs''>1"],
    ["<g' cs'' e''>1"],
    ["<b' cs'' fs''>1"],
    ["<g' b' cs'' fs''>1"],
    ["<e' fs' a'>1"],
    ["<a' d''>1"],
]

BRIDGE_PIANO_LEFT_MEASURES: list[list[PitchToken]] = [
    ["b,1"],
    ["g,1"],
    ["a,1"],
    ["a,1"],
    ["e,1"],
    ["g,1"],
    ["fs,1"],
    ["a,1"],
    ["g,1"],
    ["a,1"],
    ["d,1"],
    ["d,1"],
]

LOSS_CHORD_LABELS: list[list[tuple[str, str]]] = [
    [("1", "D5")],
    [("1", "Gmaj7(#11)")],
    [("1", "A13sus4")],
    [("1", "Dadd9")],
]

LOSS_VOICE_MEASURES: list[list[PitchToken]] = [
    [("r1", "loss of signal")],
    ["r1"],
    ["r1"],
    ["r1"],
]

LOSS_VIOLIN_MEASURES: list[list[PitchToken]] = [
    [("<a'' e'''>1", "far-side signal thins")],
    ["<b'' fs'''>1"],
    ["r1"],
    ["a''1"],
]

LOSS_VIOLA_MEASURES: list[list[PitchToken]] = [
    ["d'1"],
    ["g1"],
    ["a1"],
    ["d1"],
]

LOSS_TRUMPET_MEASURES: list[list[PitchToken]] = [
    ["r1"],
    [("r2", "distant, almost gone"), "a'2"],
    ["r1"],
    ["r1"],
]

LOSS_GUITAR_MEASURES: list[list[PitchToken]] = [
    [("c1", "let the signal drop out")],
    ["c1"],
    ["c1"],
    ["c1"],
]

LOSS_PIANO_RIGHT_MEASURES: list[list[PitchToken]] = [
    ["<a' d''>1"],
    ["<b' cs'' fs''>1"],
    ["<g' b' cs'' fs''>1"],
    ["<e' fs' a'>1"],
]

LOSS_PIANO_LEFT_MEASURES: list[list[PitchToken]] = [
    ["d,1"],
    ["g,1"],
    ["a,1"],
    ["d,1"],
]

OUTRO_CHORD_LABELS: list[list[tuple[str, str]]] = [
    [("1", "Dadd9")],
    [("1", "Dmaj9/F#")],
    [("1", "Gmaj9")],
    [("1", "A13sus4")],
    [("1", "Bm11")],
    [("1", "Gmaj7(#11)")],
    [("1", "Dadd9")],
    [("1", "D5")],
]

OUTRO_VOICE_MEASURES: list[list[PitchToken]] = [
    [("d'2", "We choose Earth."), "r2"],
    [("fs'4", "We choose each other."), "a'4", "fs'4", "e'4"],
    [("g'2", "We choose Earth."), "r2"],
    ["r1"],
    [("a'4", "We will always choose Earth."), "b'4", "a'4", "fs'4"],
    [("e'4", "We will always choose each other."), "fs'4", "a'2"],
    [("d''2", "We choose Earth."), "a'2"],
    ["d'1"],
]

OUTRO_VIOLIN_MEASURES: list[list[PitchToken]] = [
    ["a''1"],
    ["fs''1"],
    ["g''1"],
    ["e''1"],
    ["b''2", "a''2"],
    ["g''2", "fs''2"],
    ["a''1"],
    ["d'''1"],
]

OUTRO_VIOLA_MEASURES: list[list[PitchToken]] = [
    ["d'1"],
    ["fs1"],
    ["g1"],
    ["a1"],
    ["b1"],
    ["g1"],
    ["d'1"],
    ["d1"],
]

OUTRO_TRUMPET_MEASURES: list[list[PitchToken]] = [
    ["r1"],
    ["r1"],
    ["r2", "a'2"],
    ["r1"],
    ["b'2", "a'2"],
    ["r2", "fs'2"],
    ["a'1"],
    ["d''1"],
]

OUTRO_GUITAR_MEASURES: list[list[PitchToken]] = [
    [("c4", "simple communal pulse"), "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c4", "c4", "c4", "c4"],
    ["c2", "c2"],
    ["c1"],
]

OUTRO_PIANO_RIGHT_MEASURES: list[list[PitchToken]] = [
    ["<e' fs' a'>1"],
    ["<e' fs' a' cs''>1"],
    ["<a' b' d'' fs''>1"],
    ["<g' b' cs'' fs''>1"],
    ["<a' d'' e''>1"],
    ["<b' cs'' fs''>1"],
    ["<e' fs' a'>1"],
    ["<a' d''>1"],
]

OUTRO_PIANO_LEFT_MEASURES: list[list[PitchToken]] = [
    ["d,1"],
    ["fs,1"],
    ["g,1"],
    ["a,1"],
    ["b,1"],
    ["g,1"],
    ["d,1"],
    ["d,1"],
]

CHORD_LABELS.extend(VERSE2_CHORD_LABELS)
VOICE_MEASURES.extend(VERSE2_VOICE_MEASURES)
VIOLIN_MEASURES.extend(VERSE2_VIOLIN_MEASURES)
VIOLA_MEASURES.extend(VERSE2_VIOLA_MEASURES)
TRUMPET_MEASURES.extend(VERSE2_TRUMPET_MEASURES)
GUITAR_MEASURES.extend(VERSE2_GUITAR_MEASURES)
PIANO_RIGHT_MEASURES.extend(VERSE2_PIANO_RIGHT_MEASURES)
PIANO_LEFT_MEASURES.extend(VERSE2_PIANO_LEFT_MEASURES)

CHORD_LABELS.extend(SHORT_REFRAIN_CHORD_LABELS)
VOICE_MEASURES.extend(SHORT_REFRAIN_VOICE_MEASURES)
VIOLIN_MEASURES.extend(SHORT_REFRAIN_VIOLIN_MEASURES)
VIOLA_MEASURES.extend(SHORT_REFRAIN_VIOLA_MEASURES)
TRUMPET_MEASURES.extend(SHORT_REFRAIN_TRUMPET_MEASURES)
GUITAR_MEASURES.extend(SHORT_REFRAIN_GUITAR_MEASURES)
PIANO_RIGHT_MEASURES.extend(SHORT_REFRAIN_PIANO_RIGHT_MEASURES)
PIANO_LEFT_MEASURES.extend(SHORT_REFRAIN_PIANO_LEFT_MEASURES)

CHORD_LABELS.extend(BRIDGE_CHORD_LABELS)
VOICE_MEASURES.extend(BRIDGE_VOICE_MEASURES)
VIOLIN_MEASURES.extend(BRIDGE_VIOLIN_MEASURES)
VIOLA_MEASURES.extend(BRIDGE_VIOLA_MEASURES)
TRUMPET_MEASURES.extend(BRIDGE_TRUMPET_MEASURES)
GUITAR_MEASURES.extend(BRIDGE_GUITAR_MEASURES)
PIANO_RIGHT_MEASURES.extend(BRIDGE_PIANO_RIGHT_MEASURES)
PIANO_LEFT_MEASURES.extend(BRIDGE_PIANO_LEFT_MEASURES)

CHORD_LABELS.extend(LOSS_CHORD_LABELS)
VOICE_MEASURES.extend(LOSS_VOICE_MEASURES)
VIOLIN_MEASURES.extend(LOSS_VIOLIN_MEASURES)
VIOLA_MEASURES.extend(LOSS_VIOLA_MEASURES)
TRUMPET_MEASURES.extend(LOSS_TRUMPET_MEASURES)
GUITAR_MEASURES.extend(LOSS_GUITAR_MEASURES)
PIANO_RIGHT_MEASURES.extend(LOSS_PIANO_RIGHT_MEASURES)
PIANO_LEFT_MEASURES.extend(LOSS_PIANO_LEFT_MEASURES)

CHORD_LABELS.extend(OUTRO_CHORD_LABELS)
VOICE_MEASURES.extend(OUTRO_VOICE_MEASURES)
VIOLIN_MEASURES.extend(OUTRO_VIOLIN_MEASURES)
VIOLA_MEASURES.extend(OUTRO_VIOLA_MEASURES)
TRUMPET_MEASURES.extend(OUTRO_TRUMPET_MEASURES)
GUITAR_MEASURES.extend(OUTRO_GUITAR_MEASURES)
PIANO_RIGHT_MEASURES.extend(OUTRO_PIANO_RIGHT_MEASURES)
PIANO_LEFT_MEASURES.extend(OUTRO_PIANO_LEFT_MEASURES)


def _markup(text: str, *, bold: bool = False, italic: bool = False) -> abjad.Markup:
    command = "bold" if bold else "italic" if italic else "normal-text"
    return abjad.Markup(rf'\markup \{command} "{text}"')


def _make_leaf(token: str) -> abjad.Leaf:
    if token.startswith("r"):
        return abjad.Rest(token)
    if token.startswith("s"):
        return abjad.Skip(token)
    if token.startswith("<"):
        return abjad.Chord(token)
    return abjad.Note(token)


def _duration_of_pitch_measure(measure: Sequence[PitchToken]) -> abjad.Duration:
    duration = abjad.Duration(0)
    for item in measure:
        token = item[0] if isinstance(item, tuple) else item
        duration += abjad.get.duration(_make_leaf(token))
    return duration


def _duration_of_chord_measure(measure: Sequence[tuple[str, str]]) -> abjad.Duration:
    duration = abjad.Duration(0)
    for denominator, _ in measure:
        duration += abjad.Duration(1, int(denominator))
    return duration


def _part_measures() -> dict[str, Sequence[Sequence[PitchToken]]]:
    return {
        "voice": VOICE_MEASURES,
        "violin": VIOLIN_MEASURES,
        "viola": VIOLA_MEASURES,
        "trumpet": TRUMPET_MEASURES,
        "piano_right": PIANO_RIGHT_MEASURES,
        "piano_left": PIANO_LEFT_MEASURES,
    }


def _section_slices() -> dict[str, slice]:
    start = 0
    slices = {}
    for section_name, measure_count in SECTION_LENGTHS.items():
        stop = start + measure_count
        slices[section_name] = slice(start, stop)
        start = stop
    return slices


def _sectioned_parts() -> dict[str, dict[str, Sequence[Sequence[PitchToken]]]]:
    slices = _section_slices()
    return {
        section_name: {
            part_name: measures[section_slice]
            for part_name, measures in _part_measures().items()
        }
        for section_name, section_slice in slices.items()
    }


def _section_name_for_measure(measure_index: int) -> str:
    for section_name, section_slice in _section_slices().items():
        start = section_slice.start or 0
        stop = section_slice.stop or 0
        if start <= measure_index < stop:
            return section_name
    raise ValueError(f"measure index {measure_index} is outside declared sections")


def _section_title(section_name: str) -> str:
    return section_name.replace("_", " ").title()


def _validate_score_data() -> None:
    expected_measure_count = sum(SECTION_LENGTHS.values())
    measured_parts = {"chords": CHORD_LABELS, **_part_measures()}
    bad_counts = {
        part_name: len(measures)
        for part_name, measures in measured_parts.items()
        if len(measures) != expected_measure_count
    }
    if bad_counts:
        details = ", ".join(f"{part}={count}" for part, count in sorted(bad_counts.items()))
        raise ValueError(
            f"all parts must have {expected_measure_count} measures; found {details}"
        )

    for measure_number, measure in enumerate(CHORD_LABELS, start=1):
        duration = _duration_of_chord_measure(measure)
        if duration != abjad.Duration(1, 1):
            raise ValueError(f"chord measure {measure_number} has duration {duration}")

    for part_name, measures in _part_measures().items():
        for measure_number, measure in enumerate(measures, start=1):
            duration = _duration_of_pitch_measure(measure)
            if duration != abjad.Duration(1, 1):
                raise ValueError(
                    f"{part_name} measure {measure_number} has duration {duration}"
                )


def _token_without_duration(token: str) -> str:
    return re.sub(r"\d+\.?$", "", token)


def _token_parts(item: PitchToken) -> tuple[str, str | None, str | None]:
    if isinstance(item, tuple):
        if len(item) == 3:
            return item[0], item[1], item[2]
        return item[0], item[1], None
    return item, None, None


def _measure_tokens_for_cheat_sheet(measure: Sequence[PitchToken]) -> str:
    tokens = []
    for item in measure:
        token = item[0] if isinstance(item, tuple) else item
        tokens.append(_token_without_duration(token))
    return " / ".join(tokens)


def _chord_labels_for_cheat_sheet(measure: Sequence[tuple[str, str]]) -> str:
    return " -> ".join(label for _, label in measure)


def _transpose_chord_label_for_bflat(label: str) -> str:
    pitch_map = {
        "C": "D",
        "C#": "D#",
        "Db": "Eb",
        "D": "E",
        "D#": "E#",
        "Eb": "F",
        "E": "F#",
        "F": "G",
        "F#": "G#",
        "Gb": "Ab",
        "G": "A",
        "G#": "A#",
        "Ab": "Bb",
        "A": "B",
        "A#": "B#",
        "Bb": "C",
        "B": "C#",
    }
    match = re.match(r"^([A-G](?:#|b)?)(.*?)(?:/([A-G](?:#|b)?))?$", label)
    if match is None:
        return label
    root, quality, bass = match.groups()
    transposed = pitch_map[root] + quality
    if bass is not None:
        transposed += "/" + pitch_map[bass]
    return transposed


def _transpose_chord_labels_for_bflat(
    labels: Sequence[Sequence[tuple[str, str]]],
) -> list[list[tuple[str, str]]]:
    return [
        [(duration, _transpose_chord_label_for_bflat(label)) for duration, label in measure]
        for measure in labels
    ]


def build_chord_voicing_cheat_sheet() -> str:
    """Build a Markdown chord and piano-voicing reference from score data."""
    _validate_score_data()
    _sectioned_parts()

    lines = [
        f"# {TITLE}: Chord and Piano Voicing Cheat Sheet",
        "",
        "This reference is generated from the same measure data as the Abjad score.",
        "Chord symbols stay rehearsal-friendly while the piano staves show the color tones.",
        "",
        "| M. | Section | Chord | Piano LH | Piano RH |",
        "| ---: | --- | --- | --- | --- |",
    ]

    for measure_index, (chords, left, right) in enumerate(
        zip(CHORD_LABELS, PIANO_LEFT_MEASURES, PIANO_RIGHT_MEASURES, strict=True)
    ):
        lines.append(
            "| "
            f"{measure_index + 1} | "
            f"{_section_title(_section_name_for_measure(measure_index))} | "
            f"{_chord_labels_for_cheat_sheet(chords)} | "
            f"`{_measure_tokens_for_cheat_sheet(left)}` | "
            f"`{_measure_tokens_for_cheat_sheet(right)}` |"
        )

    lines.extend(
        [
            "",
            "## Quick Reading Notes",
            "",
            "- `Gmaj7(#11)` supplies the star-field color: the C# is the #11.",
            "- `A13sus4` keeps propulsion suspended before resolving to `A7`.",
            "- `Bm11` and `Em9` add space without making every player parse dense jazz harmony.",
            "- Piano LH gives the bass/root path; RH gives a practical voicing the pianist may vary.",
        ]
    )
    return "\n".join(lines) + "\n"


def _escape_lyric_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', r"\"")


def _lyric_text_from_annotation(text: str | None) -> str | None:
    if text is None:
        return None
    for prefix in ["spoken: ", "sung: "]:
        if text.startswith(prefix):
            return text.removeprefix(prefix)
    if text.startswith(("repeat ", "lean ", "instrumental ")):
        return None
    return text


def _is_pitched_token(token: str) -> bool:
    return not token.startswith(("r", "s"))


def _split_lyric_words(text: str) -> list[str]:
    return [word for word in text.split() if word]


def _lyrics_for_voice_measure(measure: Sequence[PitchToken]) -> list[str]:
    pitched_items = [
        item
        for item in measure
        if _is_pitched_token(_token_parts(item)[0])
    ]
    if not pitched_items:
        return []

    explicit_tokens = [_token_parts(item)[2] for item in pitched_items]
    if any(token is not None for token in explicit_tokens):
        return [
            '""' if token in {None, ""} else f'"{_escape_lyric_text(token)}"'
            for token in explicit_tokens
        ]

    lyric_text = None
    for item in pitched_items:
        if isinstance(item, tuple):
            _, annotation, _ = _token_parts(item)
            lyric_text = _lyric_text_from_annotation(annotation)
            if lyric_text:
                break

    if not lyric_text:
        return ['""' for _ in pitched_items]

    words = _split_lyric_words(lyric_text)
    lyric_tokens = []
    for index in range(len(pitched_items)):
        if index >= len(words):
            lyric_tokens.append('""')
        elif index == len(pitched_items) - 1:
            lyric_tokens.append(f'"{_escape_lyric_text(" ".join(words[index:]))}"')
        else:
            lyric_tokens.append(f'"{_escape_lyric_text(words[index])}"')
    return lyric_tokens


def _voice_lyrics_literal() -> abjad.LilyPondLiteral:
    lyric_tokens = []
    for measure in VOICE_MEASURES:
        lyric_tokens.extend(_lyrics_for_voice_measure(measure))
    return abjad.LilyPondLiteral(
        r"\addlyrics { " + " ".join(lyric_tokens) + " }",
        site="after",
    )


def _append_measures(
    container: abjad.Container,
    measures: Sequence[Sequence[PitchToken]],
    *,
    attach_annotations: bool = True,
) -> None:
    for measure in measures:
        for item in measure:
            token, text, _ = _token_parts(item)
            leaf = _make_leaf(token)
            if text and attach_annotations:
                abjad.attach(_markup(text, italic=True), leaf, direction=abjad.UP)
            container.append(leaf)


def _attach_start_indicators(
    component: abjad.Component,
    *,
    clef: str | None = None,
    dynamic: str | None = None,
    key: bool = True,
) -> None:
    first_leaf = abjad.select.leaf(component, 0)
    if first_leaf is None:
        return
    if clef is not None:
        abjad.attach(abjad.Clef(clef), first_leaf)
    if key:
        abjad.attach(abjad.KeySignature(abjad.NamedPitchClass("d"), abjad.Mode("major")), first_leaf)
    abjad.attach(abjad.TimeSignature((4, 4)), first_leaf)
    if dynamic is not None:
        abjad.attach(abjad.Dynamic(dynamic), first_leaf)


def _measure_end_leaf(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
    measure_index: int,
) -> abjad.Leaf | None:
    if measure_index >= len(measures):
        return None
    leaf_index = sum(len(measure) for measure in measures[: measure_index + 1]) - 1
    return abjad.select.leaf(component, leaf_index)


def _measure_start_leaf(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
    measure_index: int,
) -> abjad.Leaf | None:
    if measure_index >= len(measures):
        return None
    leaf_index = sum(len(measure) for measure in measures[:measure_index])
    return abjad.select.leaf(component, leaf_index)


def _attach_section_breaks(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
) -> None:
    section_ends = []
    running_total = 0
    for measure_count in list(SECTION_LENGTHS.values())[:-1]:
        running_total += measure_count
        section_ends.append(running_total - 1)
    final_leaf = abjad.select.leaf(component, -1)
    for measure_index in section_ends:
        leaf = _measure_end_leaf(component, measures, measure_index)
        if leaf is not None:
            abjad.attach(abjad.BarLine("||"), leaf)
    if final_leaf is not None:
        abjad.attach(abjad.BarLine("|."), final_leaf)


def _attach_dynamic_map(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
    part_name: str,
) -> None:
    for measure_index, dynamic in SECTION_DYNAMICS.get(part_name, {}).items():
        leaf = _measure_start_leaf(component, measures, measure_index)
        if leaf is not None:
            abjad.attach(abjad.Dynamic(dynamic), leaf)

    for start, stop in CRESCENDO_RANGES.get(part_name, []):
        start_leaf = _measure_start_leaf(component, measures, start)
        stop_leaf = _measure_end_leaf(component, measures, stop)
        if start_leaf is not None and stop_leaf is not None:
            abjad.attach(abjad.StartHairpin("<"), start_leaf)
            abjad.attach(abjad.StopHairpin(), stop_leaf)

    for start, stop in DECRESCENDO_RANGES.get(part_name, []):
        start_leaf = _measure_start_leaf(component, measures, start)
        stop_leaf = _measure_end_leaf(component, measures, stop)
        if start_leaf is not None and stop_leaf is not None:
            abjad.attach(abjad.StartHairpin(">"), start_leaf)
            abjad.attach(abjad.StopHairpin(), stop_leaf)


def _attach_system_breaks(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
    *,
    measures_per_system: int = 4,
) -> None:
    measure_count = len(measures)
    break_indices = list(range(measures_per_system - 1, measure_count - 1, measures_per_system))
    if break_indices and measure_count - break_indices[-1] - 1 == 1:
        break_indices.pop()
    for measure_index in break_indices:
        leaf = _measure_end_leaf(component, measures, measure_index)
        if leaf is not None:
            abjad.attach(abjad.LilyPondLiteral(r"\break", site="after"), leaf)


def _attach_voice_rehearsal_marks(voice: abjad.Component) -> None:
    section_starts = {}
    running_total = 0
    for section_name, measure_count in SECTION_LENGTHS.items():
        section_starts[section_name] = running_total
        running_total += measure_count

    starts = [
        (section_starts["intro"], "Intro - liftoff atmosphere"),
        (section_starts["verse_1"], "Verse 1 - spoken declaration"),
        (section_starts["refrain"], "Refrain - first sung opening"),
        (section_starts["verse_2"], "Verse 2 - new sea"),
        (section_starts["short_refrain"], "Short Refrain"),
        (section_starts["bridge"], "Bridge - We choose Earth"),
        (section_starts["loss_of_signal"], "Loss of Signal"),
        (section_starts["outro"], "Outro - choose Earth"),
    ]
    for measure_index, text in starts:
        leaf = _measure_start_leaf(voice, VOICE_MEASURES, measure_index)
        if leaf is not None:
            abjad.attach(abjad.RehearsalMark(markup=rf'\markup \box "{text}"'), leaf)


def _make_chord_context(
    labels: Sequence[Sequence[tuple[str, str]]] = CHORD_LABELS,
) -> abjad.Staff:
    context = abjad.Staff(name="ChordLabels")
    for command in [
        "Staff_symbol_engraver",
        "Clef_engraver",
        "Time_signature_engraver",
        "Bar_engraver",
    ]:
        context.remove_commands().append(command)
    for measure in labels:
        for duration, label in measure:
            skip = abjad.Skip(f"s{duration}")
            abjad.attach(_markup(label, bold=True), skip, direction=abjad.UP)
            context.append(skip)
    _attach_start_indicators(context, key=False)
    _attach_section_breaks(context, labels)
    first_leaf = abjad.select.leaf(context, 0)
    if first_leaf is not None:
        abjad.attach(abjad.InstrumentName(r'\markup "Chords"'), first_leaf)
    return context


def _make_staff(
    name: str,
    short_name: str,
    measures: Sequence[Sequence[PitchToken]],
    *,
    clef: str = "treble",
    dynamic: str | None = None,
    dynamic_part: str | None = None,
    lilypond_type: str = "Staff",
    attach_names: bool = True,
    attach_annotations: bool = True,
) -> abjad.Staff:
    staff = abjad.Staff(lilypond_type=lilypond_type, name=name)
    _append_measures(staff, measures, attach_annotations=attach_annotations)
    _attach_start_indicators(staff, clef=clef, dynamic=dynamic)
    _attach_section_breaks(staff, measures)
    if dynamic_part is not None:
        _attach_dynamic_map(staff, measures, dynamic_part)
    first_leaf = abjad.select.leaf(staff, 0)
    if attach_names and first_leaf is not None:
        abjad.attach(abjad.InstrumentName(rf'\markup "{name}"'), first_leaf)
        abjad.attach(abjad.ShortInstrumentName(rf'\markup "{short_name}"'), first_leaf)
    return staff


def _make_piano_staff() -> abjad.StaffGroup:
    right = _make_staff(
        "Piano_RH",
        "RH",
        PIANO_RIGHT_MEASURES,
        attach_names=False,
        dynamic_part="piano_right",
    )
    left = _make_staff(
        "Piano_LH",
        "LH",
        PIANO_LEFT_MEASURES,
        clef="bass",
        attach_names=False,
        dynamic_part="piano_left",
    )
    group = abjad.StaffGroup([right, left], lilypond_type="PianoStaff", name="Piano")
    first_leaf = abjad.select.leaf(right, 0)
    if first_leaf is not None:
        abjad.attach(abjad.InstrumentName(r"\markup Piano"), first_leaf)
        abjad.attach(abjad.ShortInstrumentName(r"\markup Pno."), first_leaf)
    return group


def _attach_section_rehearsal_marks(
    component: abjad.Component,
    measures: Sequence[Sequence[object]],
) -> None:
    running_total = 0
    for section_name, measure_count in SECTION_LENGTHS.items():
        leaf = _measure_start_leaf(component, measures, running_total)
        if leaf is not None:
            abjad.attach(
                abjad.RehearsalMark(markup=rf'\markup \box "{_section_title(section_name)}"'),
                leaf,
            )
        running_total += measure_count


def _make_bflat_trumpet_part_staff() -> abjad.Staff:
    staff = abjad.Staff(name="Trumpet_Bb")
    _append_measures(staff, TRUMPET_MEASURES)
    abjad.mutate.transpose(staff, "+M2")
    _attach_start_indicators(staff, clef="treble", dynamic="pp", key=False)
    first_leaf = abjad.select.leaf(staff, 0)
    if first_leaf is not None:
        abjad.attach(abjad.KeySignature(abjad.NamedPitchClass("e"), abjad.Mode("major")), first_leaf)
        abjad.attach(abjad.InstrumentName(r'\markup "Trumpet in B-flat"'), first_leaf)
        abjad.attach(abjad.ShortInstrumentName(r'\markup "Tpt. Bb"'), first_leaf)
    _attach_section_breaks(staff, TRUMPET_MEASURES)
    _attach_section_rehearsal_marks(staff, TRUMPET_MEASURES)
    return staff


def _make_part_voice_staff(*, transpose_interval: str | None = None) -> abjad.Staff:
    staff = _make_staff(
        "Voice cue",
        "Vox.",
        VOICE_MEASURES,
        dynamic_part="voice",
        attach_annotations=False,
    )
    if transpose_interval is not None:
        abjad.mutate.transpose(staff, transpose_interval)
        first_leaf = abjad.select.leaf(staff, 0)
        if first_leaf is not None:
            abjad.detach(abjad.KeySignature, first_leaf)
            abjad.attach(abjad.KeySignature(abjad.NamedPitchClass("e"), abjad.Mode("major")), first_leaf)
    _attach_voice_rehearsal_marks(staff)
    abjad.attach(_voice_lyrics_literal(), staff)
    first_leaf = abjad.select.leaf(staff, 0)
    if first_leaf is not None:
        abjad.attach(abjad.MetronomeMark(abjad.Duration(1, 4), 76), first_leaf)
    _attach_system_breaks(staff, VOICE_MEASURES)
    return staff


def _make_transposed_staff(
    name: str,
    short_name: str,
    measures: Sequence[Sequence[PitchToken]],
    *,
    transpose_interval: str,
    key_pitch: str,
    clef: str = "treble",
    dynamic: str | None = None,
    dynamic_part: str | None = None,
) -> abjad.Staff:
    staff = abjad.Staff(name=name.replace(" ", "_"))
    _append_measures(staff, measures)
    abjad.mutate.transpose(staff, transpose_interval)
    _attach_start_indicators(staff, clef=clef, dynamic=dynamic, key=False)
    if dynamic_part is not None:
        _attach_dynamic_map(staff, measures, dynamic_part)
    first_leaf = abjad.select.leaf(staff, 0)
    if first_leaf is not None:
        abjad.attach(abjad.KeySignature(abjad.NamedPitchClass(key_pitch), abjad.Mode("major")), first_leaf)
        abjad.attach(abjad.InstrumentName(rf'\markup "{name}"'), first_leaf)
        abjad.attach(abjad.ShortInstrumentName(rf'\markup "{short_name}"'), first_leaf)
    _attach_section_breaks(staff, measures)
    return staff


def _make_part_score(
    part_component: abjad.Component,
    *,
    chord_labels: Sequence[Sequence[tuple[str, str]]] = CHORD_LABELS,
    transpose_voice_interval: str | None = None,
) -> abjad.Score:
    voice = _make_part_voice_staff(transpose_interval=transpose_voice_interval)
    return abjad.Score([_make_chord_context(chord_labels), voice, part_component])


def _make_piano_part_score() -> abjad.Score:
    return _make_part_score(_make_piano_staff())


def _make_voice_part_score() -> abjad.Score:
    voice = _make_part_voice_staff()
    return abjad.Score([_make_chord_context(), voice])


def _make_score() -> abjad.Score:
    voice = _make_staff(
        "Voice",
        "Vox.",
        VOICE_MEASURES,
        dynamic_part="voice",
        attach_annotations=False,
    )
    _attach_voice_rehearsal_marks(voice)
    abjad.attach(_voice_lyrics_literal(), voice)
    first_voice_leaf = abjad.select.leaf(voice, 0)
    if first_voice_leaf is not None:
        abjad.attach(abjad.MetronomeMark(abjad.Duration(1, 4), 76), first_voice_leaf)
    _attach_system_breaks(voice, VOICE_MEASURES)

    violin = _make_staff("Violin", "Vln.", VIOLIN_MEASURES, dynamic_part="violin")
    viola = _make_staff("Viola", "Vla.", VIOLA_MEASURES, clef="alto", dynamic_part="viola")
    trumpet = _make_staff("Trumpet in C", "Tpt.", TRUMPET_MEASURES, dynamic_part="trumpet")
    color_group = abjad.StaffGroup([violin, viola, trumpet], name="Color")

    return abjad.Score(
        [
            _make_chord_context(),
            voice,
            color_group,
            _make_piano_staff(),
        ],
        name="Score",
    )


def _make_paper_block() -> abjad.Block:
    paper_block = abjad.Block(name="paper")
    paper_block.items.extend(
        [
            r"top-margin = 14\mm",
            r"bottom-margin = 14\mm",
            r"left-margin = 16\mm",
            r"right-margin = 16\mm",
            r"indent = 18\mm",
            r"short-indent = 10\mm",
            "ragged-last = ##t",
        ]
    )
    return paper_block


def _make_header_block(*, subtitle: str | None = None) -> abjad.Block:
    header_block = abjad.Block(name="header")
    header_block.items.append(rf'title = "{TITLE}"')
    if subtitle is not None:
        header_block.items.append(rf'subtitle = "{subtitle}"')
    header_block.items.append(rf'composer = "{COMPOSER}"')
    header_block.items.append("tagline = ##f")
    return header_block


def build_lilypond_file():
    """Build the first lead-score sketch for the art song."""
    _validate_score_data()

    layout_block = abjad.Block(name="layout")
    score_block = abjad.Block(name="score")
    score_block.items.extend([_make_score(), layout_block, abjad.Block(name="midi")])

    return abjad.LilyPondFile(
        items=[
            "#(set-global-staff-size 14)",
            _make_paper_block(),
            _make_header_block(),
            score_block,
        ]
    )


def build_trumpet_bflat_part_lilypond_file():
    """Build a transposed B-flat trumpet part from the concert score data."""
    return build_part_lilypond_file("trumpet-bb")


def build_part_lilypond_file(part: str):
    """Build a performer part with chord symbols and a vocal cue line."""
    _validate_score_data()
    part_builders = {
        "voice": lambda: _make_voice_part_score(),
        "violin": lambda: _make_part_score(
            _make_staff("Violin", "Vln.", VIOLIN_MEASURES, dynamic_part="violin")
        ),
        "viola": lambda: _make_part_score(
            _make_staff("Viola", "Vla.", VIOLA_MEASURES, clef="alto", dynamic_part="viola")
        ),
        "trumpet-c": lambda: _make_part_score(
            _make_staff("Trumpet in C", "Tpt.", TRUMPET_MEASURES, dynamic_part="trumpet")
        ),
        "trumpet-bb": lambda: _make_part_score(
            _make_transposed_staff(
                "Trumpet in B-flat",
                "Tpt. Bb",
                TRUMPET_MEASURES,
                transpose_interval="+M2",
                key_pitch="e",
                dynamic_part="trumpet",
            ),
            chord_labels=_transpose_chord_labels_for_bflat(CHORD_LABELS),
            transpose_voice_interval="+M2",
        ),
        "piano": _make_piano_part_score,
    }
    subtitles = {
        "voice": "Voice part",
        "violin": "Violin part",
        "viola": "Viola part",
        "trumpet-c": "Trumpet in C part",
        "trumpet-bb": "Trumpet in B-flat part",
        "piano": "Piano part",
    }
    if part not in part_builders:
        allowed = ", ".join(sorted(part_builders))
        raise ValueError(f"unknown part {part!r}; expected one of: {allowed}")

    score = part_builders[part]()
    score_block = abjad.Block(name="score")
    score_block.items.extend([score, abjad.Block(name="layout")])
    return abjad.LilyPondFile(
        items=[
            "#(set-global-staff-size 16)",
            _make_paper_block(),
            _make_header_block(subtitle=subtitles[part]),
            score_block,
        ]
    )
