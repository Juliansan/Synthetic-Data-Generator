# Quick Reference Card

## Installation

```bash
pip install -r requirements.txt
```

## Basic Commands

```bash
# List all available configs
python cli.py list-configs

# Validate a config
python cli.py validate config/environmental_sensor.yaml

# Generate data
python cli.py generate config/environmental_sensor.yaml

# Generate with preview
python cli.py generate config/environmental_sensor.yaml --preview 10

# Generate with stats
python cli.py generate config/environmental_sensor.yaml --stats

# Generate with both
python cli.py generate config/environmental_sensor.yaml --preview 10 --stats
```

## YAML Template

```yaml
generator: environmental_sensor
output_file: data/my_output.csv
rows: 100
seed: 42  # optional, for reproducibility

settings:
  frequency: "5min"  # For time-series data
  
  # Configure columns with null support
  column_name:
    min: 0
    max: 100
    nullable: true
    null_rate: 0.10  # 10% null values
```

## Available Generators

- `environmental_sensor` - Sensor data (temp, humidity, CO2)
- `business_customers` - Customer profiles
- `business_transactions` - Transaction data
- `business_products` - Product catalog
- `user_profiles` - User data

## Null Value Configuration

```yaml
columns:
  column_name:
    nullable: true
    null_rate: 0.05  # 5% null values
```

## Frequency Options

- `1min` - Every minute
- `5min` - Every 5 minutes
- `15min` - Every 15 minutes
- `1H` or `1h` - Hourly
- `D` - Daily

## Date Formats

```yaml
start_date: "2025-09-01"
# or
start_date: "2025-09-01 14:30:00"
```

## Quick Troubleshooting

**Module not found?**
```bash
pip install -r requirements.txt
```

**Config validation fails?**
```bash
python cli.py validate config/your_config.yaml
```

**Want to see what configs exist?**
```bash
python cli.py list-configs
```

## Example: Environmental Sensor

```bash
# Use the pre-built config
python cli.py generate config/environmental_sensor.yaml --preview 10 --stats

# Output: data/sensor_readings.csv
# - timestamp (5-min intervals)
# - sensor_id
# - temperature (18-26°C)
# - humidity (35-75%, 5% nulls)
# - co2_level (400-1200 ppm, 2% nulls)
# - location
```

## Example: Multi-Sensor

```bash
python cli.py generate config/multi_sensor.yaml --preview 8

# Output: data/multi_sensor_readings.csv
# Multiple sensors across different locations
```

## Example: Business Data

```bash
python cli.py generate config/business_customers.yaml --preview 5 --stats

# Output: data/customers.csv
# 1,000 customers with configurable null values on phone, address, etc.
```
