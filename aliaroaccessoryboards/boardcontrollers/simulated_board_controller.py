from pathlib import Path
from typing import List, Union

from aliaroaccessoryboards.boardcontrollers.board_controller import BoardController
from aliaroaccessoryboards.board_config import  BoardConfig

class SimulatedBoardController(BoardController):
    """
    Simulated implementation of a board controller for testing and example purposes.

    This class provides a mock implementation of a board controller by simulating relay
    states and current measurements.

    This class is primarily used in contexts where hardware access is not available or when testing control logic.
    """
    def __init__(self, board_config: Union[str, Path, BoardConfig]):
        super().__init__(board_config)
        self.device_relays = [False] * self.relay_count
        self.device_currents = [0] * self.current_count

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
