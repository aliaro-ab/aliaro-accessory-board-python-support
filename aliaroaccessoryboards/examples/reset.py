"""
This example demonstrates the initialization, usage, and resetting of an accessory board 
using the ALIARO AccessoryBoard library. 

After initializing the board, the example demonstrates connecting multiple channels to a
common `BUS_POS` channel, retrieving and displaying the board's connection states, and finally
resetting the board to its initial state.

The `board_config` defines the relay and channel mappings, as well as their initial states.
It is presented here as an inline string for demonstration purposes but is typically loaded from a `.brd` file.

If `SIMULATED` is set to `False`, the system initializes the board with the `I2CDriverBoardController`,
connecting via an actual I2C controller.
"""

from aliaroaccessoryboards import AccessoryBoard, BoardConfig

SIMULATED = True  # Comment this line out to run the example with the I2CDriver
board_config = BoardConfig.from_device_name('instrumentation_switch')

if SIMULATED:
    from aliaroaccessoryboards import SimulatedBoardController

    board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
else:
    from i2cdriver import I2CDriver
    from aliaroaccessoryboards import I2CDriverBoardController

    i2c = I2CDriver("COM5", reset=False)
    board = AccessoryBoard(board_config, I2CDriverBoardController(i2c, 22, board_config))
print("\nConnections on Initialization...")
board.print_connections()

print("\nConnecting all channels...")
board.connect_channels("DUT_CH01", "BUS_POS")
board.connect_channels("DUT_CH02", "BUS_POS")
board.print_connections()

print("\nResetting Board...")
board.reset()
board.print_connections()
