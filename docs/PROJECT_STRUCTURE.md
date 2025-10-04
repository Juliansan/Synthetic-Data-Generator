# Project Structure

## Overview

This is a CLI-first synthetic data generation tool built with Python, Click, and Rich. The architecture follows a clean separation of concerns with YAML-based configuration.

## Directory Structure

```
data_generator.py/
│
├── cli.py                          # Main CLI entry point (Click framework)
├── config_parser.py                # YAML configuration parser and validator
├── requirements.txt                # Python dependencies
│
├── config/                         # YAML configuration files
│   ├── environmental_sensor.yaml   # Single sensor with null values
│   ├── multi_sensor.yaml          # Multiple sensors with locations
│   ├── business_customers.yaml    # Customer data with nullable fields
│   ├── business_transactions.yaml # Transaction records
│   └── user_profiles.yaml         # User profiles with optional fields
│
├── generators/                     # Data generator modules
│   ├── __init__.py
│   ├── base_generator.py          # Base class with common utilities
│   ├── environmental_sensor.py    # Sensor data with temporal patterns
│   ├── business_data.py           # Business records (customers, transactions)
│   └── user_data.py               # User profile data
│
├── data/                          # Generated output files (CSV/Excel)
│   ├── sensor_readings.csv
│   ├── multi_sensor_readings.csv
│   └── customers.csv
│
└── docs/                          # Documentation
    ├── README.md                  # Main documentation
    ├── CLI_DOCUMENTATION.md       # CLI command reference
    ├── NEW_CLI_SUMMARY.md         # Implementation details
    ├── FINAL_SUMMARY.md           # Complete feature overview
    └── QUICK_REFERENCE.md         # Quick command cheat sheet
```

## Core Components

### 1. CLI Layer (`cli.py`)
- **Framework**: Click
- **Formatting**: Rich (colors, tables, progress bars, panels)
- **Commands**:
  - `generate`: Generate data from YAML config
  - `list-configs`: Show all available configurations
  - `validate`: Validate YAML configuration
- **Features**:
  - Preview mode (`--preview N`)
  - Statistics display (`--stats`)
  - Beautiful terminal output

### 2. Configuration Layer (`config_parser.py`)
- **Purpose**: Parse and validate YAML configuration files
- **Key Classes**:
  - `ConfigParser`: Main parser class
- **Validation**:
  - Required fields check
  - Type validation
  - Generator-specific config validation
  - Null config validation
- **Methods**:
  - `_load()`: Load YAML file
  - `_validate()`: Validate structure
  - `get_column_config()`: Extract column configurations
  - `parse_date()`: Parse date strings

### 3. Generator Layer (`generators/`)

#### Base Generator (`base_generator.py`)
- **Purpose**: Common utilities for all generators
- **Key Features**:
  - Null value support via `add_nulls()`
  - Timestamp generation
  - ID generation
  - Categorical data generation
  - Numeric data generation
- **Methods**:
  - `add_nulls(series, null_rate)`: Add null values to column
  - `generate_timestamps()`: Create time series
  - `generate_ids()`: Generate unique IDs
  - `generate_categorical()`: Random categorical values
  - `generate_numeric()`: Random numeric values

#### Environmental Sensor Generator (`environmental_sensor.py`)
- **Purpose**: Generate realistic sensor data with temporal patterns
- **Features**:
  - Multiple sensors support
  - Location mapping
  - Temporal patterns (daily cycles, work hours)
  - Null value support per column
- **Data Patterns**:
  - **Temperature**: Daily cycles (15-30°C) with hour-of-day variations
  - **Humidity**: Inverse correlation with temperature (40-90%)
  - **CO2 Level**: Work-hour patterns (300-1200 ppm, higher 9am-5pm)
- **Configuration**:
  ```yaml
  config:
    start_date: "2025-09-01"
    frequency_minutes: 5
    sensor_ids: ["SENSOR_001"]
    locations: ["Building A"]
  null_config:
    humidity:
      enabled: true
      rate: 0.05
  ```

#### Business Data Generator (`business_data.py`)
- **Purpose**: Generate business records (customers, transactions)
- **Data Types**:
  - **Customers**: Names, emails, phones, addresses, registration dates
  - **Transactions**: Order IDs, products, amounts, tax, shipping
- **Features**:
  - Faker integration for realistic names/addresses
  - Configurable business types
  - Optional address fields
  - Date range support
- **Configuration**:
  ```yaml
  config:
    data_type: customers
    include_addresses: true
    business_type: retail
  ```

#### User Data Generator (`user_data.py`)
- **Purpose**: Generate user profile data
- **Features**:
  - Personal information (names, emails, usernames)
  - Demographics (age ranges, locations)
  - Social media data (bios, handles)
  - Optional fields support
- **Configuration**:
  ```yaml
  config:
    include_bio: true
    include_social: true
    age_range: [18, 65]
  ```

## Data Flow

