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
