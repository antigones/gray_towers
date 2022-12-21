import copy
import random as rd
import math
import numpy as np
from collections import defaultdict


class HanoiTowerQLearning:

    def __init__(self, start_state, goal_state, n_rigs, n_disks, gamma=0.8, alpha=0.1, epsilon=0.5, max_episodes=50000):
        self.start_state = start_state
        self.goal_state = goal_state
        self.gamma = gamma
        self.alpha = alpha
        self.n_rigs = n_rigs
        self.n_disks = n_disks
        self.max_episodes = max_episodes

        self.min_epsilon = 0.01
        self.max_epsilon = 1.0
        self.decay_rate = 0.01
        self.epsilon = self.min_epsilon + \
            (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * 1)

        self.total_nr_of_state = self.n_rigs ** self.n_disks

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

    def get_reward(self, state, visited):
        print('** VISITED **')
        print(state)
        print(visited)
        if state == self.goal_state:
            return 100
        if str(state) in visited:
            print('VIS')
            return -500

        return -1

    def find_in_qsa(self, q_s_a, key):
        res = []
        for k in q_s_a.keys():
            if k.startswith(key+"|"):
                res.append(k)
        return res

    def find_val_in_qsa(self, q_s_a, key):
        res = []
        for k in q_s_a.keys():
            if k.startswith(key+"|"):
                res.append(q_s_a[k])
        return res

    def train(self, verbose=False):

        possible_initial_states = set()
        possible_initial_states.add(str(self.start_state))

        GAMMA = self.gamma
        GOAL_STATE = self.goal_state
        ALPHA = self.alpha
        MAX_EPISODES = self.max_episodes
        #q = [[0]*self.total_nr_of_state for _ in range(self.total_nr_of_state)]
        #q_prec = copy.deepcopy(q)

        done = False
        convergence_count = 0
        q_s_a = defaultdict(lambda: 0)
        q_s_a_prec = q_s_a
        episode = 1

        while episode < MAX_EPISODES and not done:
            visited = []
            initial_state_for_this_episode = rd.choice(
                list(possible_initial_states))

            print('*** EPISODE '+str(episode)+' ***')
            print('*** POSSIBLE INITIAL STATES FOR THIS EPISODE ***')
            print(len(possible_initial_states))
            while eval(initial_state_for_this_episode) != GOAL_STATE:
                # print(initial_state_for_this_episode)
                possible_next_states_for_this_state = self.get_next_allowed_moves(
                    eval(initial_state_for_this_episode))
                # print(possible_next_states_for_this_state)
                rewards_for_actions = {}
                q_s1_a = []
                for next_state in possible_next_states_for_this_state:
                    rewards_for_actions[str(next_state)
                                        ] = self.get_reward(next_state, visited)
                    q_s1_a.append(
                        q_s_a[initial_state_for_this_episode+"|"+str(next_state)])
                    possible_initial_states.add(str(next_state))

                #print('** R FOR ACTIONS **')
                # print(rewards_for_actions)
                #print('** QS1A **')
                # print(q_s1_a)
                # q_s_list = self.find_in_qsa(
                #    q_s_a, initial_state_for_this_episode)
                q_s_list = {x: q_s_a[x] for x in q_s_a.keys() if x.startswith(
                    initial_state_for_this_episode+"|")}
                #print('** QSLIST **')
                # print(q_s_list)
                e = rd.uniform(0, 1)
                if e < self.epsilon:
                    chosen_next_state = str(rd.choice(
                        possible_next_states_for_this_state))
                else:
                    m = max(
                        q_s_list, key=q_s_list.get)
                    chosen_next_state = m.split("|")[1]
                visited.append(chosen_next_state)
                q_s_a[initial_state_for_this_episode+"|"+chosen_next_state] += ALPHA * (
                    rewards_for_actions[chosen_next_state] + GAMMA * max(q_s1_a) - q_s_a[initial_state_for_this_episode+"|"+chosen_next_state])

                # print('**QSA**')
                # print(q_s_a)
                initial_state_for_this_episode = chosen_next_state

            if q_s_a == q_s_a_prec:
                if convergence_count > int(10):
                    print('** CONVERGED **')

                    done = True
                    break
                else:
                    convergence_count += 1
            else:
                q_s_a_prec = q_s_a
                convergence_count = 0

            # epsilon update

            self.epsilon = self.min_epsilon + \
                (self.max_epsilon - self.min_epsilon) * \
                np.exp(-self.decay_rate * episode)
            episode += 1

        print(q_s_a)

        c = 0
        next_state = str(self.start_state)
        while next_state != str(self.goal_state) and c <= 10:
            candidate_next_list = {x: q_s_a[x] for x in q_s_a.keys() if x.startswith(
                next_state+"|")}
            m = max(
                candidate_next_list, key=candidate_next_list.get)
            next_state = m.split("|")[1]
            print(next_state)
            c += 1
