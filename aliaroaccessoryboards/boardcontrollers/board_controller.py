import math
from abc import abstractmethod, ABC
from typing import List


class BoardController(ABC):

    def __init__(self, relay_count: int, current_count: int):
        self.relay_count = relay_count
        self.current_count = current_count
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
            raise RuntimeError("Relay state is pending commit. Commit relays before reading.")
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