from typing import List

from pydantic import BaseModel, Field


class InitialState(BaseModel):
    open: List[str] = Field(default_factory=list)
    close: List[str] = Field(default_factory=list)



class Connection(BaseModel):
    src: str
    dest: str
    relays: List[str]


class MuxItem(BaseModel):
    src: str
    dest: List[str]


class Topology(BaseModel):
    relays: List[str]
    channel_list: List[str]
    connection_list: List[Connection]
    initial_state: InitialState = Field(default_factory=InitialState)
    mux_list: List[MuxItem] = Field(default_factory=list)

