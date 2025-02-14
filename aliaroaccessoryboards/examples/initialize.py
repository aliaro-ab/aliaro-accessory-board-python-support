# Example: Initialization of AccessoryBoard
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

board_config = BoardConfig.from_brd_string(
'''
relays:
- RELAY_CH01
- RELAY_CH02
- RELAY_CH03
- RELAY_CH04

channel_list:
- DUT_CH01
- DUT_CH02
- DUT_CH03
- DUT_CH04
- BUS
connection_list:
- src: DUT_CH01
  dest: BUS
  relays:
  - RELAY_CH01
- src: DUT_CH02
  dest: BUS
  relays:
  - RELAY_CH02
- src: DUT_CH03
  dest: BUS
  relays:
  - RELAY_CH03
- src: DUT_CH04
  dest: BUS
  relays:
  - RELAY_CH04

initial_state:
  open:
  - RELAY_CH01
  - RELAY_CH02
  - RELAY_CH03
  - RELAY_CH04
'''
)

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
print("Board initialized successfully.")

# Load and print board info
print("Relay Names:", board.relays)
print("Channel Names:", board.channels)
