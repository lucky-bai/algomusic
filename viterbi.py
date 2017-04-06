from __future__ import division

import operator

import music21
from music21.chord import Chord
from music21.note import Note
from music21.interval import notesToChromatic

from chord_search import ALL_CHORDS, ALL_CHORDS_MIN, CHROMATIC_PENALTY, WHOLE_NOTE


# Initialization probabilities for major and minor chords
INIT_PROBS = [0, 1, 0, 0, 0, 0]
INIT_PROBS_MIN = [0, 0, 0, 0, 0, 1, 0]

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

    return 1 / max(1, score)


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


def run(chords, melody, series):
    all_notes = []
    # Construct music21 notes, grouped into measures
    for measure in filter(lambda x: isinstance(x, music21.stream.Measure), melody.elements):
        measure_notes = []
        for note in filter(lambda x: isinstance(x, music21.note.Note), measure.elements):
            measure_notes.append(note)
        all_notes.append(measure_notes)

    init_probs = INIT_PROBS if series == 'major' else INIT_PROBS_MIN

    # Build transition matrix where probability of self-transition is low
    all_chords = ALL_CHORDS if series == 'major' else ALL_CHORDS_MIN
    trans_probs = []
    for i in range(len(all_chords)):
        trans_prob = []
        for j in range(len(all_chords)):
            if i != j:
                trans_prob.append(3)
            else:
                trans_prob.append(1)

        s = sum(trans_prob)
        trans_probs.append(map(lambda x: x / s, trans_prob))

    prob, chord_seq = viterbi(all_chords, all_notes, init_probs, trans_probs, goodness)

    for chord in chord_seq:
        chords.append(Chord(chord.notes, duration=WHOLE_NOTE))
        print(chord.name)
