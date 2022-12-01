import copy


class GrayBucharest:

    def __init__(self, n_rigs, n_disks):
        self.n_rigs = n_rigs
        self.n_disks = n_disks
        self.rigs = self.populate_rigs()
        self.ternary_gray_sequence = [[0, 0, 0], [0, 0, 1], [0, 0, 2],
                                      [0, 1, 2], [0, 1, 1], [0, 1, 0],
                                      [0, 2, 0], [0, 2, 1], [0, 2, 2],
                                      [1, 2, 2], [1, 2, 1], [1, 2, 0],
                                      [1, 1, 0], [1, 1, 1], [1, 1, 2],
                                      [1, 0, 2], [1, 0, 1], [1, 0, 0],
                                      [2, 0, 0], [2, 0, 1], [2, 0, 2],
                                      [2, 1, 2], [2, 1, 1], [2, 1, 0],
                                      [2, 2, 0], [2, 2, 1], [2, 2, 2]]

    def move_disk(self, disk_to_move, current_rig_idx, next_rig_idx):
        """Move the disk from the current ring to the next one."""
        if current_rig_idx != next_rig_idx:
            self.rigs[current_rig_idx] = self.rigs[current_rig_idx][:-1]
            self.rigs[next_rig_idx].append(disk_to_move)

    def check_objective(self):
        """Check if game ended."""
        return self.rigs == [[], [], list(range(self.n_disks-1, -1, -1))]

    def populate_rigs(self):
        """Populate rigs with disks."""
        rigs = [[] for x in range(self.n_rigs)]
        rigs[0] = list(range(self.n_disks-1, -1, -1))
        return rigs

    def solve(self):
        """Find the moves to solve the puzzle."""

        configurations = [copy.deepcopy(self.rigs)]
        last_rigs = [0, 0, 0]
        i = 1
        while not self.check_objective():
            # g = self.dec2gray(i)
            ternary_gray_code = self.ternary_gray_sequence[i]
            small_disk_next_rig = ternary_gray_code[2]
            medium_disk_next_rig = ternary_gray_code[1]
            bigger_disk_next_rig = ternary_gray_code[0]

            self.move_disk(0, last_rigs[2], small_disk_next_rig)
            self.move_disk(1, last_rigs[1], medium_disk_next_rig)
            self.move_disk(2, last_rigs[0], bigger_disk_next_rig)

            last_rigs[0] = bigger_disk_next_rig
            last_rigs[1] = medium_disk_next_rig
            last_rigs[2] = small_disk_next_rig
            configurations.append(copy.deepcopy(self.rigs))
            i += 1
        return configurations
