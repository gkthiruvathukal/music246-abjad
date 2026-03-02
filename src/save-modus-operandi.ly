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
  f4\p( ees d c) |
  bes4( c d\< ees\!) |
  f4( g\< aes bes\!) |
  c4\mf( bes aes g) |
  f4\p( ees d c) |
  d4(\< ees f g\!) |
  aes4\mf( bes c d) |
  ees4(\> d c bes\!) |
  c4\mp( d ees f) |
  g4-_ f-_ ees-_ d-_ |
  ees4\p( d) c( bes) |
  c4( d ees\< f\!) |
  g4\mf( aes bes c) |
  d4(\> c bes aes\!) |
  g4\mp( f ees d) |
  c4\p( bes aes\> g\!) \bar "||"
}

leftHandA = \relative c {
  \clef bass
  \key f \dorian
  \time 4/4
  f2\p( c') | f,2( bes) |
  f2( c') | bes2( f') |
  f,2( c') | bes2( f) |
  c'2( f,) | bes2( c) |
  f,2( ees') | c2( f,) |
  bes2( f) | c'2( ees,) |
  f2( c') | bes2( f') |
  c2( bes) | f2\> ( c'\p) \bar "||"
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
  
  f8\mf( ges aes bes c des) |
  ees8( des c\> bes aes ges\!) |
  f8\f( ges aes bes c8. des16) |
  ees4.\sf ~ ees8( des c) |
  bes8(\> aes ges f ees des\!) |
  c8\mf( des ees f ges aes) |
  bes8( c des ees\< f ges\!) |
  aes4.\ff ~ aes8( ges f) |
  ees8\p( des c bes aes ges) |
  f4. ~ f8 r r |
  ges8\mf( aes bes c des ees) |
  f8\f( ges aes8. bes16 c8 des) |
  ees8-! ees-! ees-! des4.-> |
  c8(\> bes aes ges f ees\!) |
  des8\mp( ees f ges\< aes bes\!) |
  c4.\mf ~ c8 r r 
  
  \ottava #0  % Return to normal pitch at the double bar
  \bar "||"
}


leftHandB = \relative c {
  \clef bass
  \key f \phrygian
  \time 6/8
  f4.\mf( c') | ges4.( f) |
  f4.( c') | c4.( ges') |
  f,4.( ees') | des4.( f,) |
  c'4.( ges') | f,4.( f') |
  f,4.\p( c') | ges4. r |
  f4.\mf( des') | ges,4.( c) |
  f,4.( ees') | des4.( ges,) |
  c4.\mp( f,) | c'4.\mf r \bar "||"
}

% ============================================================
% SECTION C — F Lydian, 4/4, Andante tranquillo
% ============================================================

rightHandC = \relative c' {  % Changed to c' so notes sit lower on the staff
  \clef treble
  \key f \lydian
  \time 4/4
  \tempo "Andante tranquillo" 4 = 76
  
  f4\p( g a b) |
  c4( b a g) |
  a4( b c d) |
  e4\mp( d c\> b\!) |
  a4\p( g f e) |
  g4( a b\< c\!) |
  d4\mp( e f g) |
  a4(\> g f e\!) |
  d4\p( e f g) |

  \ottava #1  % Notes will now sound one octave higher than written
  a4( b c d) |
  e4\mp(\< f g a\!) |
  b4\mf( a g\> f\!) |
  e4\mp( d c b) |
  a4\p( g f e) |
  d4\pp( e f\> g\!) |
  f1\ppp 
  
  \ottava #0  % Return to normal if continuing further
  \bar "|."
}

leftHandC = \relative c' {
  \clef treble  % Changed from bass to treble
  \key f \lydian
  \time 4/4
  f2\p( c') | g2( f) |
  c'2( f,) | g2\mp( a) |
  f2( c') | g2\p( f) |
  c'2( g) | f2( e') |
  d2\p( c) | g2( f) |
  c'2\mp( g) | f2( c') |
  e,2\p( f) | c'2( g) |
  f2\pp( c') | f,1\ppp \bar "|."
}


% ============================================================
% Construct the final score as three movements
% ============================================================

% --- Movement I: Section A — F Dorian ---
\score {
  <<
    % --- Piano ---
    \new PianoStaff \with {
      instrumentName = "Piano"
      shortInstrumentName = ""
    } <<
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \rightHandA
      }
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \leftHandA
      }
    >>
  >>

  \layout {
    indent = 0
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

\pageBreak

% --- Movement II: Section B — F Phrygian ---
\score {
  <<
    % --- Piano ---
    \new PianoStaff \with {
      instrumentName = "Piano"
      shortInstrumentName = ""
    } <<
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \rightHandB
      }
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \leftHandB
      }
    >>
  >>

  \layout {
    indent = 0
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
    }
    ragged-last = ##t
  }

  \midi {
    \tempo 4. = 80
  }
}

\pageBreak

% --- Movement III: Section C — F Lydian ---
\score {
  <<
    % --- Piano ---
    \new PianoStaff \with {
      instrumentName = "Piano"
      shortInstrumentName = ""
    } <<
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \rightHandC
      }
      \new Staff \with { midiInstrument = "acoustic grand" } {
        \leftHandC
      }
    >>
  >>

  \layout {
    indent = 0
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
    }
    ragged-last = ##t
  }

  \midi {
    \tempo 4 = 76
  }
}

