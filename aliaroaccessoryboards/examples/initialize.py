"""
This example demonstrates how to initialize an AccessoryBoard with a given configuration.
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

# At this point, the board has been initialized.
# Configuration information and the simulated controller ensure that the board is ready for use,
# even without actual hardware.

# Confirmation message to signal successful initialization
print("Board initialized successfully.")

# Step 3: Access and print details about the board
print(
    "Relay Names:", board.relays
)  # Output the relay names from the board configuration
print(
    "Channel Names:", board.channels
)  # Output the channel names from the board configuration
