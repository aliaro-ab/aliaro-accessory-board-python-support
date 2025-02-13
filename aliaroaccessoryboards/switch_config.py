from pathlib import Path
from typing import List, Union

import pydantic_yaml
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

    @classmethod
    def from_top_file(cls, top_file: Union[str, Path]) -> "Topology":
        with open(top_file) as f:
            top = pydantic_yaml.parse_yaml_raw_as(Topology, f.read())
        return top

    @classmethod
    def from_top_string(cls, top_string: str) -> "Topology":
        top = pydantic_yaml.parse_yaml_raw_as(Topology, top_string)
        return top
