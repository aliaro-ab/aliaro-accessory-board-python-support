"""
This example demonstrates how to initialize an AccessoryBoard with a predefined configuration
and interact with its relays and channels.

The `board_config` defines the relay and channel mappings, as well as their initial states.
It is presented here as an inline string for demonstration purposes but is typically loaded from a `.brd` file.

If `SIMULATED` is set to `False`, the system initializes the board with the `I2CDriverBoardController`,
connecting via an actual I2C controller.
"""
from aliaroaccessoryboards import AccessoryBoard, BoardConfig

SIMULATED = True  # Comment this line out to run the example with the I2CDriver

board_config = BoardConfig.from_brd_string(
    '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    - RELAY_CH03
    - RELAY_CH04
    
    channel_list:
    - DUT_CH01
    - DUT_CH02
    - DUT_CH03
    - DUT_CH04
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
    - src: DUT_CH03
      dest: BUS
      relays:
      - RELAY_CH03
    - src: DUT_CH04
      dest: BUS
      relays:
      - RELAY_CH04
    
    initial_state:
      open:
      - RELAY_CH01
      - RELAY_CH02
      - RELAY_CH03
      - RELAY_CH04
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

print("Board initialized successfully.")

# Load and print board info
print("Relay Names:", board.relays)
print("Channel Names:", board.channels)
