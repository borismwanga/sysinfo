# Real-Time System Monitor (RTSM)

A Neofetch-like system monitoring tool with live updates in the terminal.

## Overview

RTSM provides a colorful, interactive dashboard in your terminal that displays system information and real-time resource usage. The monitor updates continuously, showing CPU usage, memory consumption, and GPU statistics (if available).

## Features

- Real-time system monitoring with configurable refresh rate
- Attractive ASCII art based on your operating system
- Detailed system information display
- Live resource usage statistics with visual progress bars
- Optional GPU monitoring
- Customizable appearance and display options
- Square terminal sizing option

## Requirements

- Python 3.6+
- psutil (for system monitoring)
- GPUtil (optional, for GPU monitoring)
- A terminal that supports colors

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rtsm.git
   cd rtsm
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the monitor with:

```
python main.py
```

### Command Line Options

- `-r`, `--refresh`: Set the refresh rate in seconds (default: 1.0)
  ```
  python main.py --refresh 2.0
  ```

- `-a`, `--ascii`: Specify a custom ASCII art file
  ```
  python main.py --ascii /path/to/my-ascii-art.txt
  ```

- `-c`, `--config`: Specify a custom configuration file (JSON format)
  ```
  python main.py --config /path/to/my-config.json
  ```

- `-s`, `--square`: Set terminal to square size (e.g., 80x80 characters)
  ```
  python main.py --square 80
  ```

## Controls

- `q`: Quit the application
- `c`: Toggle system information display

## Configuration

You can customize the monitor by creating a JSON configuration file. Example:

```json
{
  "show_system_info": true,
  "show_ascii": true,
  "show_resources": true,
  "show_clock": true,
  "colors": {
    "title": 6,
    "label": 2,
    "value": 7,
    "ascii": 3,
    "bar_filled": 2,
    "bar_empty": 7
  }
}
```

## Project Structure

```
rtsm/
│
├── __init__.py            # Package initialization
├── main.py                # Main entry point
├── monitor.py             # Core monitoring class
├── utils.py               # Utility functions
├── ascii_art.py           # ASCII art and related functions
├── system_info.py         # System information gathering
├── resource_usage.py      # Resource usage monitoring
└── requirements.txt       # Dependencies
```

## Customizing ASCII Art

You can create your own ASCII art file and use it with the `-a` option. The file should contain ASCII art that fits well in your terminal.

## GPU Monitoring

GPU monitoring requires the GPUtil package:

```
pip install GPUtil
```

Note that GPU monitoring is currently only available for NVIDIA GPUs.

## Known Issues

- Terminal resizing may not work on all systems or terminal emulators
- Some virtual environments may not display colors correctly
- GPU monitoring is limited to NVIDIA GPUs via GPUtil

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Neofetch and other system information tools
- Thanks to the psutil and GPUtil projects for making system monitoring easier