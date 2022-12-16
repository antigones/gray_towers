import random as rd

configurations = [
    [[2, 1], [], []],
    [[2], [1], []],
    [[2], [], [1]],
    [[], [1], [2]],
    [[], [2], [1]],
    [[], [], [2, 1]],
    [[1], [], [2]],
    [[1], [2], []],
    [[], [2, 1], []],
]


r = [
    [-1, 0, 0, -1, -1, -1, -1, -1, -1],  # 0
    [0, -1, 0, 0, -1, -1, -1, -1, -1],  # 1
    [0, 0, -1, -1, 0, -1, -1, -1, -1],  # 2
    [-1, 0, -1, -1, -1, 100, 0, -1, -1],  # 3
    [-1, -1, 0, -1, -1, -1, -1, 0, 0],  # 4
    [-1, -1, -1, 0, -1, -1, 0, -1, -1],  # 5
    [-1, -1, -1, 0, -1, 100, -1, 0, -1],  # 6
    [-1, -1, -1, -1, 0, -1, 0, -1, 0],  # 7
    [-1, -1, -1, -1, 0, -1, -1, 0, 0],  # 8
]

q = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

"""
states = {
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 4],
    3: [1, 5, 6],
    4: [2, 7, 8],
    5: [3, 6],
    6: [3, 5],
    7: [4, 8],
    8: [4, 7],
}
"""

possible_initial_states = [0, 1, 2, 3, 4, 5, 6, 7, 8]
explored_initial_states = set()
episode = 1
GAMMA = 0.8
GOAL_STATE = 5
while len(possible_initial_states) - len(explored_initial_states) > 0:
    initial_state_for_this_episode = rd.choice(possible_initial_states)
    explored_initial_states.add(initial_state_for_this_episode)
    print('*** EPISODE '+str(episode)+' ***')
    while initial_state_for_this_episode != GOAL_STATE:
        # choose a possible initial state for this episode
        initial_state_for_this_episode = rd.choice(possible_initial_states)

        print('** INITIAL STATE FOR EPISODE '+str(episode))
        print(initial_state_for_this_episode)
        print('*** CHOICES FOR THIS STATE***')
        possible_choices_for_this_state = r[initial_state_for_this_episode]
        print(possible_choices_for_this_state)
        candidate_next_states = []
        for i in range(len(possible_choices_for_this_state)):
            if possible_choices_for_this_state[i] != -1:
                candidate_next_states.append(i)

        # candidate_next_states = []
        # for i in range(len(candidate_next_indices)):
        #    candidate_next_states.append(
        #        possible_choices_for_this_state[candidate_next_indices[i]])
        # print(candidate_next_states)
        print('*** CANDIDATE NEXT STATES ***')
        print(candidate_next_states)
        next_state = rd.choice(candidate_next_states)
        print('*** NEXT STATE ***')
        print(next_state)
        print(r[initial_state_for_this_episode][next_state])
        print(q[next_state])
        q[initial_state_for_this_episode][next_state] = r[initial_state_for_this_episode][next_state] + \
            GAMMA * max(q[next_state])
        print('*** UPDATED Q ***')
        print(q)
        initial_state_for_this_episode = next_state
    # possible_initial_states.remove(initial_state_for_this_episode)
    episode += 1

next_state = 0
print(configurations[next_state])
c = 0
while next_state != GOAL_STATE and c < 10:
    edges = q[next_state]
    (m, i) = max((v, i) for i, v in enumerate(edges))
    # print(i)
    print(configurations[i])
    next_state = i
    c += 1
