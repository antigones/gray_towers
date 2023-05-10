import copy
import math

from gray_tower import GrayTower


class GrayHanoi(GrayTower):

    def __init__(self, n_disks):
        super().__init__(3, n_disks)
        self.small_disk_peg_seq = self.calc_small_disc_peg_seq()

    def calc_small_disc_peg_seq(self):
        """Calculate how small disk should move along the pegs."""
        # those starts from index 2
        if self.n_disks % 2 == 1:
            return [2, 1, 0] # (first, target, remaining) -> target, remaining, first
        return [1, 2, 0]  #  (first, remaining, target) -> remaining, target, first

    def dec2brgray(self, n):
        return n ^ (n >> 1)

    def solve(self, verbose=False):
        """Find the moves to solve the puzzle."""
        configurations = [copy.deepcopy(self.pegs)]
        small_disk_move = 0
        i = 1
        while not self.check_objective():
            g = self.dec2brgray(i)
            g_last = self.dec2brgray(i-1)
            which_position_changed = g ^ g_last
            disk_to_move = int(math.log(which_position_changed, 2))

            if disk_to_move == 0:
                next_peg_idx = self.small_disk_peg_seq[small_disk_move % 3]
                small_disk_move += 1
            else:
                next_peg_idx = self.find_allowed(disk_to_move)
            current_peg_idx = self.find_peg(disk_to_move)
            self.move_disk(disk_to_move, current_peg_idx, next_peg_idx)

            configurations.append(copy.deepcopy(self.pegs))
            i += 1
        if verbose:
            self.pretty_print(configurations)
        return configurations
