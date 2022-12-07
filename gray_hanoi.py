import copy
import math

from gray_tower import GrayTower


class GrayHanoi(GrayTower):

    def __init__(self, n_rigs, n_disks):
        super().__init__(n_rigs, n_disks)
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

    def solve(self, verbose=False):
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
        if verbose:
            self.pretty_print(configurations)
        return configurations
