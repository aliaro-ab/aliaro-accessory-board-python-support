"""
This example demonstrates how error handling works for the Accessory Board relays.

`SourceConflictException`: Raised when attempting to set multiple channels as sources 
that conflict with one another.

`PathUnsupportedException`: Raised when trying to connect two channels without a defined 
or supported path between them.

`ResourceInUseException`: Raised when a relay or other resource is already in use 
and cannot be used for the requested operation.

`MuxConflictException`: Raised when attempting to connect two channels that are part of
the same mux.

The `board_config` defines the relay and channel mappings, as well as their initial states.
It is presented here as an inline string for demonstration purposes but is typically loaded from a `.brd` file.

If `SIMULATED` is set to `False`, the system initializes the board with the `I2CDriverBoardController`,
connecting via an actual I2C controller.
"""
from aliaroaccessoryboards import AccessoryBoard, PathUnsupportedException, SourceConflictException, BoardConfig, \
    ResourceInUseException
from aliaroaccessoryboards.accessory_board import MuxConflictException

SIMULATED = True  # Comment this line out to run the example with the I2CDriver

board_config = BoardConfig.from_brd_string(
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
if SIMULATED:
    from aliaroaccessoryboards import SimulatedBoardController

    board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
else:
    from i2cdriver import I2CDriver
    from aliaroaccessoryboards import I2CDriverBoardController

    i2c = I2CDriver("COM5", reset=False)
    board = AccessoryBoard(board_config, I2CDriverBoardController(i2c, 22, board_config))

try:
    board.connect_channels("DUT_CH01", "DEADBEEF")
except ValueError as e:
    print(e)

board_config = BoardConfig.from_brd_string(
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

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.mark_as_source("DUT_CH01")
    board.mark_as_source("DUT_CH02")
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except SourceConflictException as e:
    print(e)

board_config = BoardConfig.from_brd_string(
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

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "DUT_CH02")
except PathUnsupportedException as e:
    print(e)

board_config = BoardConfig.from_brd_string(
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

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except ResourceInUseException as e:
    print(e)

board_config = BoardConfig.from_brd_string(
    '''
    relays:
    - RELAY_BUSA
    - RELAY_BUSB

    channel_list:
    - DUT
    - BUSA
    - BUSB
    connection_list:
    - src: DUT
      dest: BUSA
      relays:
      - RELAY_BUSA
    - src: DUT
      dest: BUSB
      relays:
      - RELAY_BUSB

    initial_state:
      open:
      - RELAY_BUSA
      - RELAY_BUSB
    mux_list:
      - src: DUT
        dest:
        - BUSA
        - BUSB  
    '''
)

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT", "BUSA")
    board.connect_channels("DUT", "BUSB")
except MuxConflictException as e:
    print(e)
