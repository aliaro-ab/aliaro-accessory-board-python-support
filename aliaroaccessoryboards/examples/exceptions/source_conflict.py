from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, SourceConflictException

board_config = BoardConfig.from_device_name('instrumentation_switch')

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.mark_as_source("DUT_CH01")
    board.mark_as_source("DUT_CH02")
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH02", "BUS_POS")
except SourceConflictException as e:
    print(e)
