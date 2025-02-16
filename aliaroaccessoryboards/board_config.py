from __future__ import annotations

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


class BoardConfig(BaseModel):
    relays: List[str]
    channel_list: List[str]
    connection_list: List[Connection]
    initial_state: InitialState = Field(default_factory=InitialState)
    mux_list: List[MuxItem] = Field(default_factory=list)
    current_sensors: List[str] = Field(default_factory=list)

    @classmethod
    def from_brd_file(cls, top_file: Union[str, Path]) -> BoardConfig:
        with open(top_file) as f:
            top = pydantic_yaml.parse_yaml_raw_as(BoardConfig, f.read())
        return top

    @classmethod
    def from_brd_string(cls, top_string: str) -> BoardConfig:
        top = pydantic_yaml.parse_yaml_raw_as(BoardConfig, top_string)
        return top

    @classmethod
    def from_device_name(cls, device_name: str) -> BoardConfig:
        import os
        top_file = os.path.join(os.path.dirname(__file__), "boards", f"{device_name}.brd")
        return cls.from_brd_file(top_file)