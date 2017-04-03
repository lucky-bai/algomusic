from collections import namedtuple

from music21.note import Note
from music21.interval import notesToChromatic

# Cannot use name 'Chord', already taken
HarmonyChord = namedtuple('HarmonyChord', ['name', 'notes'])


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

# Todo: add more chords
C_MAJ = HarmonyChord(name='C', notes=['c3', 'e3', 'g3', 'c4'])
G_MAJ = HarmonyChord(name='G', notes=["g2", "b2", "d3", "g3"])
A_MIN = HarmonyChord(name='Am', notes=["a2", "c3", "e3", "a3"])
E_MIN = HarmonyChord(name='Em', notes=["e3", "g3", "b3", "e4"])
F_MAJ = HarmonyChord(name='F', notes=["f2", "a2", "c3", "f3"])

ALL_CHORDS = [
  C_MAJ, G_MAJ, A_MIN, E_MIN, F_MAJ,
]


def chord_search(notes):
  """Attempt to find the best chord to match a set of notes"""
  best_chord, best_score = C_MAJ, -1000

  for chord in ALL_CHORDS:
    chord_score = 0
    for note1 in chord.notes:
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

  print best_chord.name
  return best_chord
