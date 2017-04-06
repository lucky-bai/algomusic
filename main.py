import argparse
import sys

import music21
from music21 import converter
from music21.tempo import MetronomeMark
from music21.stream import Stream

import chord_search
import viterbi

# If Only by JJ Lin
JJ_LIN_MELODY = """
tinynotation: 4/4
r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
f1
"""

# A Little Happiness by Hebe Tien
A_LITTLE_HAPPINESS = """
tinynotation: 4/4
r2 b8 a8 g8 f#8    e8 e8 e8 e8 e8 b4 b8    a2 a8 g8 f#8 e8
d8 d8 d8 d8 d8 a4 a8    g1
"""

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

# Parse command line arguments
parser = argparse.ArgumentParser(description='Find sequence of harmonizing chord progression.')
parser.add_argument('--algorithm', type=str, default='hmm', help='algorithm to use: basic or hmm')
parser.add_argument('--melody', type=str, default='jj_lin', help='jj_lin or little_happiness')
parser.add_argument('--series', type=str, default='major', help='major or minor')
args = parser.parse_args()

print('Algorithm: {}, Melody: {}, Series: {}'.format(args.algorithm, args.melody, args.series))

# Pick melody
if args.melody == 'little_happiness':
    melody = converter.parse(A_LITTLE_HAPPINESS)
elif args.melody == 'jj_lin':
    melody = converter.parse(JJ_LIN_MELODY)
else:
    print('Unrecognized melody: should be jj_lin or little_happiness')
    sys.exit(1)

if args.series not in ('major', 'minor'):
    print('Unrecognized series: should be major or minor')
    sys.exit(1)

melody.insert(0, MetronomeMark(number=95))

# Pick algorithm
if args.algorithm == 'basic':
    chord_search.run(chords, melody, args.series)
elif args.algorithm == 'hmm':
    viterbi.run(chords, melody, args.series)
else:
    print('Unrecognized algorithm: should be basic or hmm')
    sys.exit(1)

# Combine two parts
song = Stream()
song.insert(0, melody)
song.insert(0, chords)

# song.show('midi')
song.show()
