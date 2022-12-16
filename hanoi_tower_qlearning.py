import copy
import random as rd


class HanoiTowerQLearning:

    def __init__(self, start_state, goal_state, n_rigs, n_disks, gamma=0.8):
        self.start_state = start_state
        self.goal_state = goal_state
        self.gamma = gamma
        self.n_rigs = n_rigs
        self.n_disks = n_disks

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
        r_matrix = [[-1]*total_nr_of_state]*total_nr_of_state
        r_matrix = [[-1] * total_nr_of_state for _ in range(total_nr_of_state)]
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
                        # compile environment matrix (R)
                        c += 1

        for start_state in index_dict.keys():
            next_states = self.get_next_allowed_moves(eval(start_state))
            start_state_index = index_dict[str(start_state)]
            for next_state in next_states:
                next_state_index = index_dict[str(next_state)]
                if next_state == self.goal_state:
                    r_matrix[start_state_index][next_state_index] = 100
                else:
                    r_matrix[start_state_index][next_state_index] = 0
        return space_dict, index_dict, r_matrix, q_matrix

    def train(self):

        space_dict, index_dict, r, q = self.generate_qr(
            self.start_state)

        possible_initial_states = list(range(len(space_dict)))
        explored_initial_states = set()
        episode = 1
        GAMMA = self.gamma
        GOAL_STATE = index_dict[str(self.goal_state)]

        while len(possible_initial_states) - len(explored_initial_states) > 0:
            initial_state_for_this_episode = rd.choice(possible_initial_states)
            explored_initial_states.add(initial_state_for_this_episode)
            print('*** EPISODE '+str(episode)+' ***')
            while initial_state_for_this_episode != GOAL_STATE:
                # choose a possible initial state for this episode
                initial_state_for_this_episode = rd.choice(
                    possible_initial_states)

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

        print(space_dict[next_state])
        c = 0
        while next_state != GOAL_STATE and c < 10:
            edges = q[next_state]
            (m, i) = max((v, i) for i, v in enumerate(edges))
            # print(i)
            print(space_dict[i])
            next_state = i
            c += 1
