from aliaroaccessoryboards import AccessoryBoard, PathUnsupportedException, SourceConflictException, Topology, \
    ResourceInUseException
from aliaroaccessoryboards.boardcontrollers.simulated_board_controller import SimulatedBoardController

topology = Topology.from_top_string(
    '''
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
)
board = AccessoryBoard(topology, SimulatedBoardController)
try:
    board.connect_channels("DUT_CH01", "DEADBEEF")
except ValueError as e:
    print(e)

topology = Topology.from_top_string(
    '''
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
)

board = AccessoryBoard(topology, SimulatedBoardController)
try:
    board.mark_as_source("DUT_CH01")
    board.mark_as_source("DUT_CH02")
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except SourceConflictException as e:
    print(e)

topology = Topology.from_top_string(
    '''
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
)

board = AccessoryBoard(topology, SimulatedBoardController)
try:
    board.connect_channels("DUT_CH01", "DUT_CH02")
except PathUnsupportedException as e:
    print(e)

topology = Topology.from_top_string(
    '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    - RELAY_EXTRA
    
    channel_list:
    - DUT_CH01
    - DUT_CH02
    - BUS
    connection_list:
    - src: DUT_CH01
      dest: BUS
      relays:
      - RELAY_CH01
      - RELAY_EXTRA
    - src: DUT_CH02
      dest: BUS
      relays:
      - RELAY_CH02
      - RELAY_EXTRA
    initial_state:
      open:
      - RELAY_CH01
      - RELAY_CH02
      - RELAY_EXTRA
    '''
)

board = AccessoryBoard(topology, SimulatedBoardController)
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except ResourceInUseException as e:
    print(e)