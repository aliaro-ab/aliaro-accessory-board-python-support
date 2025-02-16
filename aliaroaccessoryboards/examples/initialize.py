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
board_config = BoardConfig.from_device_name('instrumentation_switch')


if SIMULATED:
    from aliaroaccessoryboards import SimulatedBoardController

    board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
else:
    from i2cdriver import I2CDriver
    from aliaroaccessoryboards import I2CDriverBoardController

    i2c = I2CDriver("COM5", reset=False)
    board = AccessoryBoard(board_config, I2CDriverBoardController(i2c, 22, board_config))

print("Board initialized successfully.")

# Load and print board information
print("Relay Names:", board.relays)
print("Channel Names:", board.channels)
