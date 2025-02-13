# Example: Initialization of AccessoryBoard
from aliaroaccessoryboards import AccessoryBoard
from aliaroaccessoryboards.boardcontrollers.simulated_board_controller import SimulatedBoardController


board = AccessoryBoard("example.top", SimulatedBoardController)
print("Board initialized successfully.")

# Load and print board info
print("Relay Names:", board.relays)
print("Channel Names:", board.channels)
