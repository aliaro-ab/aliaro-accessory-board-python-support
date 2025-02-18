import pytest
from ruamel.yaml import YAMLError

from aliaroaccessoryboards.board_config import BoardConfig, ConnectionPath, InitializationCommands, ExclusiveConnection
from tests.shared import yaml_config


# Happy Path
def test_board_config_from_yaml_success(yaml_config: yaml_config):
    config = BoardConfig.from_brd_string(yaml_config)

    assert isinstance(config, BoardConfig)
    assert config.relays == ["RELAY_CH01", "RELAY_CH02"]
    assert config.channels == ["DUT_CH01", "DUT_CH02", "BUS"]


# BRD File sanity checks
def test_board_config_from_brd_file_success(tmp_path, yaml_config) -> None:
    temp_file = tmp_path / "valid_board.brd"
    temp_file.write_text(yaml_config)

    config = BoardConfig.from_brd_file(temp_file)

    assert isinstance(config, BoardConfig)
    assert config.relays == ["RELAY_CH01", "RELAY_CH02"]
    assert config.channels == ["DUT_CH01", "DUT_CH02", "BUS"]


def test_board_config_from_invalid_brd_file_raises_yaml_error(tmp_path) -> None:
    invalid_content = """
    relays: - relay1 - relay2
    """
    temp_file = tmp_path / "invalid_board.brd"
    temp_file.write_text(invalid_content)

    with pytest.raises(YAMLError):
        BoardConfig.from_brd_file(temp_file)


def test_board_config_from_nonexistent_file_raises_file_not_found_error(tmp_path) -> None:
    nonexistent_file = tmp_path / "nonexistent.brd"

    with pytest.raises(FileNotFoundError):
        BoardConfig.from_brd_file(nonexistent_file)


def test_board_config_from_device_name_success() -> None:
    config = BoardConfig.from_device_name("32ch_instrumentation_switch")

    assert isinstance(config, BoardConfig)


# Validation Tests
def test_connection_path_invalid_relay_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Relay 'INVALID_RELAY' not found.*"):
        BoardConfig(
            relays=["RELAY_A"],
            channels=["CHANNEL_1", "CHANNEL_2"],
            connection_paths=[
                ConnectionPath(
                    src="CHANNEL_1",
                    dest="CHANNEL_2",
                    relays=["INVALID_RELAY"]
                )
            ]
        )


def test_connection_path_invalid_channel_source_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Source channel 'INVALID_CHANNEL' not found.*"):
        BoardConfig(
            relays=["RELAY_A"],
            channels=["CHANNEL_2"],
            connection_paths=[
                ConnectionPath(
                    src="INVALID_CHANNEL",
                    dest="CHANNEL_2",
                    relays=["RELAY_A"]
                )
            ]
        )


def test_connection_path_invalid_channel_destination_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Destination channel 'INVALID_CHANNEL' not found.*"):
        BoardConfig(
            relays=["RELAY_A"],
            channels=["CHANNEL_1"],
            connection_paths=[
                ConnectionPath(
                    src="CHANNEL_1",
                    dest="INVALID_CHANNEL",
                    relays=["RELAY_A"]
                )
            ]
        )


def test_initialization_commands_invalid_open_relay_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Relay 'INVALID_RELAY' not found in relays.*"):
        BoardConfig(
            relays=["RELAY_A"],
            channels=["CHANNEL_1", "CHANNEL_2"],
            connection_paths=[
                ConnectionPath(
                    src="CHANNEL_1",
                    dest="CHANNEL_2",
                    relays=["RELAY_A"]
                )
            ],
            initialization_commands=InitializationCommands(open_relays=["INVALID_RELAY"])
        )


def test_initialization_commands_invalid_close_relay_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Relay 'INVALID_RELAY' not found in relays.*"):
        BoardConfig(
            relays=["RELAY_A"],
            channels=["CHANNEL_1", "CHANNEL_2"],
            connection_paths=[
                ConnectionPath(
                    src="CHANNEL_1",
                    dest="CHANNEL_2",
                    relays=["RELAY_A"]
                )
            ],
            initialization_commands=InitializationCommands(close_relays=["INVALID_RELAY"])
        )


def test_validate_exclusive_connections_with_invalid_source() -> None:
    with pytest.raises(ValueError, match="Source channel 'INVALID_CHANNEL' not found in channels."):
        BoardConfig(
            relays=["RELAY_A", "RELAY_B"],
            channels=["CHANNEL_1", "CHANNEL_2"],
            connection_paths=[],
            exclusive_connections=[
                ExclusiveConnection(src="INVALID_CHANNEL", dests=["CHANNEL_2"])
            ]
        )


def test_validate_exclusive_connections_with_invalid_destination() -> None:
    with pytest.raises(ValueError, match="Destination channel 'INVALID_CHANNEL' not found in channels."):
        BoardConfig(
            relays=["RELAY_A", "RELAY_B"],
            channels=["CHANNEL_1", "CHANNEL_2"],
            connection_paths=[],
            exclusive_connections=[
                ExclusiveConnection(src="CHANNEL_1", dests=["INVALID_CHANNEL"])
            ]
        )
