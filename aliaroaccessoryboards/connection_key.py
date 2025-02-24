import collections
from typing import Iterator


class ConnectionKey(collections.abc.Set):
    def __init__(self, channel1: str, channel2: str):
        self._frozenset = frozenset([channel1, channel2])

    def __contains__(self, x: str) -> bool:
        return x in self._frozenset

    def __len__(self) -> int:
        return len(self._frozenset)

    def __iter__(self) -> Iterator[str]:
        return iter(self._frozenset)

    def __hash__(self) -> int:
        return hash(self._frozenset)

    def __str__(self) -> str:
        return " <--> ".join(sorted(self._frozenset))

    def __repr__(self) -> str:
        return str(self)
