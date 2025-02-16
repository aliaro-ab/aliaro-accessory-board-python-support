from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, ResourceInUseException

# Step 1: Create a configuration for the board
# The `BoardConfig` class creates a configuration object from the provided YAML string.
# This example contrives a setup where RELAY_CONFLICTED is used in two different connection paths.
board_config = BoardConfig.from_brd_string(
    '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    - RELAY_CONFLICTED

    channel_list:
    - DUT_CH01
    - DUT_CH02
    - BUS
    connection_list:
    - src: DUT_CH01
      dest: BUS
      relays:
      - RELAY_CH01
      - RELAY_CONFLICTED
    - src: DUT_CH02
      dest: BUS
      relays:
      - RELAY_CH02
      - RELAY_CONFLICTED
    initial_state:
      open:
      - RELAY_CH01
      - RELAY_CH02
      - RELAY_CONFLICTED
    '''
)

# Step 2: Initialize the AccessoryBoard instance
# The `AccessoryBoard` represents the main hardware (or a simulated version in this example).
# We pass:
# - board_config: The configuration generated above.
# - SimulatedBoardController: A mock controller simulating the behavior of a hardware controller.
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except ResourceInUseException as e:
    print(e)