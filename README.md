# ALIARO Accessory Board Python API

## Overview

The ALIARO Accessory Board Python API simplifies the connection management of systems using ALIARO Accessory Boards.

---

## Prerequisites

- **Python Version:** Python 3.9+.

---

## Installation

To install the latest version directly from the GitHub repository, follow these instructions:

### Using `pip`:

```bash
pip install git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git
```

Replace `<username>` and `<repository>` with the appropriate GitHub username and repository name.

For a specific branch, include `@branch_name`:

```bash
pip install git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git@branch_name
```

For a specific commit, include `@commit_hash`:

```bash
pip install git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git@<commit_hash>
```

---

### Using `poetry`:

To add the repository as a dependency in a `poetry`-based project, use the following:

```bash
poetry add git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git
```

For a specific branch:

```bash
poetry add git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git#branch_name
```

For a specific commit:

```bash
poetry add git+https://github.com/aliaro-ab/aliaro-accessory-board-python-support.git#<commit_hash>
```

---

## Getting Started

### Basic Workflow

The typical workflow for using this API includes:

1. **Initialize the board:** Load the provided configuration file for the device.
2. **Perform operations:** Connect/disconnect channels, reset the board, and query its state.

---

## API Usage

### Example 1: Initializing the Board

This example demonstrates how to initialize the board in **simulated mode**.

Replace `SimulatedBoardController` with `I2CDriverBoardController` to interact with real hardware.

```python
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Step 1: Create a board configuration
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Step 2: Initialize the board with a simulated controller
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
```

### Example 2: Managing Connections

This example demonstrates how to connect and disconnect channels programmatically while managing the state of
connections.

```python
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Create a configuration for the board
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Initialize the AccessoryBoard instance
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Connect specific channels
board.connect_channels("DUT_CH01", "BUS_POS")
board.connect_channels("DUT_CH02", "BUS_POS")

# Disconnect specific channels
board.disconnect_channels("DUT_CH01", "BUS_POS")
board.disconnect_channels("DUT_CH02", "BUS_POS")
board.print_connections()  # Print updated connections

# Disconnect all channels
board.disconnect_all_channels()
```
### Example 3: Switching from Simulated to I2C-Controller

This example is similar to Example 2, 
but demonstrates using the `I2CDriverBoardController` instead of the `SimulatedBoardController`.

```python
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, I2CDriverBoardController
import i2cdriver

# Create a configuration for the board
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Initialize i2cdriver instance to connected USB port
driver = i2cdriver.I2CDriver("COM5")

# Pick a starting address for your I2C bus to target
target_i2c_address = 8

# Initialize the AccessoryBoard instance 
board = AccessoryBoard(board_config, I2CDriverBoardController(driver, target_i2c_address, board_config))

# Connect specific channels
board.connect_channels("DUT_CH01", "BUS_POS")
board.connect_channels("DUT_CH02", "BUS_POS")

# Print updated connections
board.print_connections()

# Disconnect specific channels
board.disconnect_channels("DUT_CH01", "BUS_POS")
board.disconnect_channels("DUT_CH02", "BUS_POS")

# Disconnect all channels
board.disconnect_all_channels()

```

### Example 4: Resetting the Board

Resetting the board reverts it to its initial configuration, ensuring a clean state for further operations.

```python
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Create the board configuration using the device name
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Initialize the board in simulated mode
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Reset the board to its initial state
board.reset()

# Notify the reset action is complete
print("Board reset successfully.")
```

### Example 5: Error Handling

Handle errors gracefully using `try`/`except` blocks to debug issues during board operations.

#### Invalid Channel Name

When any invalid channel name is encountered in any of the `AccessoryBoard` functions, a `KeyError` is raised with
information on what name was not valid.

For example, the code below prints the message:

``` text
'Invalid channel names provided: DEADBEEF'
```

```python
from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController

board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

try:
    board.connect_channels("DUT_CH01", "DEADBEEF")  # Invalid channel
except KeyError as e:
    print(f"Invalid channel: {e}")

```

#### Exclusive Connection Conflict

When a channel is connected to multiple channels as defined by the `exclusive_connections` list in the board 
configuration, a `ExclusiveConnectionConflictException` is raised with information on the conflict.

For example, the code below prints the message:

```text
Connection is mutually exclusive with an existing connection: Requested: BUS_NEG <--> DUT_CH01, Conflicting connection: BUS_POS```

```python
from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController,
    ExclusiveConnectionConflictException

board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

try:
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH01", "BUS_NEG")  # Conflict occurs
except ExclusiveConnectionConflictException as e:
    print(f"Multiplexer conflict: {e}")
```

#### Unsupported Path

