import music21
from music21 import converter
from music21.tempo import MetronomeMark
from music21.chord import Chord
from music21.note import Rest
from music21.note import Note
from music21.duration import Duration
from music21.stream import Stream
from music21.interval import notesToChromatic


# How bad a interval sounds (given number of semitones)
CHROMATIC_PENALTY = {
  0: 0,
  1: -2,
  2: -1,
  3: 0,
  4: 0,
  5: 0,
  6: -2,
}

def chord_search(notes):
  """Attempt to find the best chord to match a set of notes"""
  best_chord, best_score = C_MAJOR, -1000

  for chord in ALL_CHORDS:
    chord_score = 0
    for note1 in chord:
      note1 = Note(note1)
      for note2 in notes:
        chromatic_distance = notesToChromatic(note1, note2).semitones

        # Normalize distance to be between 0 and 6
        chromatic_distance = chromatic_distance % 12
        if chromatic_distance > 6:
          chromatic_distance = 12 - chromatic_distance

        chord_score += CHROMATIC_PENALTY[chromatic_distance]

    if chord_score > best_score:
      best_score = chord_score
      best_chord = chord

  print best_chord
  return best_chord


# If Only by JJ Lin
JJ_LIN_MELODY = """
tinynotation: 4/4
r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
f1
"""

WHOLE_NOTE = Duration(4.0)

C_MAJOR = ["c3", "e3", "g3", "c4"]
G_MAJOR = ["g2", "b2", "d3", "g3"]
A_MINOR = ["a2", "c3", "e3", "a3"]
E_MINOR = ["e3", "g3", "b3", "e4"]
F_MAJOR = ["f2", "a2", "c3", "f3"]

ALL_CHORDS = [
  #C_MAJOR, G_MAJOR, A_MINOR, E_MINOR, F_MAJOR,
  C_MAJOR, G_MAJOR, F_MAJOR,
]

chords = converter.parse("""tinynotation: 4/4""")
"""
chords.append(Rest(duration=WHOLE_NOTE))
chords.append(Chord(C_MAJOR, duration=WHOLE_NOTE))
chords.append(Chord(G_MAJOR, duration=WHOLE_NOTE))
chords.append(Chord(A_MINOR, duration=WHOLE_NOTE))
chords.append(Chord(G_MAJOR, duration=WHOLE_NOTE))
chords.append(Chord(F_MAJOR, duration=WHOLE_NOTE))
chords.append(Chord(E_MINOR, duration=WHOLE_NOTE))
chords.append(Chord(F_MAJOR, duration=WHOLE_NOTE))
chords.append(Chord(G_MAJOR, duration=WHOLE_NOTE))
"""

melody = converter.parse(JJ_LIN_MELODY)
melody.insert(0, MetronomeMark(number=95))

# Insert a chord for each measure
for measure in filter(lambda x: isinstance(x, music21.stream.Measure), melody.elements):
  measure_notes = []
  for note in filter(lambda x: isinstance(x, music21.note.Note), measure.elements):
    measure_notes.append(note)
  chords.append(Chord(chord_search(measure_notes), duration=WHOLE_NOTE))


# Combine two parts
song = Stream()
song.insert(0, melody)
song.insert(0, chords)

song.show('midi')
#song.show()
