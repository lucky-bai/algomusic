from viterbi import viterbi


if __name__ == '__main__':
    print('Run wikipedia example as test')
    observations_space = ['normal', 'cold', 'dizzy']
    observations = ['normal', 'cold', 'dizzy']
    states = ['Healthy', 'Fever']
    init_probs = [0.6, 0.4]
    trans_probs = [[0.7, 0.3], [0.4, 0.6]]
    def emit_fn(state, obs):
        vals = {'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
                'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
        return vals[state][obs]

    seq_prob, seq = viterbi(states, observations, init_probs, trans_probs, emit_fn)
    print('Most like sequence is', seq)
    print('This sequence has probability', seq_prob)
