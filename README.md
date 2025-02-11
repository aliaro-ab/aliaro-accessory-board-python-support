
# MuxClient

This Python module provides a `MuxClient` class to control the AL-RD004 module. The `MuxClient` class is designed to be used as a context manager.
## Installation

The first prerequisite is having Python installed, if it is not installed in your local environment,\
please visit the [python installer page](https://www.python.org/downloads/).

Then, follow these steps to get started:

- Install Poetry by running `curl -ssl https://install.python-poetry.org | py -`.
- Navigate to the project directory
- Install project dependencies using Poetry by running the following in command line: `poetry install`.

## Usage
Only the variable `active_mux` is required for instantiating `MuxClient`.

However, the standard variables used will be the following:

`i2c` addresses on bus: `[23, 22, 21, 20]`\
com port used: `COM5`\
devices: `{"bnc_1": 0, "bnc_2": 1, "bnc_3": 2, "bnc_4": 3, "bnc_5": 4}`

If desired, these variables can be changed by either passing the variables into the constructor,
or by changing the default values in the `MuxClient` class.

Furthermore, whilst a session to one board is expected to be open at a time due to
a Singleton pattern implementation, the current address can be changed within the context 
manager. 

### Example
If only wanting to set `active_mux` as a parameter:

`with MuxClient(active_mux=0) as mux:`\
    `mux.connect_channel(dut_channel_number=1, pin_mode=True, desired_state=True)`\
    `mux.connect_ground(pin_mode=False, desired_state=True)`\
    `mux.connect_device(instr="bnc_1", desired_state=True)`\

If wanting to change default parameters from the caller:

`mux_addresses` = [8, 9, 10, 11]\
`devices` = {"instrument_1": 0, "instrument_2": 1, "instrument_3": 2, "instrument_4": 3, "DMM": 4}\
`com_port` = "COM3"\
`address` = 8\
`with MuxClient(active_mux=0, mux_addresses, devices, com_port, address) as mux:`\
    `mux.connect_channel(dut_channel_number=1, pin_mode=True, desired_state=True)`\
    `mux.connect_ground(pin_mode=False, desired_state=True)`\
    `mux.connect_device(instr="bnc_1", desired_state=True)`\

Changing the address within the context manager:

`with MuxClient(active_mux=0) as mux:`\
    `mux.active_mux` = 3

Where `active_mux` is the index of the mux in the supplied addresses.

### Explanation

- channel_number: Channel number (0 index) to be set by user.
- pin_mode: positive or negative relay of channel to be set.
Each positive/negative relay are connected to a corresponding rail, allowing one connection 
to be active at a time per rail.
- desired_state: Turns relay on/off.
