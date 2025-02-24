import pytest
from unittest.mock import MagicMock
from aliaroaccessoryboards import (
    SimulatedBoardController,
    PathUnsupportedException,
    ResourceInUseException,
    SourceConflictException,
    ExclusiveConnectionConflictException,
)
from aliaroaccessoryboards.accessory_board import AccessoryBoard
from aliaroaccessoryboards.connection_key import ConnectionKey
from tests.shared import board_config


def test_connection_key_repr() -> None:
    """Test the __repr__ of the ConnectionKey class."""
    key = ConnectionKey("A", "B")
    assert repr(key) == str(key)


# noinspection DuplicatedCode
def test_accessory_board_initialization_with_reset_success(board_config: board_config):
    board_config.initialization_commands.open_relays = ["AC", "BD"]
    board_config.initialization_commands.close_relays = ["AD", "BC"]
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    assert accessory_board._board_config == board_config
    assert accessory_board.board_controller == board_controller
    assert accessory_board._initial_state == board_config.initialization_commands
    assert accessory_board.channels == set(board_config.channels)
    assert isinstance(accessory_board._connection_map, dict)
    assert list(accessory_board.relays) == board_config.relays
    assert isinstance(accessory_board._exclusive_connections, dict)
    assert isinstance(accessory_board._relay_counter, dict)
    assert accessory_board._source_channels == set()
    assert accessory_board._connections == {
        ConnectionKey("A", "D"),
        ConnectionKey("B", "C"),
    }


# noinspection DuplicatedCode
def test_accessory_board_initialization_without_reset_success(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=False,
    )
    assert accessory_board._board_config == board_config
    assert accessory_board.board_controller == board_controller
    assert accessory_board._initial_state == board_config.initialization_commands
    assert accessory_board.channels == set(board_config.channels)
    assert isinstance(accessory_board._connection_map, dict)
    assert list(accessory_board.relays) == board_config.relays
    assert isinstance(accessory_board._exclusive_connections, dict)
    assert isinstance(accessory_board._relay_counter, dict)
    assert accessory_board._source_channels == set()
    assert (
        accessory_board._connections == set()
    )  # No board reset, so no connections should be present.


# noinspection DuplicatedCode
def test_accessory_board_connect_valid_channels_success(board_config: board_config):
    board_controller = SimulatedBoardController(board_config)
    board_controller.set_relay = MagicMock()
    board_controller.commit_relays = MagicMock()
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.connect_channels("A", "C")
    assert accessory_board._connections == {ConnectionKey("A", "C")}
    assert ConnectionKey("A", "C") in accessory_board._connections
    assert accessory_board._relay_counter["AC"] == 1
    assert not accessory_board.board_controller._pending_commit
    board_controller.set_relay.assert_called_with(board_config.relays.index("AC"), True)


def test_print_connections_with_no_connections(board_config: board_config, capsys):
    """Test print_connections function when no connections exist."""
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Call the function and capture the output
    accessory_board.print_connections()
    captured = capsys.readouterr()
    assert captured.out.strip() == "No connections."


def test_print_connections_with_active_connections(board_config: board_config, capsys):
    """Test print_connections function with active connections."""
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.connect_channels("A", "C")
    accessory_board.connect_channels("B", "D")

    # Call the function and capture the output
    accessory_board.print_connections()
    captured = capsys.readouterr()
    expected_output = "A <--> C\nB <--> D"
    assert captured.out.strip() == expected_output


