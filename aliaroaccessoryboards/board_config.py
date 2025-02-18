from __future__ import annotations

from pathlib import Path
from typing import List, Union

import pydantic_yaml
from pydantic import BaseModel, Field


class InitializationCommands(BaseModel):
    """
    Commands to be executed on board reset/initialization.

    This class represents commands necessary for initializing the accessory board,
    including lists of relays to be opened or closed during the initialization process.

    :ivar open_relays: List of relay names that should be opened.
    :ivar close_relays: List of relay names that should be closed.
    """
    open_relays: List[str] = Field(default_factory=list)
    close_relays: List[str] = Field(default_factory=list)



class ConnectionPath(BaseModel):
    """
    Relays to close to connect two channels.

    Represents a list of relays to close to between a source and a destination channel.

    Used for defining and validating connections.

    :ivar src: The source of the connection path.
    :ivar dest: The destination of the connection path.
    :ivar relays: A list of relays to close to connect the source and destination.
    """
    src: str
    dest: str
    relays: List[str]


class ExclusiveConnection(BaseModel):
    """
    Represents a constraint that the given source can only be connected to one of the given destinations at a time.

    This is commonly used to define constraints such as only allowing a channel to be connected
    to one bus channel at a time.

    :ivar src: The connection source.
    :ivar dests: A list of exclusive destination endpoints for the source.
    """
    src: str
    dests: List[str]


class BoardConfig(BaseModel):
    """
    Represents the configuration for an ALIARO Accessory board, including details about relays,
    channels, connection paths, commands for initialization, exclusive connections, and current sensors.

    This class is used for loading, parsing, and handling board configuration data
    from various sources such as files, strings, or device names.

    :ivar relays: List of relay names associated with the board.
    :ivar channels: List of channel identifiers associated with the board.
    :ivar connection_paths: A list of connection paths specific to the board setup.
    :ivar initialization_commands: Commands used for initializing the board.
    :ivar exclusive_connections: List of exclusive connections.
    :ivar current_sensors: List of current sensor identifiers in the board.
    """
    schema_version: str = "1.0.0"
    relays: List[str]
    channels: List[str]
    connection_paths: List[ConnectionPath]
    initialization_commands: InitializationCommands = Field(default_factory=InitializationCommands)
    exclusive_connections: List[ExclusiveConnection] = Field(default_factory=list)
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