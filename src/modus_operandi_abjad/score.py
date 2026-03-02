"""
Score construction for Modus Operandi for Piano.

Three movements:
  I.   F Dorian  — Lento (4/4)
  II.  F Phrygian — Presto agitato (6/8)
  III. F Lydian  — Andante tranquillo (4/4)
"""

import abjad


# ============================================================
# Helper to build a movement score block
# ============================================================


def make_movement(rh_voice, lh_voice, tempo_midi_string):
    """Wrap right-hand and left-hand staves into a PianoStaff inside a score block."""
    upper = abjad.Staff([rh_voice], name="RH")
    lower = abjad.Staff([lh_voice], name="LH")

    piano_staff = abjad.StaffGroup(
        [upper, lower],
        lilypond_type="PianoStaff",
        name="PianoStaff",
    )
    abjad.setting(piano_staff).instrumentName = '"Piano"'
    abjad.setting(piano_staff).shortInstrumentName = '""'

    score = abjad.Score([piano_staff], name="Score")

    # Layout block
    layout = abjad.Block("layout")
    layout.items.append("indent = 0")
    layout.items.append("ragged-last = ##t")
    context_block = abjad.Block("context")
    context_block.items.append(r"\Score")
    context_block.items.append(
        r"\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)"
    )
    layout.items.append(context_block)

    # MIDI block
    midi = abjad.Block("midi")
    midi.items.append(tempo_midi_string)

    # Score block
    score_block = abjad.Block("score")
    score_block.items.append(score)
    score_block.items.append(layout)
    score_block.items.append(midi)

    return score_block


# ============================================================
# Movement I — F Dorian, 4/4, Lento
# ============================================================


