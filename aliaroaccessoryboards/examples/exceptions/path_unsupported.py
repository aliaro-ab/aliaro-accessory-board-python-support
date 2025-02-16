from aliaroaccessoryboards import PathUnsupportedException, AccessoryBoard, BoardConfig, SimulatedBoardController

board_config = BoardConfig.from_device_name('instrumentation_switch')
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "DUT_CH02")
except PathUnsupportedException as e:
    print(e)
