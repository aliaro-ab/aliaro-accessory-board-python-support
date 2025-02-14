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
print(board_config)

def print_connections(connections):
    if len(connections) == 0:
        print("No connections.")
        return
    for connection in connections:
        connection = list(connection)
        print(connection[0], "<->", connection[1])

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
print("\nConnecting channels DUT_CH01 and DUT_CH02 to BUS...")
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
    print_connections(board.connections)
except Exception as e:
    print("Error:", e)

print("\nDisconnecting channels DUT_CH01 and BUS...")
try:
    board.disconnect_channels("DUT_CH01", "BUS")
    print_connections(board.connections)
except Exception as e:
    print("Error:", e)

print("\nDisconnecting channels DUT_CH02 and BUS...")
try:
    board.disconnect_channels("DUT_CH02", "BUS")
    print_connections(board.connections)
except Exception as e:
    print("Error:", e)

print("\nConnecting all channels...")
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
    board.connect_channels("DUT_CH03", "BUS")
    board.connect_channels("DUT_CH04", "BUS")
    print_connections(board.connections)
except Exception as e:
    print("Error:", e)

print("Disconnecting all channels...")
try:
    board.disconnect_all_channels()
    print_connections(board.connections)
except Exception as e:
    print("Error:", e)