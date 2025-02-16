"""
This example demonstrates managing relay connections, disconnections.

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

print("\nConnecting channels DUT_CH01 and DUT_CH02 to BUS_POS...")
try:
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH02", "BUS_POS")
    board.print_connections()
except Exception as e:
    print("Error:", e)

print("\nDisconnecting channels DUT_CH01 and BUS_POS...")
try:
    board.disconnect_channels("DUT_CH01", "BUS_POS")
    board.print_connections()
except Exception as e:
    print("Error:", e)

print("\nDisconnecting channels DUT_CH02 and BUS_POS...")
try:
    board.disconnect_channels("DUT_CH02", "BUS_POS")
    board.print_connections()
except Exception as e:
    print("Error:", e)

print("\nConnecting all channels...")
try:
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH02", "BUS_POS")
    board.connect_channels("DUT_CH03", "BUS_POS")
    board.connect_channels("DUT_CH04", "BUS_POS")
    board.print_connections()
except Exception as e:
    print("Error:", e)

print("Disconnecting all channels...")
try:
    board.disconnect_all_channels()
    board.print_connections()
except Exception as e:
    print("Error:", e)
