import pytest

from aliaroaccessoryboards.boardcontrollers.simulated_board_controller import (
    SimulatedBoardController,
)
from tests.shared import board_config


@pytest.fixture
def simulated_board_controller(board_config: board_config) -> SimulatedBoardController:
    return SimulatedBoardController(board_config)


def test_read_relays_initial_state(simulated_board_controller) -> None:
    relay_state = simulated_board_controller.read_relays_from_device()
    assert relay_state == 0  # No relays should be active initially


def test_write_relays_to_device(simulated_board_controller) -> None:
    simulated_board_controller.write_relays_to_device(
        0b101
    )  # Activate relay 0 and relay 2
    relay_state = simulated_board_controller.read_relays_from_device()
    assert relay_state == 0b101


def test_read_currents_initial_state(simulated_board_controller) -> None:
    current_state = simulated_board_controller.read_currents_from_device()
    assert current_state == [0, 0]  # Initial currents should be 0


def test_relay_count_property(
    board_config: board_config, simulated_board_controller
) -> None:
    assert simulated_board_controller.relay_count == len(board_config.relays)


def test_current_count_property(
    board_config: board_config, simulated_board_controller
) -> None:
    assert simulated_board_controller.current_count == len(board_config.current_sensors)
