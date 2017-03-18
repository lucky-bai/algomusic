from music21 import converter
from music21.tempo import MetronomeMark

# If Only by JJ Lin
JJ_LIN_MELODY = """
tinynotation: 4/4
r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
f1
"""

melody = converter.parse(JJ_LIN_MELODY)
melody.insert(0, MetronomeMark(number=95))

melody.show('midi')
#melody.show()
