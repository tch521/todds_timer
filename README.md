# Todd's Timer

[![PyPI version](https://badge.fury.io/py/todds_timer.svg)](https://badge.fury.io/py/todds_timer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A versatile and easy-to-use Python timer utility for measuring code execution time and analyzing performance.

## Features

- Use as a decorator or context manager
- Nested timing support with proper indentation
- Detailed logging of start and end times
- Statistical analysis of execution times across multiple runs
- Customizable task names with support for dynamic formatting
- Lightweight and easy to integrate into existing projects

## Installation

Install Todd's Timer using pip:

```bash
pip install todds_timer
```

## Usage

At the top of your python file, import the Timer class and configure logging.
Standard timing messages are logged at the DEBUG level, however the summary table
produced by `print_average_times()` is at the INFO level.

```python
from todds_timer import Timer
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
```

### As a Context Manager

```python
with Timer("Calculating sum"):
    result = sum([1,2,3,4])
```
Output:
```
DEBUG ----STARTED Calculating sum
DEBUG ----COMPLETED (in 0.000 seconds) Calculating sum
```

### As a Decorator

```python
@Timer("Calculate sum of {0} and {1}")
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 7)
```
Output:
```
DEBUG ----STARTED Calculate sum of 5 and 7
DEBUG ----COMPLETED (in 0.000 seconds) Calculate sum of 5 and 7
```

### Nested Timers

```python
with Timer("Outer operation"):
    # Some code here
    with Timer("Inner operation"):
        # More code here
        pass
```
Output:
```
DEBUG ----STARTED Outer operation
DEBUG --------STARTED Inner operation
DEBUG --------COMPLETED (in 0.000 seconds) Inner operation
DEBUG ----COMPLETED (in 0.000 seconds) Outer operation
```

### Analyzing Timing Results

```python
# After running some timed operations
Timer.print_average_times(sort="name")
```
Output:
```
INFO Average | Minimum | Maximum | Count | Task name
INFO   0.000 |   0.000 |   0.000 |     1 | Calculate sum of 5 and 7
INFO   0.000 |   0.000 |   0.000 |     1 | Calculating sum
INFO   0.000 |   0.000 |   0.000 |     1 | Inner operation
INFO   0.000 |   0.000 |   0.000 |     1 | Outer operation
```

## Configuration

Todd's Timer uses Python's built-in `logging` module. To see the timing output, ensure that your logging is configured to show DEBUG level messages:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
