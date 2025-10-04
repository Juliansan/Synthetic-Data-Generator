# Synthetic Data Generator

A powerful CLI tool for generating realistic synthetic data using YAML configuration files. Built with Python, Click, and Rich for a modern, user-friendly experience.

## Features

- 🎯 **CLI-First Design**: Simple, intuitive command-line interface for all operations.
- 📝 **YAML Configuration**: Declarative config files make it easy to define complex data structures.
- 🎨 **Beautiful Output**: Rich terminal formatting with colors, tables, and progress bars.
- 🔍 **Null Value Support**: Configure null rates per column to simulate real-world data imperfections.
- 📊 **Multiple Generators**: Specialized generators for environmental sensors, business data, and user profiles.
- ✅ **Validation**: Built-in config validation to catch errors before you generate data.

## Quick Start

### 1. Installation

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .\.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Usage

```bash
# List all available data generation configs
python cli.py list-configs

# Generate data from a config file and show statistics
python cli.py generate config/environmental_sensor.yaml --stats

# Preview the first 10 rows without saving the file
python cli.py generate config/business_customers.yaml --preview 10

# Validate a configuration file's syntax
python cli.py validate config/environmental_sensor.yaml
```

## Configuration

Data generation is controlled by YAML files in the `config/` directory.

### YAML Structure

```yaml
# The type of generator to use
generator_type: environmental_sensor

# Output file path and format (csv or excel)
output_file: data/sensor_readings.csv
format: csv
num_records: 288

# Generator-specific settings
config:
  start_date: "2025-09-01"
  frequency_minutes: 5
  sensor_ids: ["SENSOR_001"]
  locations: ["Building A"]

# Optional: Configure null values for specific columns
null_config:
  humidity:
    enabled: true
    rate: 0.05  # 5% of humidity values will be null
  co2_level:
    enabled: true
    rate: 0.02  # 2% of co2_level values will be null
```

## CLI Commands

### `generate`
Generates data based on a YAML configuration file.

```bash
python cli.py generate <config_file> [OPTIONS]

Options:
  --preview N     Show the first N rows in the terminal without saving.
  --stats         Display statistics about the generated data, including null counts.
```

### `list-configs`
Lists all available YAML configurations in the `config/` directory.

```bash
python cli.py list-configs
```

### `validate`
Validates the syntax and structure of a configuration file.

```bash
python cli.py validate <config_file>
```

## Project Structure

```
.
├── cli.py                      # Main CLI entry point
├── config_parser.py            # YAML configuration parser
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── config/                     # Data generation configuration files
│   ├── environmental_sensor.yaml
│   └── ...
│
├── generators/                 # The data generator modules
│   ├── base_generator.py
│   └── ...
│
├── data/                       # Default directory for generated output files
│
└── docs/                       # Additional documentation
    ├── CLI_DOCUMENTATION.md
    ├── QUICK_REFERENCE.md
    └── PROJECT_STRUCTURE.md
```

## Documentation

For more detailed information, see the `docs/` folder:
- **[CLI_DOCUMENTATION.md](docs/CLI_DOCUMENTATION.md)**: Comprehensive CLI command reference.
- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)**: A quick command cheat sheet.
- **[PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)**: A guide to the project's architecture.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
