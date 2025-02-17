from collections import Counter
from pathlib import Path
from typing import Set, Union, List, Dict, Iterable

from aliaroaccessoryboards import PathUnsupportedException, ResourceInUseException, SourceConflictException, \
    MuxConflictException
from aliaroaccessoryboards.board_config import BoardConfig, Connection, MuxItem
from aliaroaccessoryboards.boardcontrollers.board_controller import BoardController
from aliaroaccessoryboards.connection_key import ConnectionKey


class AccessoryBoard:
    def __init__(self, board_config: Union[str, Path, BoardConfig], board_controller: BoardController,
                 reset: bool = True):

        # Initialize configuration
        self.board_controller = board_controller

        # Process board config information
        self._board_config = self._initialize_board_config(board_config)
        self._initial_state = self._board_config.initial_state
        self.channels = frozenset(self._board_config.channel_list)
        self._connection_map = self._build_connection_map(self._board_config.connection_list)
        self.relays = tuple(self._board_config.relays)
        self._mux = self._build_mux_map(self._board_config.mux_list)

        # Initialize board state
        self._source_channels = set()
        self._relay_counter = Counter()
        self._connections: Set[ConnectionKey] = set()

        # Reset and check existing connections
        if reset:
            self.reset()
        self._check_and_add_existing_connections()

    @staticmethod
    def _initialize_board_config(board_config: Union[str, Path, BoardConfig]) -> BoardConfig:
        return board_config if isinstance(board_config, BoardConfig) else BoardConfig.from_brd_file(board_config)

    @staticmethod
    def _build_connection_map(connection_list: List[Connection]) -> Dict[ConnectionKey, List[str]]:
        """Create a map of connections to relays."""
        return {
            ConnectionKey(connection.src, connection.dest): connection.relays
            for connection in connection_list
        }

    @staticmethod
    def _build_mux_map(mux_list: List[MuxItem]) -> Dict[str, List[str]]:
        """Create the mux mapping from configuration."""
        return {mux_entry.src: mux_entry.dest for mux_entry in mux_list}

    def _check_and_add_existing_connections(self) -> None:
        """
        Checks if all relays are closed for any of the possible connections
        in the connection_map and adds those connections to self.connections.
        """
        for connection, relays in self._connection_map.items():
            if all(self._relay_counter[relay] > 0 for relay in relays):
                self._connections.add(connection)

    def connect_channels(self, channel1: str, channel2: str):
        """
        Connects two inputs on the device.

        This creates an electrical connection between two specified inputs
        on the device by closing the relays associated with the connection
        path between them.

        :raises KeyError: One or both of the specified channel names are invalid
        :raises PathUnsupportedException: The path is not possible.
        :raises ResourceInUseException: The path is possible, but elements of the path are in use by another existing path.
        :raises SourceConflictException: The path is possible, but connecting the channels will connect two sources.
        :raises MuxConflictException: The path is possible, but connecting the channels will conflict
                    with an existing connection in the mux.

        :param channel1: The identifier of the first input to connect.
        :param channel2: The identifier of the second input to connect.
        :return: None
        """
        connection_key = ConnectionKey(channel1, channel2)

        # If already connected, no action required.
        if connection_key in self._connections:
            return

        # Confirm that the connection is valid
        self._validate_channel_names(connection_key)
        self._validate_mux(connection_key)
        self._validate_single_source(connection_key)
        self._validate_path_exists(connection_key)

        # Get relays and confirm that they are not in use for any other paths
        relays_to_close = self._connection_map[connection_key]
        self._validate_relays(relays_to_close)

        # Close relays for the connection
        for relay in relays_to_close:
            self.board_controller.set_relay(self.relays.index(relay), True)
            self._relay_counter[relay] += 1

        # Commit the changes to the hardware
        self.board_controller.commit_relays()

        # Register the connection
        self._connections.add(connection_key)

    def _validate_relays(self, relays_to_close: List[str]) -> None:
        """
        Validates the list of relays to be closed.

        The method iterates over the provided list of relay identifiers and checks
        if any of the relays are currently in use.

        If a relay is found to be in use, a `ResourceInUseException` is raised.
        This ensures that no relays that are currently in operation are inadvertently
        closed.

        :param relays_to_close: List of relay identifiers to be validated.
        :raises ResourceInUseException: If any relay in the list is currently in use.
        :return: None
        """
        for relay in relays_to_close:
            if self._relay_counter[relay] > 0:
                raise ResourceInUseException(relay)

    def _validate_path_exists(self, connection_key: ConnectionKey) -> None:
        """
        Validates that the provided connection key exists within the connection map.

        This method checks if a given `connection_key` is present in the `connection_map`.
        If the key is not found, a `PathUnsupportedException` is raised.

        It is used to verify that the necessary path for the connection exists within the internal
        mapping.

        :param connection_key: The ConnectionKey object to be validated.
        :raises PathUnsupportedException: If the connection key does not exist
            in the connection map.
        :return: None
        """
        if connection_key not in self._connection_map:
            raise PathUnsupportedException(connection_key)

    def _validate_single_source(self, connection_key: ConnectionKey) -> None:
        """
        Validate that the connection does not connect multiple sources.
        
        Validates the connection by checking for conflicts among specified
        channels and their respective connections.
        This method ensures that multiple sources are not connected to each other.
        
        :param connection_key: The ConnectionKey object to be validated.
        :raises SourceConflictException: If conflicting source connections are detected.
        """

        # Check if both channels in the connection key are marked as sources
        if all(channel in self._source_channels for channel in connection_key):
            raise SourceConflictException(connection_key, set(connection_key))

        for channel in connection_key:
            if channel in self._source_channels:
                for connection in self._connections:
                    if any(other_channel in set(connection_key) - {channel} for other_channel in connection):
                        conflicting_sources = {ch for ch in connection if ch in self._source_channels}
                        if conflicting_sources:
                            raise SourceConflictException(connection_key, conflicting_sources)

    def _validate_mux(self, connection_key: ConnectionKey) -> None:
        """
        Validates that neither channel would conflict with an existing mux connection.

        :param connection_key: The ConnectionKey object to be validated.
        :raises MuxConflictException: If a conflicting channel is detected in the multiplexing
            configuration.
        """
        for channel in connection_key:
            if channel in self._mux:
                for connection in self._connections:
                    if channel in connection:
                        existing_connection = next(iter(set(connection) - {channel}))
                        if existing_connection in self._mux[channel]:
                            raise MuxConflictException(connection_key, existing_connection)

    def _validate_channel_names(self, channel_names: Iterable):
        """
        Validates the channel names exist in the device configuration.

        :param channel_names: ConnectionKey object that contains channel names to validate.
        :type channel_names: ConnectionKey
        :raises KeyError: If the provided ``connection_key`` contains channel
            names that are not part of the existing ``self.channels`` list.
        """
        invalid_channels = [str(ch) for ch in channel_names if ch not in self.channels]
        if invalid_channels:
            raise KeyError(f"Invalid channel names provided: {', '.join(invalid_channels)}")

    def disconnect_channels(self, channel1: str, channel2: str):
        """
        Disconnects two specified channels from each other.

        This ensures that the specified channels are no longer connected
        by opening the relays associated with the connection path between them.

        :param channel1: The identifier for the first channel to disconnect.
        :param channel2: The identifier for the second channel to disconnect.
        :return: None
        """
        self._validate_channel_names(ConnectionKey(channel1, channel2))
        connection_key = ConnectionKey(channel1, channel2)
        if connection_key not in self._connections:
            return  # No action needed if the channels are not connected.

        relays_to_open = self._connection_map.get(connection_key, [])

        for relay in relays_to_open:
            self._relay_counter[relay] -= 1
            if self._relay_counter[relay] == 0:
                self.board_controller.set_relay(self.relays.index(relay), False)

        # Commit the changes to the hardware
        self.board_controller.commit_relays()

        # Remove the connection from the active connections list.
        self._connections.remove(connection_key)

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
        self._connections.clear()
        self._relay_counter.clear()
        self._relay_counter.update(self._initial_state.close)

    def reset(self) -> None:
        """
        Reset relays on the device to their initial state.

        :return: None.
        """
        self.disconnect_all_channels()
        # Set relays to their initial states
        for relay in self._initial_state.open:
            self.board_controller.set_relay(self.relays.index(relay), False)
        for relay in self._initial_state.close:
            self.board_controller.set_relay(self.relays.index(relay), True)

        # Commit changes to the hardware
        self.board_controller.commit_relays()

        # Check if the initial relay states connect anything
        self._check_and_add_existing_connections()

    def mark_as_source(self, channel: str):
        self._validate_channel_names([channel])
        self._source_channels.add(channel)

    def unmark_as_source(self, channel: str):
        self._validate_channel_names([channel])
        self._source_channels.remove(channel)

    def print_connections(self) -> None:
        """
        Prints all connections present in the given AccessoryBoard.
         If there are no connections, a message indicating this is displayed.

        :return: None
        """
        if len(self._connections) == 0:
            print("No connections.")
            return
        connections = [str(connection) for connection in self._connections]
        connections.sort()
        for connection in sorted(connections):
            print(connection)
