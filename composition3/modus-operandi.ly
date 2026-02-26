\version "2.24.0"

\header {
  title = "Modus Operandi for Piano"
  composer = "George K. Thiruvathukal"
  subtitle = "A Monody built using Lilypond and Abjad"
  tagline = ##f
}

% ============================================================
% SECTION A — F Dorian, 4/4, Lento
% ============================================================

rightHandA = \relative c' {
  \clef treble
  \key f \dorian
  \time 4/4
  \tempo "Lento" 4 = 46
  \p
  f4( ees d c) |
  bes4( c d\< ees\!) |
  f4( g\< aes bes\!) |
  \mf c4( bes aes g) |
  \p f4( ees d c) |
  d4(\< ees f g\!) |
  \mf aes4( bes c d) |
  ees4(\> d c bes\!) |
  \mp c4( d ees f) |
  g4-_ f-_ ees-_ d-_ |
  \p ees4( d) c( bes) |
  c4( d ees\< f\!) |
  \mf g4( aes bes c) |
  d4(\> c bes aes\!) |
  \mp g4( f ees d) |
  \p c4( bes aes\> g\!) \bar "||"
}

leftHandA = \relative c {
  \clef bass
  \key f \dorian
  \time 4/4
  \p
  f2( c') | f,2( bes) |
  f2( c') | bes2( f') |
  f,2( c') | bes2( f) |
  c'2( f,) | bes2( c) |
  f,2( ees') | c2( f,) |
  bes2( f) | c'2( ees,) |
  f2( c') | bes2( f') |
  c2( bes) | f2( c'\>) \p \bar "||"
}

% ============================================================
% SECTION B — F Phrygian, 6/8, Presto agitato
% ============================================================

rightHandB = \relative c'' {
  \clef treble
  \key f \phrygian
  \time 6/8
  \tempo "Presto agitato" 4. = 80
  
  \ottava #1  % Start Octave Up notation here
  
  \mf
  f8( ges aes bes c des) |
  ees8( des c\> bes aes ges\!) |
  \f f8( ges aes bes c8. des16) |
  ees4.\sf ~ ees8( des c) |
  bes8(\> aes ges f ees des\!) |
  \mf c8( des ees f ges aes) |
  bes8( c des ees\< f ges\!) |
  \ff aes4. ~ aes8( ges f) |
  \p ees8( des c bes aes ges) |
  f4. ~ f8 r r |
  \mf ges8( aes bes c des ees) |
  \f f8( ges aes8. bes16 c8 des) |
  ees8-! ees-! ees-! des4.-> |
  c8(\> bes aes ges f ees\!) |
  \mp des8( ees f ges\< aes bes\!) |
  \mf c4. ~ c8 r r 
  
  \ottava #0  % Return to normal pitch at the double bar
  \bar "||"
}


leftHandB = \relative c {
  \clef bass
  \key f \phrygian
  \time 6/8
  \mf
  f4.( c') | ges4.( f) |
  f4.( c') | c4.( ges') |
  f,4.( ees') | des4.( f,) |
  c'4.( ges') | f,4.( f') |
  \p f,4.( c') | ges4. r |
  \mf f4.( des') | ges,4.( c) |
  f,4.( ees') | des4.( ges,) |
  \mp c4.( f,) | \mf c'4. r \bar "||"
}

% ============================================================
% SECTION C — F Lydian, 4/4, Andante tranquillo
% ============================================================

rightHandC = \relative c' {  % Changed to c' so notes sit lower on the staff
  \clef treble
  \key f \lydian
  \time 4/4
  \tempo "Andante tranquillo" 4 = 76
  
  \p
  f4( g a b) |
  c4( b a g) |
  a4( b c d) |
  \mp e4( d c\> b\!) |
  \p a4( g f e) |
  g4( a b\< c\!) |
  \mp d4( e f g) |
  a4(\> g f e\!) |
  \p d4( e f g) |

  \ottava #1  % Notes will now sound one octave higher than written
  a4( b c d) |
  \mp e4(\< f g a\!) |
  \mf b4( a g\> f\!) |
  \mp e4( d c b) |
  \p a4( g f e) |
  \pp d4( e f\> g\!) |
  \ppp f1 
  
  \ottava #0  % Return to normal if continuing further
  \bar "|."
}

leftHandC = \relative c' {
  \clef treble  % Changed from bass to treble
  \key f \lydian
  \time 4/4
  \p
  f2( c') | g2( f) |
  c'2( f,) | \mp g2( a) |
  f2( c') | \p g2( f) |
  c'2( g) | f2( e') |
  \p d2( c) | g2( f) |
  \mp c'2( g) | f2( c') |
  \p e,2( f) | c'2( g) |
  \pp f2( c') | \ppp f,1 \bar "|."
}

violaA = \relative c {
  \clef tenor
  \key f \dorian
  \time 4/4
  \p
  f2( c') | f,2( bes) |
  f2( c') | bes2( f') |
  f,2( c') | bes2( f) |
  c'2( f,) | bes2( c) |
  f,2( ees') | c2( f,) |
  bes2( f) | c'2( ees,) |
  f2( c') | bes2( f') |
  c2( bes) | f2( c'\>) \p \bar "||"
}

violaB = \relative c {
  \clef tenor
  \key f \phrygian
  \time 6/8
  \mf
  f4.( c') | ges4.( f) |
  f4.( c') | c4.( ges') |
  f,4.( ees') | des4.( f,) |
  c'4.( ges') | f,4.( f') |
  \p f,4.( c') | ges4. r |
  \mf f4.( des') | ges,4.( c) |
  f,4.( ees') | des4.( ges,) |
  \mp c4.( f,) | \mf c'4. r \bar "||"
}

violaC = \relative c' {
  \clef tenor
  \key f \lydian
  \time 4/4
  \p
  f2( c') | g2( f) |
  c'2( f,) | \mp g2( a) |
  f2( c') | \p g2( f) |
  c'2( g) | f2( e') |
  \p d2( c) | g2( f) |
  \mp c'2( g) | f2( c') |
  \p e,2( f) | c'2( g) |
  \pp f2( c') | \ppp f,1 \bar "|."
}


% ============================================================
% Construct the final score! 
% ============================================================

\score {
  <<
    % --- Viola ---
    \new Staff \with {
      instrumentName = "Viola"
      shortInstrumentName = "Vla."
      midiInstrument = "viola"
    } {
      \violaA
      \violaB
      \violaC
    }

    % --- Piano ---
    \new PianoStaff \with {
      instrumentName = "Piano"
      shortInstrumentName = "Pno."
    } <<
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \rightHandA
        \rightHandB
        \rightHandC
      }
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \leftHandA
        \leftHandB
        \leftHandC
      }
    >>
  >>

  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
    }
    ragged-last = ##t
  }

  \midi {
    \tempo 4 = 46
  }
}

