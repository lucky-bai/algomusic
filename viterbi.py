import operator


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
