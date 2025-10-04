# Data Generator CLI Documentation

## Overview

The Data Generator CLI is a powerful command-line tool for generating realistic synthetic data using YAML configuration files. Built with **Click** and **Rich**, it provides a beautiful, user-friendly interface for data generation.

## Features

✅ **YAML-based configuration** - Define your data schema in simple YAML files  
✅ **Multiple generator types** - Environmental sensors, business data, user profiles, etc.  
✅ **Null value support** - Configure nullable columns with custom null rates  
✅ **Beautiful CLI** - Rich formatting with colors, tables, and progress indicators  
✅ **Validation** - Validate configuration files before generation  
✅ **Preview & Stats** - See samples and statistics of generated data  

## Installation

```bash
cd data_generator.py
pip install -r requirements.txt
```

## Quick Start

### 1. List Available Configurations

```bash
python cli.py list-configs
```

Output:
```
╭───────────────────────────────╮
│ Available Configuration Files │
╰───────────────────────────────╯
╭────────────────────────────┬───────────────────────┬───────╮
│ File                       │ Generator Type        │ Rows  │
├────────────────────────────┼───────────────────────┼───────┤
│ environmental_sensor.yaml  │ environmental_sensor  │ 288   │
│ multi_sensor.yaml          │ environmental_sensor  │ 480   │
│ business_customers.yaml    │ business_customers    │ 1,000 │
╰────────────────────────────┴───────────────────────┴───────╯
```

### 2. Validate a Configuration

```bash
python cli.py validate config/environmental_sensor.yaml
```

### 3. Generate Data

```bash
# Basic generation
python cli.py generate config/environmental_sensor.yaml

# With preview and statistics
python cli.py generate config/environmental_sensor.yaml --preview 10 --stats
```

## CLI Commands

### `generate`

Generate data from a YAML configuration file.

```bash
python cli.py generate <config_file> [OPTIONS]
```

**Options:**
- `--preview, -p INTEGER`: Number of rows to preview (default: 5, 0 to disable)
- `--stats, -s`: Show statistics about generated data

**Example:**
```bash
python cli.py generate config/environmental_sensor.yaml --preview 10 --stats
```

### `list-configs`

List all available configuration files in the `config/` directory.

```bash
python cli.py list-configs
```

### `validate`

Validate a YAML configuration file without generating data.

```bash
python cli.py validate <config_file>
```

## YAML Configuration Format

### Basic Structure

```yaml
generator: <generator_type>
output_file: <path_to_output>
rows: <number_of_rows>
seed: <random_seed>  # optional

settings:
  # Generator-specific settings
```

### Generator Types

1. **environmental_sensor** - Environmental sensor data
2. **business_customers** - Customer profiles
3. **business_transactions** - Transaction/order data
4. **business_products** - Product catalog
5. **business_sales** - Sales aggregates
6. **user_profiles** - User profile data
7. **user_accounts** - Account data
8. **user_activity** - Login activity
9. **user_preferences** - User settings

### Configuring Null Values

Add nullable columns with custom null rates:

```yaml
settings:
  columns:
    column_name:
      nullable: true
      null_rate: 0.10  # 10% null values
```

## Example Configurations

### Environmental Sensor

```yaml
generator: environmental_sensor
output_file: data/sensor_readings.csv
rows: 288  # 24 hours at 5-minute intervals
seed: 42

settings:
  frequency: "5min"
  start_date: "2025-09-01 00:00:00"
  
  temperature:
    min: 18.0
    max: 26.0
    nullable: false
    null_rate: 0.0
  
  humidity:
    min: 35.0
    max: 75.0
    nullable: true
    null_rate: 0.05  # 5% nulls
  
  co2_level:
    min: 400
    max: 1200
    nullable: true
    null_rate: 0.02  # 2% nulls
  
  sensors:
    - id: "SENSOR_001"
      location: "Building A - Floor 1 - Room 101"
  
  anomalies:
    enabled: true
    rate: 0.03
```

### Multi-Sensor Configuration

```yaml
generator: environmental_sensor
output_file: data/multi_sensor_readings.csv
rows: 480
seed: 42

settings:
  frequency: "15min"
  
  sensors:
    - id: "ROOM_101"
      location: "Building A - Floor 1 - Room 101"
    - id: "ROOM_102"
      location: "Building A - Floor 1 - Room 102"
    - id: "CONF_ROOM"
      location: "Building A - Floor 2 - Conference Room"
    - id: "LOBBY"
      location: "Building B - Floor 1 - Lobby"
```

### Business Customers

```yaml
generator: business_customers
output_file: data/customers.csv
rows: 1000
seed: 42

settings:
  include_address: true
  include_signup_date: true
  
  columns:
    phone:
      nullable: true
      null_rate: 0.10  # 10% don't have phone
    
    zip_code:
      nullable: true
      null_rate: 0.05
```

## Output Examples

### Sensor Data

```csv
timestamp,sensor_id,temperature,humidity,co2_level,location
2025-09-01 00:00:00,SENSOR_001,20.17,61.06,494.0,Building A - Floor 1 - Room 101
2025-09-01 00:05:00,SENSOR_001,19.85,59.46,619.0,Building A - Floor 1 - Room 101
2025-09-01 00:10:00,SENSOR_001,19.8,66.87,551.0,Building A - Floor 1 - Room 101
2025-09-01 00:15:00,SENSOR_001,19.8,,522.0,Building A - Floor 1 - Room 101
```

Note the empty value in the 4th row (humidity column) - this is a null value configured at 5% rate.

## Advanced Usage

### Custom Date Ranges

```yaml
settings:
  start_date: "2025-01-01 00:00:00"
  end_date: "2025-12-31 23:59:59"
```

Supported date formats:
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM:SS`

### Frequency Options

For time-series data:
- `1min` - Every minute
- `5min` - Every 5 minutes
- `15min` - Every 15 minutes
- `1H` or `1h` - Hourly
- `D` - Daily
- `W` - Weekly
- `M` - Monthly

### Anomaly Injection

For testing edge cases:

```yaml
settings:
  anomalies:
    enabled: true
    rate: 0.03  # 3% anomalous readings
```

## Troubleshooting

### Configuration Validation Errors

If you get a validation error:

```bash
python cli.py validate config/your_config.yaml
```

This will show exactly what's wrong with your configuration.

### Missing Required Fields

All configs must have:
- `generator` - The generator type
- `output_file` - Where to save the data
- `rows` - Number of rows to generate

### Invalid Generator Type

Check `python cli.py list-configs` to see valid generator types in action, or see the list above.

## Tips

1. **Start small** - Test with a small number of rows first
2. **Use seeds** - For reproducible data generation
3. **Validate first** - Always validate your config before generating large datasets
4. **Preview data** - Use `--preview` to check output format
5. **Check stats** - Use `--stats` to verify null rates and ranges

## Creating New Configurations

1. Copy an existing config from `config/`
2. Modify the settings for your use case
3. Validate: `python cli.py validate config/your_config.yaml`
4. Generate: `python cli.py generate config/your_config.yaml --preview 5`

## Support

For more examples, check the `config/` directory for various pre-built configurations.
