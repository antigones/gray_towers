import copy
import math


class GrayHanoi:

    def __init__(self, n_rigs, n_disks):
        self.n_rigs = n_rigs
        self.n_disks = n_disks
        self.rigs = self.populate_rigs()
        self.small_disk_rig_seq = self.calc_small_disc_rig_seq()

    def calc_small_disc_rig_seq(self):
        """Calculate how small disk should move along the rigs."""
        # those starts from index 2
        if self.n_disks % 2 == 1:

            # 0=first, 1=target , 2=remaining
            return [2, 1, 0]
        return [1, 2, 0]  # first, remaining, target

    def dec2gray(self, n):
        return n ^ (n >> 1)

    def find_allowed(self, disk):
        """
        Return index of the rig to move the disk to, with respect to allowed moves
        move is allowed if the rig is empty or the disk on the rig is bigger than the
        one we are placing on the top of it.
        """
        for idx, rig in enumerate(self.rigs):
            if len(rig) == 0 or rig[-1] > disk:
                return idx

    def find_rig(self, disk):
        """Find the rigs where the disk lies on."""
        for idx, rig in enumerate(self.rigs):
            if len(rig) > 0:
                if rig[-1] == disk:
                    return idx

    def move_disk(self, disk_to_move, current_rig_idx, next_rig_idx):
        """Move the disk from the current ring to the next one."""
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
        small_disk_move = 0
        last = 0
        i = 1
        while not self.check_objective():
            g = self.dec2gray(i)
            g_last = self.dec2gray(last)
            which_position_changed = g ^ g_last
            disk_to_move = int(math.log(which_position_changed, 2))

            if disk_to_move == 0:
                next_rig_idx = self.small_disk_rig_seq[small_disk_move % 3]
                small_disk_move += 1
            else:
                next_rig_idx = self.find_allowed(disk_to_move)

            current_rig_idx = self.find_rig(disk_to_move)
            self.move_disk(disk_to_move, current_rig_idx, next_rig_idx)
            configurations.append(copy.deepcopy(self.rigs))
            last = i
            i += 1
        return configurations
