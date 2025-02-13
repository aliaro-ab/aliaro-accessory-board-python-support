# File: tests/test_accessory_board.py

from unittest.mock import Mock, patch, mock_open

import pytest
from aliaroaccessoryboards import BoardController, Topology, AccessoryBoard
from aliaroaccessoryboards.switch_config import InitialState


# Test: __init__ with valid topology file and reset=True
def test_accessory_board_init_with_reset():
    mock_controller = Mock(spec=BoardController)
    mock_topology = Mock(spec=Topology)
    mock_topology.initial_state = InitialState()
    mock_topology.connection_list = []
    mock_topology.channel_list = []
    mock_topology.relays = []
    mock_topology.mux_list = []

    with patch("aliaroaccessoryboards.accessory_board.pydantic_yaml.parse_yaml_raw_as", return_value=mock_topology):
        with patch("builtins.open", mock_open()):
            board = AccessoryBoard("mock_topology.yaml", mock_controller, reset=True)
            assert board.initial_state == mock_topology.initial_state
            assert board.connection_map == {}
            assert board.channels == set(mock_topology.channel_list)
            assert board.relays == set(mock_topology.relays)
            assert board.mux_list == mock_topology.mux_list
            assert board.controller == mock_controller
            assert isinstance(board.connections, set)


# Test: __init__ with valid topology file and reset=False
def test_accessory_board_init_without_reset():
    mock_controller = Mock(spec=BoardController)
    mock_topology = Mock(spec=Topology)
    mock_topology.initial_state = {}
    mock_topology.connection_list = []
    mock_topology.channel_list = []
    mock_topology.relays = []
    mock_topology.mux_list = []

    with patch("aliaroaccessoryboards.accessory_board.pydantic_yaml.parse_yaml_raw_as", return_value=mock_topology):
        with patch("builtins.open", mock_open()):
            with patch.object(AccessoryBoard, "reset") as mock_reset:
                board = AccessoryBoard("mock_topology.yaml", mock_controller, reset=False)
                mock_reset.assert_not_called()
                assert board.initial_state == mock_topology.initial_state
                assert board.connection_map == {}
                assert board.channels == set(mock_topology.channel_list)
                assert board.relays == set(mock_topology.relays)
                assert board.mux_list == mock_topology.mux_list
                assert board.controller == mock_controller
                assert isinstance(board.connections, set)


# Test: __init__ raises an exception if topology file is invalid
def test_accessory_board_init_invalid_topology():
    mock_controller = Mock(spec=BoardController)
    with patch("builtins.open", mock_open()), patch(
            "aliaroaccessoryboards.accessory_board.pydantic_yaml.parse_yaml_raw_as", side_effect=ValueError
    ):
        with pytest.raises(ValueError):
            AccessoryBoard("invalid_topology.yaml", mock_controller)
