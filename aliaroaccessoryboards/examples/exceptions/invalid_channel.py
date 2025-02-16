from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController

board_config = BoardConfig.from_device_name('instrumentation_switch')

board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

try:
    board.connect_channels("DUT_CH01", "DEADBEEF")
except KeyError as e:
    print(e)
