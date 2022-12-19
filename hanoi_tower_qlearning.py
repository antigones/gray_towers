import copy
import random as rd
import math
import numpy as np


class HanoiTowerQLearning:

    def __init__(self, start_state, goal_state, n_rigs, n_disks, gamma=0.8, alpha=0.1, epsilon=0.5, max_episodes=50000):
        self.start_state = start_state
        self.goal_state = goal_state
        self.gamma = gamma
        self.alpha = alpha
        self.n_rigs = n_rigs
        self.n_disks = n_disks
        self.max_episodes = max_episodes
        self.epsilon = epsilon

    def get_next_allowed_moves(self, starting_state):
        next_moves = []
        for i, source_rig in enumerate(starting_state):

            if len(source_rig) > 0:
                for j, dest_rig in enumerate(starting_state):
                    copied_rigs = copy.deepcopy(starting_state)
                    if i != j:
                        # no point in moving on same rig
                        if len(dest_rig) > 0:
                            if dest_rig[-1] > source_rig[-1]:
                                copied_rigs[i] = copied_rigs[i][:-1]
                                copied_rigs[j].append(source_rig[-1])
                                next_moves.append(copied_rigs)
                        else:
                            copied_rigs[i] = copied_rigs[i][:-1]
                            copied_rigs[j].append(source_rig[-1])
                            next_moves.append(copied_rigs)
        return next_moves

    def generate_space_states(self, from_state):
        q = []
        q.append(from_state)
        space = []
        visited = []
        while len(q) > 0:
            state_to_explore = q.pop(0)
            if not state_to_explore in visited:
                next_states = self.get_next_allowed_moves(state_to_explore)
                visited.append(state_to_explore)
                q += next_states
                for state in next_states:
                    if not state in space:
                        space.append(state)
        return space

    def generate_qr(self, from_state):
        q = []
        q.append(from_state)
        total_nr_of_state = self.n_rigs ** self.n_disks
        r_matrix = [[-math.inf]*total_nr_of_state]*total_nr_of_state
        r_matrix = [[-math.inf] *
                    total_nr_of_state for _ in range(total_nr_of_state)]
        q_matrix = [[0]*total_nr_of_state for _ in range(total_nr_of_state)]
        space_dict = {0: from_state}
        index_dict = {str(from_state): 0}
        visited = []
        c = 1
        while len(q) > 0:
            state_to_explore = q.pop(0)
            if not state_to_explore in visited:
                visited.append(state_to_explore)
                next_states = self.get_next_allowed_moves(state_to_explore)
                q += next_states
                for next_state in next_states:
                    if str(next_state) not in index_dict.keys():
                        space_dict[c] = next_state
                        index_dict[str(next_state)] = c
                        # fill reward matrix (R)
                        c += 1

        for start_state in index_dict.keys():
            next_states = self.get_next_allowed_moves(eval(start_state))
            start_state_index = index_dict[str(start_state)]
            for next_state in next_states:
                next_state_index = index_dict[str(next_state)]
                if next_state == self.goal_state:
                    r_matrix[start_state_index][next_state_index] = 100
                else:
                    r_matrix[start_state_index][next_state_index] = 0.1

        # loopback for goal state
        goal_state_index = index_dict[str(self.goal_state)]
        r_matrix[goal_state_index][goal_state_index] = 100
        return space_dict, index_dict, r_matrix, q_matrix

    def train(self, verbose=False):

        space_dict, index_dict, r, q = self.generate_qr(
            self.start_state)
        possible_initial_states = list(range(len(space_dict)))
        episode = 1
        GAMMA = self.gamma
        GOAL_STATE = index_dict[str(self.goal_state)]
        ALPHA = self.alpha
        MAX_EPISODES = self.max_episodes
        q_prec = copy.deepcopy(q)

        done = False
        convergence_count = 0

        min_epsilon = 0.01
        max_epsilon = 1.0
        decay_rate = 0.01
        self.epsilon = min_epsilon + \
            (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

        while episode < MAX_EPISODES and not done:
            initial_state_for_this_episode = rd.choice(
                possible_initial_states)
            print('*** EPISODE '+str(episode)+' ***')
            while initial_state_for_this_episode != GOAL_STATE:
                possible_choices_for_this_state = r[initial_state_for_this_episode]
                candidate_next_states = []
                for i in range(len(possible_choices_for_this_state)):
                    if possible_choices_for_this_state[i] != -math.inf:
                        candidate_next_states.append(i)

                # print(initial_state_for_this_episode)
                # print(candidate_next_states)

                r = rd.uniform(0, 1)
                if r < self.epsilon:
                    next_state = rd.choice(candidate_next_states)
                else:
                    next_state = np.argmax(r[initial_state_for_this_episode])

                # naive way to update
                # q[initial_state_for_this_episode][next_state] = r[initial_state_for_this_episode][next_state] + \
                #    GAMMA * max(q[next_state])

                ## another way to update ##
                q_target = r[initial_state_for_this_episode][next_state] + \
                    GAMMA * max(q[next_state])
                q_delta = q_target - \
                    q[initial_state_for_this_episode][next_state]
                q[initial_state_for_this_episode][next_state] = q[initial_state_for_this_episode][next_state] + \
                    ALPHA*(q_delta)
                ## end of another way to update ##
                initial_state_for_this_episode = next_state

            if np.allclose(q, q_prec) and sum(sum(x) for x in q) > 0:
                if convergence_count > int(10):
                    print('CONVERGE!')

                    done = True
                    break
                else:
                    convergence_count += 1
            else:
                q_prec = copy.deepcopy(q)
                convergence_count = 0

            # epsilon update

            self.epsilon = min_epsilon + \
                (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
            episode += 1

        next_state = 0
        print(space_dict[next_state])
        c = 0
        while next_state != GOAL_STATE:
            edges = q[next_state]
            (m, i) = max((v, i) for i, v in enumerate(edges))
            print(space_dict[i])
            next_state = i
            c += 1
