from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, ResourceInUseException
from aliaroaccessoryboards.accessory_board import MuxConflictException

board_config = BoardConfig.from_device_name('instrumentation_switch')

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH01", "BUS_NEG")
except MuxConflictException as e:
    print(e)
