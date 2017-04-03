import music21
from music21 import converter
from music21.tempo import MetronomeMark
from music21.chord import Chord
from music21.note import Rest
from music21.note import Note
from music21.duration import Duration
from music21.stream import Stream
from music21.interval import notesToChromatic

from chord_search import *

# If Only by JJ Lin
JJ_LIN_MELODY = """
tinynotation: 4/4
r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
f1
"""

WHOLE_NOTE = Duration(4.0)

chords = converter.parse("""tinynotation: 4/4""")
"""
chords.append(Rest(duration=WHOLE_NOTE))
chds.append(Chd(C_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(A_MIN, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(F_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(E_MIN, duration=WHOLE_NOTE))
chds.append(Chd(F_MAJ, duration=WHOLE_NOTE))
chds.append(Chd(G_MAJ, duration=WHOLE_NOTE))
"""

melody = converter.parse(JJ_LIN_MELODY)
melody.insert(0, MetronomeMark(number=95))

# Insert a chord for each measure
for measure in filter(lambda x: isinstance(x, music21.stream.Measure), melody.elements):
  measure_notes = []
  for note in filter(lambda x: isinstance(x, music21.note.Note), measure.elements):
    measure_notes.append(note)
  chords.append(Chord(chord_search(measure_notes).notes, duration=WHOLE_NOTE))


# Combine two parts
song = Stream()
song.insert(0, melody)
song.insert(0, chords)

#song.show('midi')
#song.show()
