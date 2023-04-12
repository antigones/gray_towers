import copy

from gray_tower import GrayTower


class GrayBucharest(GrayTower):

    def __init__(self, n_pegs, n_disks):
        super().__init__(n_pegs, n_disks)
        
        self.ternary_gray_sequence = [
            [0, 0, 0], [0, 0, 1], [0, 0, 2],
            [0, 1, 2], [0, 1, 1], [0, 1, 0],
            [0, 2, 0], [0, 2, 1], [0, 2, 2],
            [1, 2, 2], [1, 2, 1], [1, 2, 0],
            [1, 1, 0], [1, 1, 1], [1, 1, 2],
            [1, 0, 2], [1, 0, 1], [1, 0, 0],
            [2, 0, 0], [2, 0, 1], [2, 0, 2],
            [2, 1, 2], [2, 1, 1], [2, 1, 0],
            [2, 2, 0], [2, 2, 1], [2, 2, 2]
        ]
        
        # self.ternary_gray_sequence = self.generate_m_ary_gray_code(3)

    def solve(self, verbose=False):
        """Find the moves to solve the puzzle."""

        configurations = [copy.deepcopy(self.pegs)]
        last_pegs = self.ternary_gray_sequence[0]
        # i = 1
        # while not self.check_objective():
        for i in range(len(self.ternary_gray_sequence)):
            ternary_gray_code = self.ternary_gray_sequence[i]
            small_disk_next_peg = ternary_gray_code[2]
            medium_disk_next_peg = ternary_gray_code[1]
            bigger_disk_next_peg = ternary_gray_code[0]

            self.move_disk(0, last_pegs[2], small_disk_next_peg)
            self.move_disk(1, last_pegs[1], medium_disk_next_peg)
            self.move_disk(2, last_pegs[0], bigger_disk_next_peg)

            last_pegs[0] = bigger_disk_next_peg
            last_pegs[1] = medium_disk_next_peg
            last_pegs[2] = small_disk_next_peg
            configurations.append(copy.deepcopy(self.pegs))
            i += 1
        if verbose:
            self.pretty_print(configurations)
        return configurations
