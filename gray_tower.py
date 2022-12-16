import copy
import itertools


class GrayTower:
    def __init__(self, n_rigs, n_disks):
        self.n_rigs = n_rigs
        self.n_disks = n_disks
        self.rigs = self.populate_rigs()

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

    def generate_m_ary_gray_code(self, m):
        """Generate m-ary Gray code."""
        base = list(range(m))
        desc = list(range(m-1, -1, -1))
        asc = list(range(0, m))

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
            print_rigs = copy.deepcopy(configuration)
            for rig in print_rigs:
                padding = [self.n_disks]*(self.n_disks-len(rig))
                rig.extend(padding)
            smallest_disk_width = 3
            disk_widths = [
                x+smallest_disk_width for x in list(range(0, self.n_disks*2, 2))]
            base_width = disk_widths[-1] + 2
            disks_repr = [((base_width-x)//2)*' '+'0' * x +
                          ((base_width-x)//2)*' ' for x in disk_widths]
            rig_repr = [' '*(base_width//2)+"|"+' '*(base_width//2)]
            pretty_disks = disks_repr + rig_repr
            rig_str = list()
            for rig in print_rigs:
                rig_str.append([pretty_disks[a] for a in rig])
            for i in range(self.n_disks-1, -1, -1):
                for j in range(self.n_rigs):
                    out_str += rig_str[j][i]
                out_str += '\n'
            out_str += '='*(base_width*self.n_rigs)
            out_str += '\n'
            out_str += '\n'
        print(out_str)

    def pretty_print_configuration(self, configuration):
        """Pretty-print a specific configuration in a nice ascii-art form."""
        out_str = "\n"
        print_rigs = copy.deepcopy(configuration)
        for rig in print_rigs:
            padding = [self.n_disks]*(self.n_disks-len(rig))
            rig.extend(padding)
        smallest_disk_width = 3
        disk_widths = [
            x+smallest_disk_width for x in list(range(0, self.n_disks*2, 2))]
        base_width = disk_widths[-1] + 2
        disks_repr = [((base_width-x)//2)*' '+'0' * x +
                      ((base_width-x)//2)*' ' for x in disk_widths]
        rig_repr = [' '*(base_width//2)+"|"+' '*(base_width//2)]
        pretty_disks = disks_repr + rig_repr
        rig_str = list()
        for rig in print_rigs:
            rig_str.append([pretty_disks[a] for a in rig])
        for i in range(self.n_disks-1, -1, -1):
            for j in range(self.n_rigs):
                out_str += rig_str[j][i]
            out_str += '\n'
        out_str += '='*(base_width*self.n_rigs)
        out_str += '\n'
        out_str += '\n'
        return out_str
