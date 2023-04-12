import copy


class GrayTower:
    def __init__(self, n_pegs, n_disks):
        self.n_pegs = n_pegs
        self.n_disks = n_disks
        self.pegs = self.populate_pegs()

    def find_allowed(self, disk):
        """
        Return index of the peg to move the disk to, with respect to allowed moves
        move is allowed if the peg is empty or the disk on the peg is bigger than the
        one we are placing on the top of it.
        """
        for idx, peg in enumerate(self.pegs):
            if len(peg) == 0 or peg[-1] > disk:
                return idx

    def find_peg(self, disk):
        """Find the pegs where the disk lies on."""
        for idx, peg in enumerate(self.pegs):
            if len(peg) > 0:
                if peg[-1] == disk:
                    return idx

    def move_disk(self, disk_to_move, current_peg_idx, next_peg_idx):
        """Move the disk from the current ring to the next one."""
        if current_peg_idx != next_peg_idx:
            self.pegs[current_peg_idx] = self.pegs[current_peg_idx][:-1]
            self.pegs[next_peg_idx].append(disk_to_move)

    def check_objective(self):
        """Check if game ended."""
        return self.pegs == [[], [], list(range(self.n_disks-1, -1, -1))]

    def populate_pegs(self):
        """Populate pegs with disks."""
        pegs = [list(range(self.n_disks-1, -1, -1)), [], []]
        return pegs

    def generate_m_ary_gray_code(self, m):
        """Generate m-ary Gray code."""
        base = list(range(m))
        desc = list(range(m-1, -1, -1))
        asc = list(range( m))

        for _ in range(m-1):
            p = []
            for i, b in enumerate(base):
                if i % 2 == 0:
                    for a in asc:
                        p += [str(b)+str(a)]
                else:
                    for d in desc:
                        p += [str(b)+str(d)]
            base = p
        p = [[int(n) for n in x] for x in p]
        return p

    def pretty_print(self, configurations):
        """Pretty-print the solution configurations in a nice ascii-art form."""
        out_str = "\n"
        for configuration in configurations:
            print_pegs = copy.deepcopy(configuration)
            for peg in print_pegs:
                padding = [self.n_disks]*(self.n_disks-len(peg))
                peg.extend(padding)
            smallest_disk_width = 3
            disk_widths = [
                x+smallest_disk_width for x in list(range(0, self.n_disks*2, 2))]
            base_width = disk_widths[-1] + 2
            disks_repr = [((base_width-x)//2)*' '+'0' * x +
                          ((base_width-x)//2)*' ' for x in disk_widths]
            peg_repr = [' '*(base_width//2)+"|"+' '*(base_width//2)]
            pretty_disks = disks_repr + peg_repr
            peg_str = list()
            for peg in print_pegs:
                peg_str.append([pretty_disks[a] for a in peg])
            for i in range(self.n_disks-1, -1, -1):
                for j in range(self.n_pegs):
                    out_str += peg_str[j][i]
                out_str += '\n'
            out_str += '='*(base_width*self.n_pegs)
            out_str += '\n'
            out_str += '\n'
        print(out_str)

    def pretty_print_configuration(self, configuration):
        """Pretty-print a specific configuration in a nice ascii-art form."""
        out_str = "\n"
        print_pegs = copy.deepcopy(configuration)
        for peg in print_pegs:
            padding = [self.n_disks]*(self.n_disks-len(peg))
            peg.extend(padding)
        smallest_disk_width = 3
        disk_widths = [
            x+smallest_disk_width for x in list(range(0, self.n_disks*2, 2))]
        base_width = disk_widths[-1] + 2
        disks_repr = [((base_width-x)//2)*' '+'0' * x +
                      ((base_width-x)//2)*' ' for x in disk_widths]
        peg_repr = [' '*(base_width//2)+"|"+' '*(base_width//2)]
        pretty_disks = disks_repr + peg_repr
        peg_str = list()
        for peg in print_pegs:
            peg_str.append([pretty_disks[a] for a in peg])
        for i in range(self.n_disks-1, -1, -1):
            for j in range(self.n_pegs):
                out_str += peg_str[j][i]
            out_str += '\n'
        out_str += '='*(base_width*self.n_pegs)
        out_str += '\n'
        out_str += '\n'
        return out_str
