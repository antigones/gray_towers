import copy

from gray_tower import GrayTower


class GrayBucharest(GrayTower):

    def __init__(self):
        super().__init__(3, 3)
        
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
        
        # self.ternary_gray_sequence = self.generate_m_ary_gray_code(self.n_disks)

    def solve(self, verbose=False):
        """Find the moves to solve the puzzle."""

        configurations = []
        last_pegs = self.ternary_gray_sequence[0]

        for i in range(len(self.ternary_gray_sequence)):
            ternary_gray_code = self.ternary_gray_sequence[i]
                
            self.move_disk(0, last_pegs[2], ternary_gray_code[2])
            self.move_disk(1, last_pegs[1], ternary_gray_code[1])
            self.move_disk(2, last_pegs[0], ternary_gray_code[0])

            last_pegs[0] = ternary_gray_code[0]
            last_pegs[1] = ternary_gray_code[1]
            last_pegs[2] = ternary_gray_code[2]

            configurations.append(copy.deepcopy(self.pegs))
        if verbose:
            self.pretty_print(configurations)
        return configurations
