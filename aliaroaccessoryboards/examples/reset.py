from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

def print_connections(connections):
    if len(connections) == 0:
        print("No connections.")
        return
    for connection in connections:
        connection = list(connection)
        print(connection[0], "<->", connection[1])

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

  close:
  - RELAY_CH03
  - RELAY_CH04
'''
)

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

print("\nConnections on Initialization...")
print_connections(board.connections)

print("\nConnecting all channels...")
board.connect_channels("DUT_CH01", "BUS")
board.connect_channels("DUT_CH02", "BUS")
# board.connect_channels("DUT_CH03", "BUS")
# board.connect_channels("DUT_CH04", "BUS")
print_connections(board.connections)

print("\nResetting Board...")
board.reset()
print_connections(board.connections)
