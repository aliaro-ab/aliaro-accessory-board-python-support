import pytest

from aliaroaccessoryboards.board_config import BoardConfig, ConnectionPath, InitializationCommands, ExclusiveConnection


@pytest.fixture
def board_config() -> BoardConfig:
    return BoardConfig(
        relays=["AC", "AD", "BC", "BD"],
        channels=["A", "B", "C", "D", "X", "Y"],
        connection_paths=[
            ConnectionPath(src="A", dest="C", relays=["AC"]),
            ConnectionPath(src="A", dest="D", relays=["AD"]),
            ConnectionPath(src="B", dest="C", relays=["BC"]),
            ConnectionPath(src="B", dest="D", relays=["BD"]),
            ConnectionPath(src="X", dest="Y", relays=["AC", "BD"]),
        ],
        initialization_commands=InitializationCommands(),
        exclusive_connections=[
            ExclusiveConnection(src="A", dests=["C", "D"]),
            ExclusiveConnection(src="B", dests=["C", "D"]),
        ],
        current_sensors=["Sensor1", "Sensor2"]
    )


@pytest.fixture
def yaml_config() -> str:
    return '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    
    channels:
    - DUT_CH01
    - DUT_CH02
    - BUS
    connection_paths:
    - src: DUT_CH01
      dest: BUS
      relays:
      - RELAY_CH01
    - src: DUT_CH02
      dest: BUS
      relays:
      - RELAY_CH02
    
    initialization_commands:
      relays_to_open:
      - RELAY_CH01
      - RELAY_CH02
    '''
