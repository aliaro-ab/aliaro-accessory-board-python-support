from collections import Counter
from typing import Set

import pydantic_yaml

from aliaroaccessoryboards import BoardController, Topology


class PathUnsupportedException(RuntimeError):
    pass


class ResourceInUseException(RuntimeError):
    pass


class SourceConflictException(RuntimeError):
    pass

class AccessoryBoard:
    def __init__(self, top_file, controller: BoardController, reset: bool = True):
        with open(top_file) as f:
            top = pydantic_yaml.parse_yaml_raw_as(Topology, f.read())
            # Relay states when the device is reset
            self.initial_state = top.initial_state

            # List of all available connections in the system.
            # When the user asks to connect two channels, the required relays are looked up in this list.
            self.connection_map = {}
            for connection in top.connection_list:
                key = {connection.src, connection.dest}
                value = connection.relays
                self.connection_map[key] = value

            # All possible channels
            self.channels = set(top.channel_list)

            # Channels that the user has marked as `source`, which prevents them from being connected to each other.
            self.source_channels = set()

            # All possible relays
            self.relays = set(top.relays)

            # The number of times each relay has been used in a connection.
            # This is used to ensure that a relay is not disconnected if another path is also using it.
            self.relay_counter = Counter(self.relays)

            # The RelayController used to actually set relay states.
            self.controller = controller

            # Connections that are currently active.
            self.connections: Set[Set] = set()

            # A list of channels that are exclusive,
            # meaning the src channel can only be connected to one of the dest channels at a time.
            self.mux_list = top.mux_list

            if reset:
                self.reset()

            # Check and add connections that are already closed
            self.check_and_add_existing_connections()

    def check_and_add_existing_connections(self):
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

        :raises PathUnsupportedException: The path is not possible.
        :raises ResourceInUseException: The path is possible, but elements of the path are in use by another existing path.
        :raises SourceConflictException: The path is possible, but connecting the channels will connect two sources.

        :param channel1: The identifier of the first input to connect.
        :param channel2: The identifier of the second input to connect.
        :return: None
        """
        if channel1 not in self.channels or channel2 not in self.channels:
            raise PathUnsupportedException(f"One or both channels {channel1}, {channel2} are not supported.")

        if channel1 in self.source_channels and channel2 in self.source_channels:
            raise SourceConflictException(f"Cannot connect source channels: {channel1}, {channel2}.")

        connection_key = {channel1, channel2}
        if connection_key not in self.connection_map:
            raise PathUnsupportedException(f"No path exists between channels {channel1} and {channel2}.")

        relays_to_close = self.connection_map[connection_key]

        for relay in relays_to_close:
            if self.relay_counter[relay] > 0:
                raise ResourceInUseException(f"Relay {relay} is currently in use by another connection.")

        # Close relays for the connection
        for relay in relays_to_close:
            self.controller.set_relay(int(relay), True)
            self.relay_counter[relay] += 1

        # Commit the changes to the hardware
        self.controller.commit_relays()

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
        connection_key = {channel1, channel2}
        if connection_key not in self.connections:
            return  # No action needed if the channels are not connected.

        relays_to_open = self.connection_map.get(connection_key, [])

        for relay in relays_to_open:
            self.relay_counter[relay] -= 1
            if self.relay_counter[relay] == 0:
                self.controller.set_relay(int(relay), False)

        # Commit the changes to the hardware
        self.controller.commit_relays()

        # Remove the connection from the active connections list.
        self.connections.remove(connection_key)

    def disconnect_all_channels(self):
        """
        Disconnects all existing connections to channels.

        This ensures that all existing connections between channels are
        disconnected.

        :return: None
        """
        for relay in self.relays:
            self.controller.set_relay(int(relay), False)
        self.controller.commit_relays()
        self.connections.clear()
        self.relay_counter.clear()
        self.relay_counter.update(self.initial_state.close)

    def reset(self):
        """
        Reset relays on the device to their initial state.

        :return: None.
        """
        # Set relays to their initial states
        for relay in self.initial_state.open:
            self.controller.set_relay(int(relay), False)
        for relay in self.initial_state.close:
            self.controller.set_relay(int(relay), True)

        # Commit changes to the hardware
        self.controller.commit_relays()

        # Update relay counter state to match the initial configuration
        self.relay_counter.clear()
        self.relay_counter.update(self.initial_state.close)

        self.check_and_add_existing_connections()



