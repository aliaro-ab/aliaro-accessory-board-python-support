from dataclasses import dataclass, field
from typing import List


@dataclass
class Relay:
    name: str
    offset: int = 0
    active_low: bool = False


@dataclass
class InitialState:
    open: List[str] = field(default_factory=list)
    close: List[str] = field(default_factory=list)



@dataclass
class Connection:
    src: str
    dest: str
    relays: List[str]


@dataclass
class MuxItem:
    src: str
    dest: List[str]


@dataclass
class Topology:
    relays: List[Relay]
    channel_list: List[str]
    connection_list: List[Connection]
    initial_state: InitialState = InitialState()
    mux_list: List[MuxItem] = field(default_factory=list)
