# Real-Time System Monitor (RTSM)

A Neofetch-like system information tool with continuous real-time updates. RTSM displays system information, resource usage, and a customizable ASCII art logo in your terminal with live updates.

![RTSM Screenshot](https://example.com/screenshot.png)

## Features

- **Live System Information**: OS, kernel, uptime, hostname, shell, resolution, desktop environment
- **Customizable ASCII Art**: Display built-in or custom ASCII art for your system
- **Real-Time Resource Monitoring**:
  - CPU usage with graphical progress bars
  - Memory usage (RAM and swap)
  - GPU utilization and VRAM (if GPUtil is installed)
- **Live Clock**: Current date and time, updating in real-time
- **User-Friendly Interface**: Easy-to-read layout with color coding
- **Customizable**: Configure displayed elements, colors, and refresh rate
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Requirements

- Python 3.6+
- Required packages:
  - `psutil` - For system information and resource monitoring
- Optional packages:
  - `GPUtil` - For GPU monitoring

## Installation

### Quick Start (No Installation)

Just download the standalone script and run it:

```bash
python rtsm.py
```

### Using pip

```bash
# Install from PyPI
pip install rtsm

# Run the monitor
rtsm
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/rtsm.git
cd rtsm

# Install requirements
pip install -r requirements.txt

# Install the package
pip install -e .

# Run the monitor
rtsm
```

## Usage

```
usage: rtsm [-h] [-r REFRESH] [-a ASCII] [-c CONFIG]

Real-Time System Monitor (RTSM)

options:
  -h, --help            show this help message and exit
  -r REFRESH, --refresh REFRESH
                        Refresh rate in seconds (default: 1.0)
  -a ASCII, --ascii ASCII
                        Path to custom ASCII art file
  -c CONFIG, --config CONFIG
                        Path to configuration file (JSON)
```

### Examples

```bash
# Run with default settings
rtsm

# Update every 0.5 seconds
rtsm --refresh 0.5

# Use custom ASCII art
rtsm --ascii my_logo.txt

# Use custom configuration
rtsm --config my_config.json
```

## Configuration

RTSM can be configured using a JSON configuration file:

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

## Key Controls

While running RTSM, you can use the following keys:

- `q` - Quit the application
- `c` - Toggle system information display