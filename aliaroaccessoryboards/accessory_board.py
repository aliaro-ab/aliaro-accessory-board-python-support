from collections import Counter
from pathlib import Path
from typing import Set, Union, FrozenSet, List, Dict

from aliaroaccessoryboards.board_config import BoardConfig, Connection, MuxItem
from aliaroaccessoryboards.boardcontrollers.board_controller import BoardController


class AccessoryBoardException(Exception):
    pass


class PathUnsupportedException(AccessoryBoardException):
    pass


class ResourceInUseException(AccessoryBoardException):
    pass


class SourceConflictException(AccessoryBoardException):
    pass


class MuxConflictException(AccessoryBoardException):
    pass


class AccessoryBoard:
    def __init__(self, board_config: Union[str, Path, BoardConfig], board_controller: BoardController,
                 reset: bool = True):
        # Initialize configuration
        self.board_config = self._initialize_board_config(board_config)
        self.board_controller = board_controller

        # Initialize board state
        self.initial_state = self.board_config.initial_state
        self.connection_map = self._build_connection_map(self.board_config.connection_list)
        self.channels = set(self.board_config.channel_list)
        self.source_channels = set()
        self.relays = self.board_config.relays
        self.relay_counter = self._initialize_relay_counter(self.relays)
        self.connections: Set[FrozenSet] = set()
        self.mux = self._build_mux_map(self.board_config.mux_list)

        # Reset and check existing connections
        if reset:
            self.reset()
        self._check_and_add_existing_connections()

    def _initialize_board_config(self, board_config: Union[str, Path, BoardConfig]) -> BoardConfig:
        """Ensure `board_config` is a `BoardConfig` object."""
        return board_config if isinstance(board_config, BoardConfig) else BoardConfig.from_brd_file(board_config)

    def _build_connection_map(self, connection_list: List[Connection]) -> Dict[FrozenSet, List[str]]:
        """Create a map of connections to relays."""
        return {
            frozenset({connection.src, connection.dest}): connection.relays
            for connection in connection_list
        }

    def _initialize_relay_counter(self, relays: List[str]) -> Counter:
        """Initialize a counter for relay use tracking."""
        return Counter(relays)

    def _build_mux_map(self, mux_list: List[MuxItem]) -> Dict[str, List[str]]:
        """Create the mux mapping from configuration."""
        return {mux_entry.src: mux_entry.dest for mux_entry in mux_list}

    def _check_and_add_existing_connections(self) -> None:
        """
        Checks if all relays are closed for any of the possible connections
        in the connection_map and adds those connections to self.connections.
        """
        for connection, relays in self.connection_map.items():
            if all(self.relay_counter[relay] > 0 for relay in relays):
                self.connections.add(connection)

    def connect_channels(self, channel1: str, channel2: str):
        """
        Connects two inputs on the device.

        This creates an electrical connection between two specified inputs
        on the device by closing the relays associated with the connection
        path between them.

        :raises ValueError: One or both of the specified channel names are invalid
        :raises PathUnsupportedException: The path is not possible.
        :raises ResourceInUseException: The path is possible, but elements of the path are in use by another existing path.
        :raises SourceConflictException: The path is possible, but connecting the channels will connect two sources.

        :param channel1: The identifier of the first input to connect.
        :param channel2: The identifier of the second input to connect.
        :return: None
        """

        # Check that channel names are valid.
        unsupported_channels = [ch for ch in (channel1, channel2) if ch not in self.channels]
        if unsupported_channels:
            raise ValueError(f"The following channel names are invalid: {', '.join(unsupported_channels)}")

        for channel in (channel1, channel2):
            if channel in self.mux:
                for connection in self.connections:
                    if channel in connection:
                        existing_connection = next(iter(connection - {channel}))
                        if existing_connection in self.mux[channel]:
                            raise MuxConflictException(
                                f"Channel '{channel}' is already connected to '{existing_connection}', "
                                f"which conflicts with the requested connection to '{channel2}'."
                            )

        # Check that these aren't both source channels
        if channel1 in self.source_channels and channel2 in self.source_channels:
            raise SourceConflictException(f"Cannot connect source channels: {channel1}, {channel2}.")

        # Check that if one of the channels is a source channel, the other isn't already connected to a source.
        if channel1 in self.source_channels:
            for connection in self.connections:
                if channel2 in connection:
                    conflicting_sources = {ch for ch in connection if ch in self.source_channels}
                    if conflicting_sources:
                        raise SourceConflictException(
                            f"Connecting {channel1} to {channel2} would connect multiple sources: {', '.join(conflicting_sources)}. "
                            f"{channel2} is already connected to {', '.join(connection - {channel2})}."
                        )
        elif channel2 in self.source_channels:
            for connection in self.connections:
                if channel1 in connection:
                    conflicting_sources = {ch for ch in connection if ch in self.source_channels}
                    if conflicting_sources:
                        raise SourceConflictException(
                            f"Connecting {channel2} to {channel1} would connect multiple sources: {', '.join(conflicting_sources)}. "
                            f"{channel1} is already connected to {', '.join(connection - {channel1})}."
                        )

        connection_key = frozenset({channel1, channel2})
        if connection_key not in self.connection_map:
            raise PathUnsupportedException(f"No path exists between channels {channel1} and {channel2}.")

        relays_to_close = self.connection_map[connection_key]

        for relay in relays_to_close:
            if self.relay_counter[relay] > 0:
                raise ResourceInUseException(f"Relay {relay} is currently in use by another connection.")

        # Close relays for the connection
        for relay in relays_to_close:
            self.board_controller.set_relay(self.relays.index(relay), True)
            self.relay_counter[relay] += 1

        # Commit the changes to the hardware
        self.board_controller.commit_relays()

        # Register the connection
        self.connections.add(connection_key)

    def disconnect_channels(self, channel1: str, channel2: str):
        """
        Disconnects two specified channels from each other.

        This ensures that the specified channels are no longer connected
        by opening the relays associated with the connection path between them.

        :param channel1: The identifier for the first channel to disconnect.
        :param channel2: The identifier for the second channel to disconnect.
        :return: None
        """
        connection_key = frozenset({channel1, channel2})
        if connection_key not in self.connections:
            return  # No action needed if the channels are not connected.

        relays_to_open = self.connection_map.get(connection_key, [])

        for relay in relays_to_open:
            self.relay_counter[relay] -= 1
            if self.relay_counter[relay] == 0:
                self.board_controller.set_relay(self.relays.index(relay), False)

        # Commit the changes to the hardware
        self.board_controller.commit_relays()

        # Remove the connection from the active connections list.
        self.connections.remove(connection_key)

    def disconnect_all_channels(self) -> None:
        """
        Disconnects all existing connections to channels.

        This ensures that all existing connections between channels are
        disconnected.

        :return: None
        """
        for relay in self.relays:
            self.board_controller.set_relay(self.relays.index(relay), False)
        self.board_controller.commit_relays()
        self.connections.clear()
        self.relay_counter.clear()
        self.relay_counter.update(self.initial_state.close)

    def reset(self) -> None:
        """
        Reset relays on the device to their initial state.

        :return: None.
        """
        self.disconnect_all_channels()
        # Set relays to their initial states
        for relay in self.initial_state.open:
            self.board_controller.set_relay(self.relays.index(relay), False)
        for relay in self.initial_state.close:
            self.board_controller.set_relay(self.relays.index(relay), True)

        # Commit changes to the hardware
        self.board_controller.commit_relays()

        # Clear connections and check for any connections on initial state
        self._check_and_add_existing_connections()

    def mark_as_source(self, channel: str):
        self.source_channels.add(channel)

    def unmark_as_source(self, channel: str):
        self.source_channels.remove(channel)


def print_connections(board: AccessoryBoard):
    if len(board.connections) == 0:
        print("No connections.")
        return
    for connection in board.connections:
        connection = list(connection)
        print(connection[0], "<->", connection[1])