When a path cannot be found between two otherwise connectable channels,
a `PathUnsupportedException` is raised with details about the channels involved.

For example, the code below prints the message:

```text
No supported path exists between channels: Requested: DUT_CH01 <--> DUT_CH02
```

```python
from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, PathUnsupportedException

board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

try:
    board.connect_channels("DUT_CH01", "DUT_CH02")  # Unsupported path
except PathUnsupportedException as e:
    print(f"Unsupported path: {e}")
```

#### Resource In Use

When a resource (e.g., a relay) is already in use by a connection and another operation attempts to use it
simultaneously, a `ResourceInUseException` is raised with details about the conflict. 

This ensures that hardware resources are not shared incorrectly. 

For example, the code below prints the message:

```text
Relay in use by another connection: Requested: RELAY_CONFLICTED
```

```python
from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, ResourceInUseException

# Create the board configuration with a conflicting relay setup
board_config = BoardConfig.from_brd_string(
    '''
    relays:
    - RELAY_CH01
    - RELAY_CH02
    - RELAY_CONFLICTED

    channel_list:
    - DUT_CH01
    - DUT_CH02
    - BUS
    connection_list:
    - src: DUT_CH01
      dest: BUS
      relays:
      - RELAY_CH01
      - RELAY_CONFLICTED
    - src: DUT_CH02
      dest: BUS
      relays:
      - RELAY_CH02
      - RELAY_CONFLICTED
    initial_state:
      open:
      - RELAY_CH01
      - RELAY_CH02
      - RELAY_CONFLICTED
    '''
)

# Initialize a simulated board and trigger a conflict
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))
try:
    board.connect_channels("DUT_CH01", "BUS")
    board.connect_channels("DUT_CH02", "BUS")
except ResourceInUseException as e:
    print(e)
```

#### Source Conflict

A `SourceConflictException` is raised when multiple connections attempt to use the same source channel simultaneously,
which is not allowed. 

This ensures that a source channel can be linked to only one destination at a time. 

For example, the code below prints the message:

```pycon
Connection would connect multiple sources: Requested: BUS_POS <--> DUT_CH02, Conflicting Sources: DUT_CH01
```

```python
from aliaroaccessoryboards import BoardConfig, AccessoryBoard, SimulatedBoardController, SourceConflictException

board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

try:
    board.mark_as_source("DUT_CH01")
    board.mark_as_source("DUT_CH02")
    board.connect_channels("DUT_CH01", "BUS_POS")
    board.connect_channels("DUT_CH02", "BUS_POS")
except SourceConflictException as e:
    print(e)
```

## 32 Channel Instrumentation Switch Examples

### Example 1: Connect DUT to Instrument
 
Both the positive and negative bus must be used to connect DUT to an Instrument slot.
Below is an example connection for channel `DUT_CH01`, which can be accomplished with the following code snippet.

```text
DUT_CH01 <--> BUS_POS <--> J4_CENTER
DUT_GND <--> BUS_NEG <--> J4_SHIELD
```

```python
from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Create a configuration for the board
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Initialize the AccessoryBoard instance
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Connect DUT channel to positive bus
board.connect_channels("DUT_CH01", "BUS_POS")

# Connect positive instrument channel to positive bus
board.connect_channels("J4_CENTER", "BUS_POS")

# Connect DUT channel to negative bus
board.connect_channels("DUT_GND", "BUS_NEG")

# Connect negative instrument channel to negative bus
board.connect_channels("J4_SHIELD", "BUS_NEG")

# Print updated connections
board.print_connections()

# Disconnect channels
board.reset()
```

### Example 2: Connect DUT to Banana Plugs

This works the same way as Example 1 but uses different channel names corresponding to the banana plugs on the device.
The code below prints the following upon completion:

```text
BUS_NEG <--> DUT_GND
BUS_NEG <--> J9
BUS_POS <--> DUT_CH01
BUS_POS <--> J8
```

```python

from aliaroaccessoryboards import AccessoryBoard, BoardConfig, SimulatedBoardController

# Create a configuration for the board
board_config = BoardConfig.from_device_name('32ch_instrumentation_switch')

# Initialize the AccessoryBoard instance
board = AccessoryBoard(board_config, SimulatedBoardController(board_config))

# Connect DUT channels to positive bus
board.connect_channels("DUT_CH01", "BUS_POS")

#Connect red banana plug to positive bus
board.connect_channels("J8", "BUS_POS")

# Connect DUT channels to negative bus
board.connect_channels("DUT_GND", "BUS_NEG")

# Connect black banana plug to negative bus
board.connect_channels("J9", "BUS_NEG")

# Print updated connections
board.print_connections()

# Disconnect channels
board.reset()

```
