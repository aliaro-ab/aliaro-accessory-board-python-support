from aliaroaccessoryboards import AccessoryBoard
from aliaroaccessoryboards.boardcontrollers.simulated_board_controller import SimulatedBoardController

def print_connections(connections):
    if len(connections) == 0:
        print("No connections.")
        return
    for connection in connections:
        connection = list(connection)
        print(connection[0], "<->", connection[1])

board = AccessoryBoard("example.top", SimulatedBoardController)

print("Connecting all channels...")
board.connect_channels("DUT_CH01", "BUS_POS")
board.connect_channels("DUT_CH02", "BUS_POS")
board.connect_channels("DUT_CH03", "BUS_POS")
board.connect_channels("DUT_CH04", "BUS_POS")
board.connect_channels("DUT_CH05", "BUS_POS")
board.connect_channels("DUT_CH06", "BUS_POS")
board.connect_channels("DUT_CH07", "BUS_POS")
board.connect_channels("DUT_CH08", "BUS_POS")
print_connections(board.connections)

print("Resetting Board...")
board.reset()
print_connections(board.connections)
