"""
This example demonstrates the initialization, usage, and resetting of an accessory board
using the ALIARO AccessoryBoard library.

After initializing the board, the example demonstrates connecting multiple channels to a
common `BUS_POS` channel, retrieving and displaying the board's connection states, and finally
resetting the board to its initial state.
"""

from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Step 1: Create a configuration for the board
# The `BoardConfig` class creates a configuration object based on the device name.
# The identifier for the ALIARO 32-Channel Instrumentation Switch is '32ch_instrumentation_switch'.
board_config = BoardConfig.from_device_name("32ch_instrumentation_switch")

# Step 2: Initialize the AccessoryBoard instance
# The `AccessoryBoard` represents the main hardware (or a simulated version in this example).
# We pass:
# - board_config: The configuration generated above.
# - SimulatedBoardController: A mock controller simulating the behavior of a hardware controller.
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# STEP 3: Print the initial state of the board connections.
print("\nConnections on Initialization...")
board.print_connections()

# STEP 4: Connect multiple channels to a shared bus (`BUS_POS`).
print("\nConnecting all channels...")
board.connect_channels("DUT_CH01", "BUS_POS")  # First channel connection
board.connect_channels("DUT_CH02", "BUS_POS")  # Second channel connection

# Display the updated connection states after performing the connections.
board.print_connections()

# STEP 5: Reset the board to its initial state.
print("\nResetting Board...")
board.reset()

# Print the state of the board after the reset operation to verify all connections have been cleared.
board.print_connections()
