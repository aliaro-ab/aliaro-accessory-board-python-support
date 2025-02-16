"""
This example demonstrates managing relay connections and disconnections
using a simulated board environment.
The code shows how to connect individual channels to a bus, disconnect them,
print the current connections, and finally demonstrate bulk operations
such as connecting or disconnecting multiple channels.
"""

from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Step 1: Create a configuration for the board
# The `BoardConfig` class creates a configuration object based on the device name.
# The identifier for the ALIARO 32-Channel Instrumentation Switch is 'instrumentation_switch'.
board_config = BoardConfig.from_device_name('instrumentation_switch')

# Step 2: Initialize the AccessoryBoard instance
# The `AccessoryBoard` represents the main hardware (or a simulated version in this example).
# We pass:
# - board_config: The configuration generated above.
# - SimulatedBoardController: A mock controller simulating the behavior of a hardware controller.
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Step 2: Connecting specific channels to a bus
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

# Step 3: Disconnecting a specific channel
print("\nDisconnecting channels DUT_CH01 and BUS_POS...")
try:
    # Disconnect channel DUT_CH01 from BUS_POS
    board.disconnect_channels("DUT_CH01", "BUS_POS")

    # Print the updated connections on the board
    board.print_connections()
except Exception as e:
    # Handle any exceptions during disconnection
    print("Error:", e)

print("\nDisconnecting channels DUT_CH02 and BUS_POS...")
try:
    # Disconnect channel DUT_CH02 from BUS_POS
    board.disconnect_channels("DUT_CH02", "BUS_POS")

    # Print the updated state of connections
    board.print_connections()
except Exception as e:
    print("Error:", e)

# Step 4: Connecting multiple channels to a bus
print("\nConnecting all channels...")
try:
    # Connect multiple channels (DUT_CH01, DUT_CH02, DUT_CH03, DUT_CH04) to BUS_POS
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH02", "BUS_POS")
    board.connect_channels("DUT_CH03", "BUS_POS")
    board.connect_channels("DUT_CH04", "BUS_POS")

    # Print the state of connections after all operations
    board.print_connections()
except Exception as e:
    # Handle errors that might occur during connections
    print("Error:", e)

# Step 5: Disconnecting all channels at once
print("Disconnecting all channels...")
try:
    # Disconnect all existing connections on the board
    board.disconnect_all_channels()

    # Print the state of the board after clearing all connections
    board.print_connections()
except Exception as e:
    # Handle errors during the disconnection process
    print("Error:", e)
