import aliaro_i2c_device_control as i2c


class MuxClient:

    _instance = None

    def __init__(
        self,
        active_mux: int,
        mux_addresses=None,
        devices: dict = None,
        com_port: str = "COM5",
        address: int = 8,
    ):
        if not hasattr(self, "_initialized"):
            self._client = i2c.AL10xxFIUBoardClient(
                i2c.ALInstSwitch32ChBoard(), com_port, address
            )
            self._initialized = True
        if mux_addresses is None:
            self._mux_addresses = [23, 22, 21, 20]
        self._active_mux = active_mux
        if devices is None:
            self._devices = {"bnc_1": 0, "bnc_2": 1, "bnc_3": 2, "bnc_4": 3, "bnc_5": 4}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MuxClient, cls).__new__(cls)
        return cls._instance

    @property
    def active_mux(self):
        return self._mux_addresses.index(self._client.address)

    @active_mux.setter
    def active_mux(self, mux_id: int):
        self._client.address = self._mux_addresses[mux_id]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.i2c.ser.close()

    def _physical_channel_to_mux_channel(self, current_channel: int):
        """
        Calculates which channel to set on MUX from SLSC channel input.
        :param current_channel: SLSC Channel being tested
        :return Relay mapping for one channel
        """
        channel_positive = current_channel * 2
        channel_negative = channel_positive + 1

        return channel_positive, channel_negative

    def connect_all(self, desired_state: bool):
        """
        Connects all relays.

        :param desired_state: Turns relays on/off.
        :return:
        """
        self._client.set_all_relays(desired_state)
        self._client.commit_relays()

    def connect_channel(
        self,
        dut_channel_number: int,
        pin_mode: bool,
        desired_state: bool,
    ):
        """
        Sets desired channels on any mux device to a state specified by the user
        :param dut_channel_number: Current SLSC channel
        :param pin_mode: Choose positive or negative relay. True=positive, False=negative.
        :param desired_state: Turns channels on or off, True/False
        """
        channel_positive, channel_negative = self._physical_channel_to_mux_channel(
            dut_channel_number
        )
        if pin_mode:
            self._client.set_relay(channel_positive, desired_state)
        else:
            self._client.set_relay(channel_negative, desired_state)

        self._client.commit_relays()

    def connect_ground(self, pin_mode: bool, desired_state: bool):
        """
        Sets Gnd channel on the specified mux board to a desired state.

        :param pin_mode: Choose positive or negative relay. True=positive, False=negative.
        :param desired_state: Turns channel on or off, True/False
        """

        if pin_mode:
            self._client.set_relay(64, desired_state)
        else:
            self._client.set_relay(65, desired_state)
        self._client.commit_relays()

    def connect_device(self, instr: str, desired_state: bool):
        """
        Sets an instrument of a specified mux to a desired state.

        :param instr: Which instrument to set. Legal values: bnc_1, bnc_2, bnc_3, bnc_4, bnc_5
        :param desired_state: Turns instrument on or off, True/False.
        """
        base_address = 66
        channel_positive = base_address + (self._devices[instr] * 2)
        channel_negative = channel_positive + 1
        self._client.set_relay(channel_positive, desired_state)
        self._client.set_relay(channel_negative, desired_state)
        self._client.commit_relays()
