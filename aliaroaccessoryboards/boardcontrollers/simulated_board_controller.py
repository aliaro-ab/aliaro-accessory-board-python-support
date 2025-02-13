from typing import List

from aliaroaccessoryboards import BoardController

class SimulatedBoardController(BoardController):
    def __init__(self, relay_count: int, current_count: int):
        super().__init__(relay_count, current_count)
        self.device_relays = [False] * relay_count
        self.device_currents = [0] * current_count

    def read_relays_from_device(self) -> int:
        relay_mask = 0
        for i, relay in enumerate(self.device_relays):
            if relay:
                relay_mask |= (1 << i)  # Set the bit at position i
        return relay_mask

    def write_relays_to_device(self, relay_mask: int):
        self.device_relays = [(relay_mask & (1 << i)) > 0 for i in range(len(self.device_relays))]

    def read_currents_from_device(self) -> List[int]:
        return self.device_currents
