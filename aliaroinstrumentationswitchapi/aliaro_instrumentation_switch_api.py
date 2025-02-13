from typing import Tuple

import aliaro_i2c_device_control as i2c


class AliaroInstrumentationSwitchApi:
    """Aliaro Instrumentation Switch API
    ===================================

    Provides class to control an arbitrary amount of modules through I2C over a Serial connection.
    Uses a preset of addresses in class, but can be overwritten by user for customization.
    Implements functions to set relays to either a positive or negative connection rail.
    This allows multiplexing between DUT channels, ground and reading instruments.

    Please see README.md file for use cases & installation.
    """

    _instance = None

    def __init__(
        self,
        active_module: int,
        mux_addresses=None,
        instruments: dict = None,
        com_port: str = "COM5",
        address: int = 8,
    ):
        """
        Opens a Serial session to an I2C module specified by `address`.
        Only requires `active_module` for initialization.
        Intended to be used as a context manager.

        :param active_module: Index of address in mux_addresses
        :param mux_addresses: List of available I2C addresses
        :param instruments: Dictionary of instrument name and index
        :param com_port: Com port to open
        :param address: Start I2C address for connection
        """
        if not hasattr(self, "_initialized"):
            self._client = i2c.AL10xxFIUBoardClient(
                i2c.ALInstSwitch32ChBoard(), com_port, address
            )
            self._initialized = True
        if mux_addresses is None:
            self._mux_addresses = [23, 22, 21, 20]
        self._active_module = active_module
        if instruments is None:
            self._instruments = {
                "bnc_1": 0,
                "bnc_2": 1,
                "bnc_3": 2,
                "bnc_4": 3,
                "bnc_5": 4,
            }

    def __new__(cls, *args, **kwargs):
        """Declares class as Singleton instance.
        :param args:
        :param kwargs:
        """
        if cls._instance is None:
            cls._instance = super(AliaroInstrumentationSwitchApi, cls).__new__(cls)
        return cls._instance

    @property
    def active_module(self):
        return self._mux_addresses.index(self._client.address)

    @active_module.setter
    def active_module(self, mux_id: int):
        self._client.address = self._mux_addresses[mux_id]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.i2c.ser.close()

    def _physical_channel_to_mux_channel(self, current_channel: int) -> Tuple[int, int]:
        """
        Private function to calculate the DUT channel to which physical relay.

        :param current_channel: SLSC Channel being tested
        :return Relay mapping for one channel
        """
        channel_positive = current_channel * 2
        channel_negative = channel_positive + 1

        return channel_positive, channel_negative

    def connect_channel(
        self,
        dut_channel_number: int,
        polarity: bool,
        state: bool,
    ) -> None:
        """
        Sets desired channels on any mux device to a state specified by the user

        :param dut_channel_number: Current SLSC channel
        :param polarity: Which polarity to connect channel to. True=positive, False=negative.
        :param state: Opens or closes relay. True = closed, False = open.
        """
        channel_positive, channel_negative = self._physical_channel_to_mux_channel(
            dut_channel_number
        )
        if polarity:
            self._client.set_relay(channel_positive, state)
        else:
            self._client.set_relay(channel_negative, state)

        self._client.commit_relays()

    def connect_ground(self, polarity: bool, state: bool) -> None:
        """
        Sets Gnd channel on the specified mux board to a desired state.

        :param polarity: Which polarity to connect ground to. True=positive, False=negative.
        :param state: Opens or closes relay. True = closed, False = open.
        """
        if polarity:
            self._client.set_relay(64, state)
        else:
            self._client.set_relay(65, state)
        self._client.commit_relays()

    def connect_instrument(self, instr: str, state: bool) -> None:
        """Sets an instrument of a specified mux to a desired state.

        :param instr: Which instrument to set. Legal values: bnc_1, bnc_2, bnc_3, bnc_4, bnc_5
        :param state: Opens or closes relay. True = closed, False = open.
        """
        base_address = 66
        channel_positive = base_address + (self._instruments[instr] * 2)
        channel_negative = channel_positive + 1
        self._client.set_relay(channel_positive, state)
        self._client.set_relay(channel_negative, state)
        self._client.commit_relays()
