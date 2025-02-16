import tempfile

import pytest

from aliaroaccessoryboards import SimulatedBoardController
from tests.shared import board_config


class TestBoardController:
    def test_init_with_board_config(self, board_config: board_config):
        controller = SimulatedBoardController(board_config)
        assert controller.relay_count == 4
        assert controller.current_count == 2
        assert controller._relay_buffer_size == 1
        assert controller._relay_state_buffer == [False, False, False, False]
        assert not controller._pending_commit

    def test_init_with_path(self, board_config: board_config):
        import pydantic_yaml
        with tempfile.NamedTemporaryFile(delete=False, suffix=".brd") as temp_file:
            pydantic_yaml.to_yaml_file(temp_file.name, board_config)

        controller = SimulatedBoardController(temp_file.name)
        assert controller.relay_count == 4
        assert controller.current_count == 2
        assert controller._relay_buffer_size == 1
        assert controller._relay_state_buffer == [False, False, False, False]
        assert not controller._pending_commit


def test_relay_initialization(board_config: board_config):
    controller = SimulatedBoardController(board_config)
    assert len(controller.relays) == 4
    assert controller.relays == [False, False, False, False]


def test_set_relay(board_config: board_config):

    controller = SimulatedBoardController(board_config)
    controller.set_relay(0, True)
    assert controller._relay_state_buffer == [True, False, False, False]
    assert controller._pending_commit is True


def test_set_all_relays(board_config: board_config):
    controller = SimulatedBoardController(board_config)
    controller.set_all_relays(True)
    assert controller._relay_state_buffer == [True, True, True, True]
    assert controller._pending_commit is True


def test_commit_relays(board_config: board_config):
    controller = SimulatedBoardController(board_config)
    controller.set_relay(0, True)
    controller.commit_relays()
    assert controller.read_relays_from_device() == 1
    assert controller._pending_commit is False
    assert controller.relays == [True, False, False, False]


def test_relays_pending_commit_error(board_config: board_config):
    controller = SimulatedBoardController(board_config)
    controller.set_relay(1, True)
    with pytest.raises(RuntimeError, match="Relay state is pending commit. Commit relays before reading."):
        _ = controller.relays
