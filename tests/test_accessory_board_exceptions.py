from aliaroaccessoryboards import SourceConflictException
from aliaroaccessoryboards.accessory_board import (
    ConnectionKey,
    PathUnsupportedException,
    ResourceInUseException,
    MuxConflictException,
)

def test_path_unsupported_exception_initialization() -> None:
    key = ConnectionKey("X", "Y")
    exception = PathUnsupportedException(key)
    assert exception.message == "No supported path exists between channels"
    assert exception.connection_key == key
    assert str(exception) == f"No supported path exists between channels: Requested: {key}"


def test_path_unsupported_exception_custom_message() -> None:
    key = ConnectionKey("X", "Y")
    custom_message = "Custom error message"
    exception = PathUnsupportedException(key, custom_message)
    assert exception.message == custom_message
    assert str(exception) == f"Custom error message: Requested: {key}"


def test_resource_in_use_exception_default_message() -> None:
    relay_name = "Relay123"
    exception = ResourceInUseException(relay_name)
    assert exception.message == "Relay in use by another connection"
    assert exception.relay_name == relay_name
    assert str(exception) == "Relay in use by another connection: Requested: Relay123"


def test_resource_in_use_exception_custom_message() -> None:
    relay_name = "Relay123"
    custom_message = "Custom error: Resource busy"
    exception = ResourceInUseException(relay_name, message=custom_message)
    assert exception.message == custom_message
    assert exception.relay_name == relay_name
    assert str(exception) == "Custom error: Resource busy: Requested: Relay123"


def test_mux_conflict_exception_initialization() -> None:
    key = ConnectionKey("Ch1", "Ch2")
    conflicting_connection = "Ch3 <--> Ch4"
    exception = MuxConflictException(key, conflicting_connection)
    assert exception.message == "Connection would conflict with an existing mux connection"
    assert exception.connection_key == key
    assert exception.existing_connection == conflicting_connection
    assert str(exception) == (
        "Connection would conflict with an existing mux connection: "
        f"Requested: {key}, Conflicting connection: Ch3 <--> Ch4"
    )


def test_mux_conflict_exception_custom_message() -> None:
    key = ConnectionKey("Ch1", "Ch2")
    conflicting_connection = "Ch3 <--> Ch4"
    custom_message = "Custom error message"
    exception = MuxConflictException(key, conflicting_connection, message=custom_message)
    assert exception.message == custom_message
    assert str(exception) == (
        "Custom error message: "
        f"Requested: {key}, Conflicting connection: Ch3 <--> Ch4"
    )

def test_source_conflict_exception_initialization() -> None:
    key = ConnectionKey("A", "B")
    conflicting_sources = {"C", "D", "E"}
    exception = SourceConflictException(key, conflicting_sources)
    assert exception.message == "Connection would connect multiple sources"
    assert exception.connection_key == key
    assert exception.conflicting_sources == conflicting_sources
    assert str(exception) == (
        "Connection would connect multiple sources: "
        f"Requested: {key}, Conflicting Sources: {', '.join(conflicting_sources)}"
    )

def test_source_conflict_exception_custom_message() -> None:
    key = ConnectionKey("A", "B")
    conflicting_sources = {"C", "D", "E"}
    custom_message = "Custom error message"
    exception = SourceConflictException(key, conflicting_sources, message=custom_message)
    assert exception.message == custom_message
    assert str(exception) == (
        "Custom error message: "
        f"Requested: {key}, Conflicting Sources: {', '.join(conflicting_sources)}"
    )


