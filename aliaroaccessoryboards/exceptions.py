from typing import Set
from aliaroaccessoryboards.connection_key import ConnectionKey

class AccessoryBoardException(Exception):
    pass


class PathUnsupportedException(AccessoryBoardException):
    def __init__(self, connection_key: ConnectionKey, message: str = "No supported path exists between channels"):
        self.connection_key = connection_key
        self.message = message
        super().__init__(f"{self.message}: Requested: {self.connection_key}")


class ResourceInUseException(AccessoryBoardException):
    def __init__(self, relay_name: str, message="Relay in use by another connection"):
        self.relay_name = relay_name
        self.message = message
        super().__init__(f"{self.message}: Requested: {self.relay_name}")


class SourceConflictException(AccessoryBoardException):
    def __init__(self, connection_key: ConnectionKey, conflicting_sources: Set[str],
                 message="Connection would connect multiple sources", ):
        self.connection_key = connection_key
        self.conflicting_sources = conflicting_sources
        self.message = message
        super().__init__(
            f"{self.message}: Requested: {connection_key}, Conflicting Sources: {', '.join(conflicting_sources)}")


class MuxConflictException(AccessoryBoardException):
    def __init__(self, connection_key: ConnectionKey, existing_connection: str,
                 message="Connection would conflict with an existing mux connection"):
        self.connection_key = connection_key
        self.existing_connection = existing_connection
        self.message = message
        super().__init__(f"{self.message}: Requested: {connection_key}, Conflicting connection: {existing_connection}")
