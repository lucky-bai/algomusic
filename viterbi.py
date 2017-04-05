from __future__ import division

import operator

import music21
from music21 import converter
from music21.tempo import MetronomeMark
from music21.chord import Chord
from music21.note import Note
from music21.duration import Duration
from music21.stream import Stream
from music21.interval import notesToChromatic

from chord_search import ALL_CHORDS, ALL_CHORDS_MIN


def viterbi(states, obs, init_probs, trans_probs, emit_fn):
    """
    :param states: the state space
    :param obs: a list of observations
    :param init_probs: a list of initial probabilities
    :param trans_probs: transition probability matrix
    :param emit_fn: emission probability function
    """
    # V[i][j] stores probability of most likely path for the first j observations that have i as the final state
    V = [[0 for _ in range(len(obs))] for _ in range(len(states))]
    back_ptrs = [[0 for _ in range(len(obs))] for _ in range(len(states))]

    # Initialization
    for i in range(len(states)):
        V[i][0] = init_probs[i] * emit_fn(states[i], obs[0])
        back_ptrs[i][0] = 0

    for i in range(1, len(obs)):
        for j in range(len(states)):
            V[j][i] = emit_fn(states[j], obs[i]) * max(V[k][i-1] * trans_probs[k][j] for k in range(len(states)))
            # argmax
            back_ptrs[j][i], _ = max(enumerate([V[k][i-1] * trans_probs[k][j] for k in range(len(states))]), key=operator.itemgetter(1))

    z, max_prob = max(enumerate([V[k][-1] for k in range(len(states))]), key=operator.itemgetter(1))
    path = [None for _ in range(len(obs))]
    path[-1] = states[z]

    for i in range(len(obs)-1, 0, -1):
        z = back_ptrs[z][i]
        path[i-1] = states[z]

    return max_prob, path


CHROMATIC_PENALTY = {
  0: 0,
  1: 2,
  2: 1,
  3: 0,
  4: 0,
  5: 0,
  6: 2,
}

def goodness(chord, bar_notes):
    score = 0
    for note1 in chord.notes[:-1]:
        note1 = Note(note1)
        for note2 in bar_notes:
            chromatic_distance = notesToChromatic(note1, note2).semitones

            # Normalize distance to be between 0 and 6
            chromatic_distance = chromatic_distance % 12
            if chromatic_distance > 6:
              chromatic_distance = 12 - chromatic_distance

            score += CHROMATIC_PENALTY[chromatic_distance]

    print('Chord', chord.name)
    print(bar_notes)
    print('uninverted score', score)
    return 1 / max(1, score)


if __name__ == '__main__':
    # If Only by JJ Lin
    JJ_LIN_MELODY = """
    tinynotation: 4/4
    r2 r8 G8 e8 d8     e2 e8 d8 e8 c8     B8 g8 g4 e8 d8 e8 c8
    A4 a4 g8 f8 e8 f8     e2 e8 d8 e8 c8    A4 a4 g8 f8 e8 f8
    g2~ g8 c16 d16 e8 d8    e8 c16 d16 e8 d8 e8 c16 d16 e8 d8
    f1
    """


    XIAO_XIN_YUN_MELODY = """
    tinynotation: 4/4
    r2 b8 a8 g8 f#8    e8 e8 e8 e8 e8 b4 b8    a2 a8 g8 f#8 e8
    d8 d8 d8 d8 d8 a4 a8    g1
    """

    WHOLE_NOTE = Duration(4.0)

    melody = converter.parse(XIAO_XIN_YUN_MELODY)
    melody.insert(0, MetronomeMark(number=95))

    all_notes = []
    # Insert a chord for each measure
    for measure in filter(lambda x: isinstance(x, music21.stream.Measure), melody.elements):
        measure_notes = []
        for note in filter(lambda x: isinstance(x, music21.note.Note), measure.elements):
            measure_notes.append(note)
        all_notes.append(measure_notes)

    init_probs = [0, 1, 0, 0, 0, 0]
    init_probs_min = [0, 0, 0, 0, 0, 1, 0]
    trans_probs = []
    for i in range(len(ALL_CHORDS_MIN)):
        trans_prob = []
        for j in range(len(ALL_CHORDS_MIN)):
            if i != j:
                trans_prob.append(3)
            else:
                trans_prob.append(1)

        s = sum(trans_prob)
        trans_probs.append(map(lambda x: x / s, trans_prob))

    prob, chord_seq = viterbi(ALL_CHORDS_MIN, all_notes, init_probs_min, trans_probs, goodness)

    chords = converter.parse("""tinynotation: 4/4""")
    for chord in chord_seq:
        chords.append(Chord(chord.notes, duration=WHOLE_NOTE))
        print(chord.name)

    # Combine two parts
    song = Stream()
    song.insert(0, melody)
    song.insert(0, chords)

    song.show('midi')

    # print('Run wikipedia example as test')
    # observations_space = ['normal', 'cold', 'dizzy']
    # observations = ['normal', 'cold', 'dizzy']
    # states = ['Healthy', 'Fever']
    # init_probs = [0.6, 0.4]
    # trans_probs = [[0.7, 0.3], [0.4, 0.6]]
    # def emit_fn(state, obs):
    #     vals = {'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
    #             'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
    #     return vals[state][obs]
    #
    # seq_prob, seq = viterbi(states, observations, init_probs, trans_probs, emit_fn)
    # print('Most like sequence is', seq)
    # print('This sequence has probability', seq_prob)