# noinspection DuplicatedCode
def test_accessory_board_connect_valid_channels_already_connected_success(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    board_controller.set_relay = MagicMock()
    board_controller.commit_relays = MagicMock()
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.connect_channels("A", "C")
    assert accessory_board._connections == {ConnectionKey("A", "C")}
    board_controller.set_relay.assert_called_with(board_config.relays.index("AC"), True)
    assert not accessory_board.board_controller._pending_commit

    # Call again with the same connection, verifying set_relay and commit_relays are not called again.
    board_controller.set_relay.reset_mock()
    board_controller.commit_relays.reset_mock()
    accessory_board.connect_channels("A", "C")
    assert accessory_board._connections == {ConnectionKey("A", "C")}
    board_controller.set_relay.assert_not_called()
    board_controller.commit_relays.assert_not_called()


# noinspection DuplicatedCode
def test_accessory_board_disconnect_valid_channels_success(board_config: board_config):
    board_controller = SimulatedBoardController(board_config)
    board_controller.set_relay = MagicMock()
    board_controller.commit_relays = MagicMock()
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    accessory_board.connect_channels("A", "C")
    assert accessory_board._connections == {ConnectionKey("A", "C")}
    assert accessory_board._relay_counter["AC"] == 1

    accessory_board.disconnect_channels("A", "C")
    assert accessory_board._connections == set()  # Connections should now be empty
    assert (
        accessory_board._relay_counter["AC"] == 0
    )  # Relay counter should be decremented
    assert not accessory_board.board_controller._pending_commit
    board_controller.set_relay.assert_called_with(
        board_config.relays.index("AC"), False
    )


def test_accessory_board_disconnect_valid_channels_not_connected_no_op(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    board_controller.set_relay = MagicMock()
    board_controller.commit_relays = MagicMock()
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Ensure no connections exist to begin with
    assert accessory_board._connections == set()

    accessory_board.disconnect_channels("A", "C")
    # No change expected as there was no connection
    assert accessory_board._connections == set()
    assert "AC" not in accessory_board._relay_counter
    assert not accessory_board.board_controller._pending_commit


def test_accessory_board_disconnect_multiple_connections_success(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    board_controller.set_relay = MagicMock()
    board_controller.commit_relays = MagicMock()
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    accessory_board.connect_channels("A", "C")
    accessory_board.connect_channels("B", "D")
    assert accessory_board._connections == {
        ConnectionKey("A", "C"),
        ConnectionKey("B", "D"),
    }
    assert accessory_board._relay_counter["AC"] == 1
    assert accessory_board._relay_counter["BD"] == 1

    accessory_board.disconnect_channels("A", "C")
    assert accessory_board._connections == {ConnectionKey("B", "D")}
    assert accessory_board._relay_counter["AC"] == 0
    assert accessory_board._relay_counter["BD"] == 1
    board_controller.set_relay.assert_any_call(board_config.relays.index("AC"), False)
    board_controller.set_relay.assert_any_call(board_config.relays.index("BD"), True)
    assert not accessory_board.board_controller._pending_commit


@pytest.mark.parametrize(
    "test_input",
    [
        (("A", "E"), KeyError),  # E is an invalid key
        (("E", "A"), KeyError),  # E is an invalid key
        (("E", "F"), KeyError),  # E and F are invalid keys
        (("A", ""), KeyError),  # Empty String is an invalid key
        (("", "A"), KeyError),  # Empty String is an invalid key
        (("", ""), KeyError),  # Empty String is an invalid key
        (("A", None), KeyError),  # None is an invalid key
        ((None, "A"), KeyError),  # None is an invalid key
        ((None, None), KeyError),  # None is an invalid key
    ],
)
def test_accessory_board_connect_bad_input_raises_key_error(
    board_config: board_config, test_input
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    with pytest.raises(KeyError):
        accessory_board.connect_channels(*test_input)


def test_accessory_board_connect_no_path_raises_path_unsupported_exception(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    with pytest.raises(PathUnsupportedException):
        accessory_board.connect_channels("A", "B")  # No path exists between A and B


def test_accessory_board_connect_relay_in_other_path_raises_resource_in_use_exception(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    accessory_board.connect_channels("A", "C")  # Uses relay AC
    with pytest.raises(ResourceInUseException):
        accessory_board.connect_channels("X", "Y")  # Uses relays AC and BD


def test_accessory_board_direct_connect_two_sources_raises_source_conflict_exception(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.mark_as_source("A")
    accessory_board.mark_as_source("C")
    with pytest.raises(SourceConflictException):
        accessory_board.connect_channels("A", "C")


def test_accessory_board_indirect_connect_two_sources_raises_source_conflict_exception(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.mark_as_source("A")
    accessory_board.mark_as_source("B")
    accessory_board.mark_as_source("A")
    accessory_board.mark_as_source("B")
    accessory_board.connect_channels("A", "C")
    with pytest.raises(SourceConflictException):
        accessory_board.connect_channels("B", "C")


def test_accessory_board_unmark_as_source(board_config: board_config):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Mark a channel as a source
    accessory_board.mark_as_source("A")
    assert "A" in accessory_board._source_channels

    # Unmark it
    accessory_board.unmark_as_source("A")
    assert "A" not in accessory_board._source_channels


def test_accessory_board_mark_as_source_valid_channel(board_config: board_config):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Mark a channel as a source
    accessory_board.mark_as_source("A")
    assert "A" in accessory_board._source_channels


def test_accessory_board_mark_as_source_invalid_channel_raises_key_error(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Attempt marking an invalid channel and assert it raises KeyError
    with pytest.raises(KeyError):
        accessory_board.mark_as_source("InvalidChannel")


def test_accessory_board_mark_as_source_already_marked(board_config: board_config):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Mark a channel as a source twice
    accessory_board.mark_as_source("A")
    assert "A" in accessory_board._source_channels

    # Marking again should not raise any error or duplicate in source_channels
    accessory_board.mark_as_source("A")
    assert len(accessory_board._source_channels) == 1


def test_accessory_board_unmark_as_source_not_marked_raises_key_error(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )

    # Ensure the channel is not marked as a source
    assert "A" not in accessory_board._source_channels

    with pytest.raises(KeyError):
        accessory_board.unmark_as_source("A")


def test_accessory_board_connect_two_exclusive_values_raises_exclusive_connection_conflict_exception(
    board_config: board_config,
):
    board_controller = SimulatedBoardController(board_config)
    accessory_board = AccessoryBoard(
        board_config=board_config,
        board_controller=board_controller,
        reset=True,
    )
    accessory_board.connect_channels("A", "C")
    with pytest.raises(ExclusiveConnectionConflictException):
        accessory_board.connect_channels("A", "D")
