import math
from abc import abstractmethod, ABC
from pathlib import Path
from typing import List, Union

from aliaroaccessoryboards.board_config import BoardConfig


class BoardController(ABC):
    """
    Controller class for managing relay boards.

    This abstract base class provides an interface for controlling accessory boards.
    It defines methods for interacting with relays and current sensors, along
    with managing relay states and committing relay changes to the device.
    """

    def __init__(self, board_config: Union[str, Path, BoardConfig]):
        if not isinstance(board_config, BoardConfig):
            board_config = BoardConfig.from_brd_file(board_config)
        self.relay_count = len(board_config.relays)
        self.current_count = len(board_config.current_sensors)
        self._relay_buffer_size = math.ceil(self.relay_count / 4)
        self._relay_state_buffer = [False] * self.relay_count
        self._pending_commit = False

    @abstractmethod
    def read_relays_from_device(self) -> int: ...

    @abstractmethod
    def write_relays_to_device(self, relay_mask: int): ...

    @abstractmethod
    def read_currents_from_device(self) -> List[int]: ...

    @property
    def relays(self) -> List[bool]:
        if self._pending_commit:
            raise RuntimeError(
                "Relay state is pending commit. Commit relays before reading."
            )
        raw = self.read_relays_from_device()
        states = []
        for idx in range(self.relay_count):
            states.append(bool(raw & 1 << idx))
        return states

    def set_relay(self, index: int, value: bool):
        self._relay_state_buffer[index] = value
        self._pending_commit = True

    def set_all_relays(self, value: bool):
        self._relay_state_buffer = [value] * self.relay_count
        self._pending_commit = True

    def commit_relays(self) -> None:
        raw = 0
        for idx, state in enumerate(self._relay_state_buffer):
            raw = raw | state << idx
        self.write_relays_to_device(raw)
        self._pending_commit = False
