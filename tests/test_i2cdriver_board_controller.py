from unittest.mock import MagicMock

import pytest

from aliaroaccessoryboards.boardcontrollers.i2cdriver_board_controller import (
    I2CDriverBoardController,
)
from tests.shared import board_config


@pytest.fixture
def mock_i2c_driver() -> MagicMock:
    return MagicMock()


@pytest.fixture
def i2c_driver_board_controller(
    mock_i2c_driver, board_config: board_config
) -> I2CDriverBoardController:
    return I2CDriverBoardController(mock_i2c_driver, 0x40, board_config)


def test_read_relays_from_device(i2c_driver_board_controller, mock_i2c_driver) -> None:
    mock_i2c_driver.regrd.return_value = 3  # Simulate relay read result
    result = i2c_driver_board_controller.read_relays_from_device()
    assert result == 3
    mock_i2c_driver.regrd.assert_called_once_with(0x40, 128, "<H")


def test_write_relays_to_device(i2c_driver_board_controller, mock_i2c_driver) -> None:
    relay_mask = 0b1010
    i2c_driver_board_controller.write_relays_to_device(relay_mask)
    mock_i2c_driver.regwr.assert_called_once_with(
        0x40, 160, relay_mask.to_bytes(1, byteorder="little")
    )


def test_read_currents_from_device(
    i2c_driver_board_controller, mock_i2c_driver, board_config: board_config
) -> None:
    current_count = len(board_config.current_sensors)
    i2c_driver_board_controller.current_count = current_count
    mock_i2c_driver.regrd.return_value = [123, 456]  # Example current reading
    result = i2c_driver_board_controller.read_currents_from_device()
    assert result == [123, 456]
    mock_i2c_driver.regrd.assert_called_once_with(0x40, 0, f"{current_count}h")


def test_write_relays_multiple_boards(
    i2c_driver_board_controller, mock_i2c_driver, board_config: board_config
) -> None:
    relay_mask = 0b1010
    i2c_driver_board_controller.write_relays_to_device(relay_mask)
    mock_i2c_driver.regwr.assert_called_with(
        0x40, 160, relay_mask.to_bytes(1, byteorder="little")
    )

    relay_mask = 0b1001
    i2c_driver_board_controller = I2CDriverBoardController(
        mock_i2c_driver, 0x25, board_config
    )
    i2c_driver_board_controller.write_relays_to_device(relay_mask)
    mock_i2c_driver.regwr.assert_called_with(
        0x25, 160, relay_mask.to_bytes(1, byteorder="big")
    )
