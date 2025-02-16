import pytest

from aliaroaccessoryboards import BoardConfig
from aliaroaccessoryboards.board_config import Connection, InitialState, MuxItem


@pytest.fixture
def board_config() -> BoardConfig:
    return BoardConfig(
        relays=["AC", "AD", "BC", "BD"],
        channel_list=["A", "B", "C", "D", "X", "Y"],
        connection_list=[
            Connection(src="A", dest="C", relays=["AC"]),
            Connection(src="A", dest="D", relays=["AD"]),
            Connection(src="B", dest="C", relays=["BC"]),
            Connection(src="B", dest="D", relays=["BD"]),
            Connection(src="X", dest="Y", relays=["AC", "BD"]),
        ],
        initial_state=InitialState(),
        mux_list=[
            MuxItem(src="A", dest=["C", "D"]),
            MuxItem(src="B", dest=["C", "D"]),
        ],
        current_sensors=["Sensor1", "Sensor2"]
    )


@pytest.fixture
def yaml_config() -> str:
    return '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    
    channel_list:
    - DUT_CH01
    - DUT_CH02
    - BUS
    connection_list:
    - src: DUT_CH01
      dest: BUS
      relays:
      - RELAY_CH01
    - src: DUT_CH02
      dest: BUS
      relays:
      - RELAY_CH02
    
    initial_state:
      open:
      - RELAY_CH01
      - RELAY_CH02
    '''
