"""
This example showcases how to open a session to an I2CDriverBoardController
and then changing the address.
The code shows how to connect to the board and change the address, whilst printing
active connections on every board after switching.
Please see "connect_disconnect.py" for more detailed instructions regarding board
connectivity.
"""

from aliaroaccessoryboards import AccessoryBoard, BoardConfig, I2CDriverBoardController
import i2cdriver
from time import sleep

# Step 1: Create board configuration and connect to an initial address
# When connecting to an I2CDriverBoardController, an instance of I2CDriver must be instantiated first.
# Please look which COM port your device uses before instantiation.
driver = i2cdriver.I2CDriver("COM5")
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')
board = AccessoryBoard(board_config, I2CDriverBoardController(driver, 23, board_config))

# Step 2: Connect specific channels to a bus
print("\nConnecting channels DUT_CH01 and DUT_CH02 to BUS_POS...")
try:
    # Connect channel DUT_CH01 to BUS_POS
    board.connect_channels("DUT_CH01", "BUS_POS")

    # Connect channel DUT_CH02 to BUS_POS
    board.connect_channels("DUT_CH02", "BUS_POS")

    # Print the current connections on the board
    board.print_connections()
except Exception as e:
    # Handle any exceptions that occur during the connection process
    print("Error:", e)

# Step 3: Change board address
print("\nChanging address of board and printing active connections...")
try:
    # Change address to i.e. 22
    board.change_active_board(22)

    # Print the current connections on the board
    board.print_connections()
except Exception as e:
    # Handle any exceptions that occur during the connection process
    print("Error:", e)

# Step 3: Change back to original address
print("\nChanging address of board to original address and printing active connections...")
try:
    # Change address to 23
    board.change_active_board(23)

    # Print the current connections on the board
    board.print_connections()
except Exception as e:
    # Handle any exceptions that occur during the connection process
    print("Error:", e)
