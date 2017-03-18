from music21 import converter
from music21.tempo import MetronomeMark
from music21.chord import Chord
from music21.note import Rest
from music21.duration import Duration
from music21.stream import Stream


# If Only by JJ Lin
JJ_LIN_MELODY = """
tinynotation: 4/4
r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
f1
"""

WHOLE_NOTE = Duration(4.0)

C_MAJOR = Chord(["c3", "e3", "g3", "c4"], duration=WHOLE_NOTE)
G_MAJOR = Chord(["g2", "b2", "d3", "g3"], duration=WHOLE_NOTE)
A_MINOR = Chord(["a2", "c3", "e3", "a3"], duration=WHOLE_NOTE)
E_MINOR = Chord(["e3", "g3", "b3", "e4"], duration=WHOLE_NOTE)
F_MAJOR = Chord(["f2", "a2", "c3", "f3"], duration=WHOLE_NOTE)

chords = converter.parse("""tinynotation: 4/4""")
chords.append(Rest(duration=WHOLE_NOTE))
chords.append(Chord(C_MAJOR))
chords.append(Chord(G_MAJOR))
chords.append(Chord(A_MINOR))
chords.append(Chord(G_MAJOR))
chords.append(Chord(F_MAJOR))
chords.append(Chord(E_MINOR))
chords.append(Chord(F_MAJOR))
chords.append(Chord(G_MAJOR))

melody = converter.parse(JJ_LIN_MELODY)
melody.insert(0, MetronomeMark(number=95))

song = Stream()
song.insert(0, melody)
song.insert(0, chords)

song.show('midi')
#song.show()
