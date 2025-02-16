from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, MuxConflictException

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

try:
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH01", "BUS_NEG")
except MuxConflictException as e:
    print(e)