```
1. User runs CLI command
   ↓
2. cli.py parses arguments (Click)
   ↓
3. config_parser.py loads and validates YAML
   ↓
4. Appropriate generator is instantiated
   ↓
5. Generator creates DataFrame
   ↓
6. Null values applied (if configured)
   ↓
7. Data saved to CSV/Excel
   ↓
8. Rich displays results (tables, stats, progress)
```

## Configuration Schema

### Top-Level Structure
```yaml
generator_type: environmental_sensor | business_data | user_data
output_file: data/output.csv
num_records: 1000
format: csv | excel

config:
  # Generator-specific configuration
  
null_config:  # Optional
  column_name:
    enabled: true
    rate: 0.10  # 10% null values
```

### Generator-Specific Configs

#### Environmental Sensor
```yaml
config:
  start_date: "2025-09-01"
  end_date: "2025-12-31"  # Optional
  frequency_minutes: 5
  sensor_ids: ["SENSOR_001", "SENSOR_002"]
  locations: ["Building A", "Building B"]
```

#### Business Data
```yaml
config:
  data_type: customers | transactions
  include_addresses: true
  business_type: retail | wholesale | service
  date_range: ["2024-01-01", "2024-12-31"]  # For transactions
```

#### User Data
```yaml
config:
  include_bio: true
  include_social: true
  age_range: [18, 65]
  locations: ["US", "UK", "CA"]
```

## Key Features

### 1. Null Value Support
- Configure null rates per column
- Applied after data generation
- Preserves data patterns
- Statistics include null counts

### 2. Temporal Patterns (Environmental Sensor)
- **Daily Cycles**: Temperature varies by hour
- **Seasonal Variations**: Temperature changes by month
- **Work Hours**: CO2 levels higher 9am-5pm
- **Correlations**: Humidity inversely related to temperature

### 3. Rich Terminal Output
- **Colors**: Success (green), errors (red), info (cyan)
- **Tables**: Bordered tables with headers
- **Progress Bars**: Spinner during generation
- **Panels**: Boxed messages for validation/errors
- **Statistics**: Formatted tables with null counts

### 4. Validation
- **Pre-Generation**: Validate YAML before running
- **Required Fields**: Check all required fields present
- **Type Checking**: Validate data types
- **Generator Compatibility**: Check config matches generator type

## Dependencies

```
pandas>=2.0.0      # DataFrame operations
numpy>=1.24.0      # Numerical operations
faker>=18.0.0      # Fake data generation
click>=8.0.0       # CLI framework
rich>=13.0.0       # Terminal formatting
pyyaml>=6.0        # YAML parsing
openpyxl>=3.0.0    # Excel support
```

## Extension Points

### Adding New Generators

1. Create new generator class in `generators/`
2. Inherit from `BaseGenerator`
3. Implement `generate()` method
4. Add generator type to `config_parser.py` validation
5. Add command handling in `cli.py`
6. Create example YAML config in `config/`

Example:
```python
# generators/new_generator.py
from .base_generator import BaseGenerator
import pandas as pd

class NewGenerator(BaseGenerator):
    def generate(self, config, null_config=None):
        # Generate data
        df = pd.DataFrame({
            'column1': [...],
            'column2': [...]
        })
        
        # Apply null values if configured
        if null_config:
            for col, null_conf in null_config.items():
                if null_conf.get('enabled'):
                    df[col] = self.add_nulls(df[col], null_conf['rate'])
        
        return df
```

### Adding New CLI Commands

1. Add new command function in `cli.py`
2. Use Click decorators (`@cli.command()`)
3. Add Rich formatting for output
4. Update documentation

Example:
```python
@cli.command()
@click.argument('input_file')
def new_command(input_file):
    """New command description."""
    console = Console()
    # Implementation
    console.print("[green]Success![/green]")
```

## Best Practices

### Configuration Files
- Use descriptive filenames
- Include comments in YAML
- Start with small `num_records` for testing
- Validate before generating large datasets

### Generators
- Inherit from `BaseGenerator`
- Use existing utilities (timestamps, IDs, etc.)
- Apply null values at the end
- Document temporal patterns and correlations

### CLI Commands
- Use Rich for all output
- Show progress for long operations
- Provide helpful error messages
- Include examples in help text

## Testing

### Manual Testing
```bash
# Validate config
python cli.py validate config/environmental_sensor.yaml

# Preview before generating
python cli.py generate config/environmental_sensor.yaml --preview 5

# Generate with statistics
python cli.py generate config/environmental_sensor.yaml --stats
```

### Verifying Output
```bash
# Check CSV structure
head -n 10 data/sensor_readings.csv

# Count null values
grep ",," data/sensor_readings.csv | wc -l

# View statistics
python cli.py generate config/environmental_sensor.yaml --stats
```

## Future Enhancements

Potential additions:
- [ ] More generator types (IoT devices, financial data, logs)
- [ ] Data quality rules (constraints, ranges)
- [ ] Relationship support (foreign keys between datasets)
- [ ] Custom plugins for generators
- [ ] API mode (REST endpoints)
- [ ] Streaming generation for large datasets
- [ ] Data anonymization features
- [ ] Template system for configs
