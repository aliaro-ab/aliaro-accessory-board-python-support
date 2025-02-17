import pytest
from ruamel.yaml import YAMLError

from aliaroaccessoryboards.board_config import BoardConfig
from tests.shared import yaml_config


def test_board_config_from_yaml_success(yaml_config: yaml_config):


    config = BoardConfig.from_brd_string(yaml_config)

    assert isinstance(config, BoardConfig)
    assert config.relays == ["RELAY_CH01", "RELAY_CH02"]
    assert config.channels == ["DUT_CH01", "DUT_CH02", "BUS"]


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
    config = BoardConfig.from_device_name("instrumentation_switch")

    assert isinstance(config, BoardConfig)