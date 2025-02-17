"""
This example demonstrates how to use the `aliaroaccessoryboards` library to control an ALIARO 32-Channel
Instrumentation Switch to manage connections to one or more external instruments.

This diagram shows a simple representation of how the board functions.
┌───────────────┐     ┌─────────────┐     ┌───────────────┐
│      BUS+     ├──/──┤ DUT CH01-32 ├──/──┤      BUS-     │
└──────┬────────┘     └─────────────┘     └────────┬──────┘
       │                                           │
       │              ┌─────────────┐              │
       ├───────/──────┤   DUT_GND   ├───────/──────┤
       │              └─────────────┘              │
       │                                           │
       │              ┌─────────────┐              │              ┌─────────────┐
       ├───────/──────┤ J4-7 CENTER │              ├───────/──────┤ J4-7 SHIELD │
       │              └─────────────┘              │              └─────────────┘
       │                                           │
       │              ┌─────────────┐              │              ┌─────────────┐
       └───────/──────┤      J8     │              └───────/──────┤      J9     │
                      └─────────────┘                             └─────────────┘
"""

from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, SourceConflictException

# Constants for system connections
FGEN_POS = "J4_CENTER"
FGEN_NEG = "J4_SHIELD"

SCOPE_POS = "J5_CENTER"
SCOPE_NEG = "J5_SHIELD"

INPUT = "DUT_CH01"
OUTPUT = "DUT_CH02"

# Step 1: Create a configuration for the board
# The `BoardConfig` class creates a configuration object based on the device name.
# The identifier for the ALIARO 32-Channel Instrumentation Switch is '32ch_instrumentation_switch'.
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Step 2: Initialize the AccessoryBoard instance
# The `AccessoryBoard` represents the main hardware (or a simulated version in this example).
# We pass:
# - board_config: The configuration generated above.
# - SimulatedBoardController: A mock controller simulating the behavior of a hardware controller.
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Step 3: Mark any source channels so that the driver prevents them from being connected to other sources accidentally.
board.mark_as_source(FGEN_POS)  # Function Generator is an output
board.mark_as_source(FGEN_NEG)  # Function Generator is an output
board.mark_as_source(OUTPUT)

# At this point, calling `board.connect_channels(FGEN_POS, BUS_POS)` and then calling
# `board.channels.connect_channels(DUT_CH01, BUS_POS)` or any other channels marked as a source will raise a
# 'SourceConflictException' and prevent the user from connecting two sources to BUS_POS at the same time.

# Step 4: Connect Instrumentation to the desired channels on the device under test.

# Set up GND connections with DUT and all the instruments using BUS_NEG
board.connect_channels("DUT_GND", "BUS_NEG")
board.connect_channels(FGEN_NEG, "BUS_NEG")
board.connect_channels(SCOPE_NEG, "BUS_NEG")

# Monitor the pin state with an oscilloscope
board.connect_channels(SCOPE_POS, "BUS_POS")

# Use the FGEN as the source
board.connect_channels(INPUT, "BUS_POS")
board.connect_channels(FGEN_POS, "BUS_POS")

# Switch to using the OUTPUT channel as the source
board.disconnect_channels(FGEN_POS, "BUS_POS")
board.connect_channels(OUTPUT, "BUS_POS")

# Reset the board back to the default state
board.reset()