def make_movement_i():
    # ---- Right Hand ----
    rh = abjad.Voice(name="RH_Voice")

    # Key, time, tempo, clef
    rh_notes = abjad.Container()

    # Bar 1: f4\p( ees d c)
    bar = abjad.Container("f'4 ef'4 d'4 c'4")
    abjad.attach(abjad.Clef("treble"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("dorian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((4, 4)), bar[0])
    abjad.attach(
        abjad.MetronomeMark(
            reference_duration=abjad.Duration(1, 4),
            units_per_minute=46,
            textual_indication="Lento",
        ),
        bar[0],
    )
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 2: bes4( c d\< ees\!)
    bar = abjad.Container("bf'4 c'4 d'4 ef'4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 3: f4( g\< aes bes\!)
    bar = abjad.Container("f'4 g'4 af'4 bf'4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[1])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 4: c4\mf( bes aes g)
    bar = abjad.Container("c''4 bf'4 af'4 g'4")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 5: f4\p( ees d c)
    bar = abjad.Container("f'4 ef'4 d'4 c'4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 6: d4(\< ees f g\!)
    bar = abjad.Container("d'4 ef'4 f'4 g'4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 7: aes4\mf( bes c d)
    bar = abjad.Container("af'4 bf'4 c''4 d''4")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 8: ees4(\> d c bes\!)
    bar = abjad.Container("ef''4 d''4 c''4 bf'4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 9: c4\mp( d ees f)
    bar = abjad.Container("c''4 d''4 ef''4 f''4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 10: g4-_ f-_ ees-_ d-_
    bar = abjad.Container("g''4 f''4 ef''4 d''4")
    for note in bar:
        abjad.attach(abjad.Articulation("tenuto"), note)
    rh_notes.append(bar)

    # Bar 11: ees4\p( d) c( bes)
    bar = abjad.Container("ef''4 d''4 c''4 bf'4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    abjad.attach(abjad.StartSlur(), bar[2])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 12: c4( d ees\< f\!)
    bar = abjad.Container("c''4 d''4 ef''4 f''4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 13: g4\mf( aes bes c)
    bar = abjad.Container("g''4 af''4 bf''4 c'''4")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 14: d4(\> c bes aes\!)
    bar = abjad.Container("d'''4 c'''4 bf''4 af''4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 15: g4\mp( f ees d)
    bar = abjad.Container("g''4 f''4 ef''4 d''4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 16: c4\p( bes aes\> g\!) \bar "||"
    bar = abjad.Container("c''4 bf'4 af'4 g'4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    abjad.attach(abjad.BarLine("||"), bar[3])
    rh_notes.append(bar)

    for comp in rh_notes:
        rh.append(comp)

    # ---- Left Hand ----
    lh = abjad.Voice(name="LH_Voice")
    lh_notes = abjad.Container()

    # Bar 1: f2\p( c')
    bar = abjad.Container("f2 c'2")
    abjad.attach(abjad.Clef("bass"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("dorian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((4, 4)), bar[0])
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 2: f,2( bes)
    bar = abjad.Container("f2 bf2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 3: f2( c')
    bar = abjad.Container("f2 c'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 4: bes2( f')
    bar = abjad.Container("bf2 f'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 5: f,2( c')
    bar = abjad.Container("f2 c'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 6: bes2( f)
    bar = abjad.Container("bf2 f2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 7: c'2( f,)
    bar = abjad.Container("c'2 f2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 8: bes2( c)
    bar = abjad.Container("bf2 c2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 9: f,2( ees')
    bar = abjad.Container("f2 ef'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 10: c2( f,)
    bar = abjad.Container("c2 f,2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 11: bes2( f)
    bar = abjad.Container("bf2 f2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 12: c'2( ees,)
    bar = abjad.Container("c'2 ef2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 13: f2( c')
    bar = abjad.Container("f2 c'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 14: bes2( f')
    bar = abjad.Container("bf2 f'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 15: c2( bes)
    bar = abjad.Container("c2 bf2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 16: f2\>( c'\p) \bar "||"
    bar = abjad.Container("f2 c'2")
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.Dynamic("p"), bar[1])
    abjad.attach(abjad.StopSlur(), bar[1])
    abjad.attach(abjad.BarLine("||"), bar[1])
    lh_notes.append(bar)

    for comp in lh_notes:
        lh.append(comp)

    return make_movement(rh, lh, r"\tempo 4 = 46")


# ============================================================
# Movement II — F Phrygian, 6/8, Presto agitato
# ============================================================


def make_movement_ii():
    # ---- Right Hand ----
    rh = abjad.Voice(name="RH_Voice")
    rh_notes = abjad.Container()

    # Bar 1: f8\mf( ges aes bes c des)
    bar = abjad.Container("f''8 gf''8 af''8 bf''8 c'''8 df'''8")
    abjad.attach(abjad.Clef("treble"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("phrygian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((6, 8)), bar[0])
    abjad.attach(
        abjad.MetronomeMark(
            reference_duration=abjad.Duration(3, 8),
            units_per_minute=80,
            textual_indication='"Presto agitato"',
        ),
        bar[0],
    )
    abjad.attach(abjad.Ottava(n=1), bar[0])
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 2: ees8( des c\> bes aes ges\!)
    bar = abjad.Container("ef'''8 df'''8 c'''8 bf''8 af''8 gf''8")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[5])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 3: f8\f( ges aes bes c8. des16)
    bar = abjad.Container("f''8 gf''8 af''8 bf''8 c'''8. df'''16")
    abjad.attach(abjad.Dynamic("f"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 4: ees4.\sf ~ ees8( des c)
    bar = abjad.Container("ef'''4. ef'''8 df'''8 c'''8")
    abjad.attach(abjad.Dynamic("sf"), bar[0])
    abjad.attach(abjad.Tie(), bar[0])
    abjad.attach(abjad.StartSlur(), bar[1])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 5: bes8(\> aes ges f ees des\!)
    bar = abjad.Container("bf''8 af''8 gf''8 f''8 ef''8 df''8")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[5])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 6: c8\mf( des ees f ges aes)
    bar = abjad.Container("c''8 df''8 ef''8 f''8 gf''8 af''8")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 7: bes8( c des ees\< f ges\!)
    bar = abjad.Container("bf''8 c'''8 df'''8 ef'''8 f'''8 gf'''8")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[3])
    abjad.attach(abjad.StopHairpin(), bar[5])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 8: aes4.\ff ~ aes8( ges f)
    bar = abjad.Container("af'''4. af'''8 gf'''8 f'''8")
    abjad.attach(abjad.Dynamic("ff"), bar[0])
    abjad.attach(abjad.Tie(), bar[0])
    abjad.attach(abjad.StartSlur(), bar[1])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 9: ees8\p( des c bes aes ges)
    bar = abjad.Container("ef'''8 df'''8 c'''8 bf''8 af''8 gf''8")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 10: f4. ~ f8 r r
    bar = abjad.Container("f''4. f''8 r8 r8")
    abjad.attach(abjad.Tie(), bar[0])
    rh_notes.append(bar)

    # Bar 11: ges8\mf( aes bes c des ees)
    bar = abjad.Container("gf''8 af''8 bf''8 c'''8 df'''8 ef'''8")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 12: f8\f( ges aes8. bes16 c8 des)
    bar = abjad.Container("f'''8 gf'''8 af'''8. bf'''16 c''''8 df''''8")
    abjad.attach(abjad.Dynamic("f"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 13: ees8-! ees-! ees-! des4.->
    bar = abjad.Container("ef''''8 ef''''8 ef''''8 df''''4.")
    abjad.attach(abjad.Articulation("staccatissimo"), bar[0])
    abjad.attach(abjad.Articulation("staccatissimo"), bar[1])
    abjad.attach(abjad.Articulation("staccatissimo"), bar[2])
    abjad.attach(abjad.Articulation("accent"), bar[3])
    rh_notes.append(bar)

    # Bar 14: c8(\> bes aes ges f ees\!)
    bar = abjad.Container("c''''8 bf'''8 af'''8 gf'''8 f'''8 ef'''8")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[5])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 15: des8\mp( ees f ges\< aes bes\!)
    bar = abjad.Container("df'''8 ef'''8 f'''8 gf'''8 af'''8 bf'''8")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[3])
    abjad.attach(abjad.StopHairpin(), bar[5])
    abjad.attach(abjad.StopSlur(), bar[5])
    rh_notes.append(bar)

    # Bar 16: c4.\mf ~ c8 r r  \ottava #0  \bar "||"
    bar = abjad.Container("c''''4. c''''8 r8 r8")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.Tie(), bar[0])
    abjad.attach(abjad.Ottava(n=0, site="after"), bar[3])
    abjad.attach(abjad.BarLine("||"), bar[3])
    rh_notes.append(bar)

    for comp in rh_notes:
        rh.append(comp)

    # ---- Left Hand ----
    lh = abjad.Voice(name="LH_Voice")
    lh_notes = abjad.Container()

    # Bar 1: f4.\mf( c')
    bar = abjad.Container("f4. c'4.")
    abjad.attach(abjad.Clef("bass"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("phrygian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((6, 8)), bar[0])
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 2: ges4.( f)
    bar = abjad.Container("gf4. f4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 3: f4.( c')
    bar = abjad.Container("f4. c'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 4: c4.( ges')
    bar = abjad.Container("c4. gf'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 5: f,4.( ees')
    bar = abjad.Container("f,4. ef'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 6: des4.( f,)
    bar = abjad.Container("df4. f,4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 7: c'4.( ges')
    bar = abjad.Container("c'4. gf'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 8: f,4.( f')
    bar = abjad.Container("f,4. f'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 9: f,4.\p( c')
    bar = abjad.Container("f,4. c'4.")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 10: ges4. r
    bar = abjad.Container("gf4. r4.")
    lh_notes.append(bar)

    # Bar 11: f4.\mf( des')
    bar = abjad.Container("f4. df'4.")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 12: ges,4.( c)
    bar = abjad.Container("gf,4. c4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 13: f,4.( ees')
    bar = abjad.Container("f,4. ef'4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 14: des4.( ges,)
    bar = abjad.Container("df4. gf,4.")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 15: c4.\mp( f,)
    bar = abjad.Container("c4. f,4.")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 16: c'4.\mf r \bar "||"
    bar = abjad.Container("c'4. r4.")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.BarLine("||"), bar[1])
    lh_notes.append(bar)

    for comp in lh_notes:
        lh.append(comp)

    return make_movement(rh, lh, r"\tempo 4. = 80")


# ============================================================
# Movement III — F Lydian, 4/4, Andante tranquillo
# ============================================================


def make_movement_iii():
    # ---- Right Hand ----
    rh = abjad.Voice(name="RH_Voice")
    rh_notes = abjad.Container()

    # Bar 1: f4\p( g a b)
    bar = abjad.Container("f'4 g'4 a'4 b'4")
    abjad.attach(abjad.Clef("treble"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("lydian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((4, 4)), bar[0])
    abjad.attach(
        abjad.MetronomeMark(
            reference_duration=abjad.Duration(1, 4),
            units_per_minute=76,
            textual_indication='"Andante tranquillo"',
        ),
        bar[0],
    )
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 2: c4( b a g)
    bar = abjad.Container("c''4 b'4 a'4 g'4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 3: a4( b c d)
    bar = abjad.Container("a'4 b'4 c''4 d''4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 4: e4\mp( d c\> b\!)
    bar = abjad.Container("e''4 d''4 c''4 b'4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 5: a4\p( g f e)
    bar = abjad.Container("a'4 g'4 f'4 e'4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 6: g4( a b\< c\!)
    bar = abjad.Container("g'4 a'4 b'4 c''4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 7: d4\mp( e f g)
    bar = abjad.Container("d''4 e''4 f''4 g''4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 8: a4(\> g f e\!)
    bar = abjad.Container("a''4 g''4 f''4 e''4")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 9: d4\p( e f g)
    bar = abjad.Container("d''4 e''4 f''4 g''4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 10: \ottava #1  a4( b c d)
    bar = abjad.Container("a''4 b''4 c'''4 d'''4")
    abjad.attach(abjad.Ottava(n=1), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 11: e4\mp(\< f g a\!)
    bar = abjad.Container("e'''4 f'''4 g'''4 a'''4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin("<"), bar[0])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 12: b4\mf( a g\> f\!)
    bar = abjad.Container("b'''4 a'''4 g'''4 f'''4")
    abjad.attach(abjad.Dynamic("mf"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 13: e4\mp( d c b)
    bar = abjad.Container("e'''4 d'''4 c'''4 b''4")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 14: a4\p( g f e)
    bar = abjad.Container("a''4 g''4 f''4 e''4")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 15: d4\pp( e f\> g\!)
    bar = abjad.Container("d''4 e''4 f''4 g''4")
    abjad.attach(abjad.Dynamic("pp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StartHairpin(">"), bar[2])
    abjad.attach(abjad.StopHairpin(), bar[3])
    abjad.attach(abjad.StopSlur(), bar[3])
    rh_notes.append(bar)

    # Bar 16: f1\ppp  \ottava #0  \bar "|."
    bar = abjad.Container("f''1")
    abjad.attach(abjad.Dynamic("ppp"), bar[0])
    abjad.attach(abjad.Ottava(n=0, site="after"), bar[0])
    abjad.attach(abjad.BarLine("|."), bar[0])
    rh_notes.append(bar)

    for comp in rh_notes:
        rh.append(comp)

    # ---- Left Hand ----
    lh = abjad.Voice(name="LH_Voice")
    lh_notes = abjad.Container()

    # Bar 1: f2\p( c')
    bar = abjad.Container("f'2 c''2")
    abjad.attach(abjad.Clef("treble"), bar[0])
    abjad.attach(
        abjad.KeySignature(abjad.NamedPitchClass("f"), abjad.Mode("lydian")), bar[0]
    )
    abjad.attach(abjad.TimeSignature((4, 4)), bar[0])
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 2: g2( f)
    bar = abjad.Container("g'2 f'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 3: c'2( f,)
    bar = abjad.Container("c''2 f'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 4: g2\mp( a)
    bar = abjad.Container("g'2 a'2")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 5: f2( c')
    bar = abjad.Container("f'2 c''2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 6: g2\p( f)
    bar = abjad.Container("g'2 f'2")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 7: c'2( g)
    bar = abjad.Container("c''2 g'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 8: f2( e')
    bar = abjad.Container("f'2 e''2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 9: d2\p( c)
    bar = abjad.Container("d''2 c''2")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 10: g2( f)
    bar = abjad.Container("g'2 f'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 11: c'2\mp( g)
    bar = abjad.Container("c''2 g'2")
    abjad.attach(abjad.Dynamic("mp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 12: f2( c')
    bar = abjad.Container("f'2 c''2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 13: e,2\p( f)
    bar = abjad.Container("e'2 f'2")
    abjad.attach(abjad.Dynamic("p"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 14: c'2( g)
    bar = abjad.Container("c''2 g'2")
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 15: f2\pp( c')
    bar = abjad.Container("f'2 c''2")
    abjad.attach(abjad.Dynamic("pp"), bar[0])
    abjad.attach(abjad.StartSlur(), bar[0])
    abjad.attach(abjad.StopSlur(), bar[1])
    lh_notes.append(bar)

    # Bar 16: f1\ppp \bar "|."
    bar = abjad.Container("f'1")
    abjad.attach(abjad.Dynamic("ppp"), bar[0])
    abjad.attach(abjad.BarLine("|."), bar[0])
    lh_notes.append(bar)

    for comp in lh_notes:
        lh.append(comp)

    return make_movement(rh, lh, r"\tempo 4 = 76")


def build_lilypond_file():
    """Assemble the full LilyPondFile from all three movements."""
    header = abjad.Block("header")
    header.items.append(r'title = "Modus Operandi for Piano"')
    header.items.append(r'composer = "George K. Thiruvathukal"')
    header.items.append(r'subtitle = "A Monody built using Lilypond and Abjad"')
    header.items.append(r"tagline = ##f")

    movement_i = make_movement_i()
    movement_ii = make_movement_ii()
    movement_iii = make_movement_iii()

    return abjad.LilyPondFile(
        items=[
            header,
            movement_i,
            r"\pageBreak",
            movement_ii,
            r"\pageBreak",
            movement_iii,
        ],
    )
