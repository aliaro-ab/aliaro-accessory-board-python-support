from time import sleep
from typing import List

from i2cdriver import I2CDriver

from aliaroaccessoryboards.boardcontrollers.board_controller import BoardController


class I2CDriverBoardController(BoardController):
    READ_CURRENT = 0
    READ_RELAYS = 128
    WRITE_RELAYS = 160

    def __init__(self, i2c_driver: I2CDriver, device_address: int, relay_count: int, current_count: int):
        super().__init__(relay_count, current_count)
        self._device_address = device_address
        self._i2c_driver = i2c_driver

    def read_relays_from_device(self) -> int:
        return self._i2c_driver.regrd(self._device_address, self.READ_RELAYS, "<H")

    def write_relays_to_device(self, relay_mask: int):
        self._i2c_driver.regwr(
            self._device_address,
            self.WRITE_RELAYS,
            relay_mask.to_bytes(self._relay_buffer_size, byteorder="little"),
        )
        sleep(0.04)

    def read_currents_from_device(self) -> List[int]:
        return self._i2c_driver.regrd(
            self._device_address, self.READ_CURRENT, f"{self.current_count}h"
        )
