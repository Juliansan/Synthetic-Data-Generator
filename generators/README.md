# Data Generators

This folder contains specialized data generators for different types of synthetic data.

## Structure

```
generators/
├── __init__.py                    # Package initialization
├── base_generator.py              # Base class with common functionality
├── environmental_sensor.py        # Environmental sensor data generator
├── business_data.py               # Business and e-commerce data generator
└── user_data.py                   # User profiles and activity data generator
```

## Generators

### BaseGenerator

The base class that all specialized generators inherit from. Provides common utilities:

- `generate_ids()`
- `generate_categorical()`
- `generate_numeric()`
- `add_nulls()`

### EnvironmentalSensorGenerator

Generates realistic environmental sensor data with temporal patterns. This generator is used when you set `generator_type: environmental_sensor` in your YAML configuration.

**Features:**
- Realistic temperature variations with daily/seasonal patterns
- Humidity correlated with temperature
- CO2 level fluctuations based on time of day
- Multi-sensor support with location tracking

**Output columns:**
- `timestamp` - Reading timestamp
- `sensor_id` - Sensor identifier
- `temperature` - Temperature in Celsius
- `humidity` - Humidity percentage
- `co2_level` - CO2 level in ppm
- `location` - Sensor location (optional)

### BusinessDataGenerator

Generates realistic business and e-commerce data. This generator is used when you set `generator_type: business_data` in your YAML configuration.

**Features:**
- Customer profiles with contact information
- Transaction/order data with realistic patterns
- Product catalogs with pricing
- Sales aggregates (daily/weekly/monthly)

**Key `data_type` options in YAML:**
- `customers`: Generates customer data with contact info and addresses.
- `transactions`: Creates order/transaction data with products and pricing.
- `products`: Builds a product catalog with categories and inventory.
- `sales`: Generates aggregated sales metrics.

### UserDataGenerator

Generates realistic user and account data. This generator is used when you set `generator_type: user_data` in your YAML configuration.

**Features:**
- User profiles with demographics
- Account and subscription data
- Login activity logs
- User preferences and settings

**Key `data_type` options in YAML:**
- `user_profiles`: Creates user profiles with personal information.
- `accounts`: Generates account and subscription data.
- `login_activity`: Creates login event logs.
- `user_preferences`: Generates user settings and preferences.

## Creating Custom Generators

To create a new specialized generator that works with the CLI:

1.  Create a new Python file in the `generators/` directory (e.g., `my_generator.py`).
2.  In that file, create a class that inherits from `BaseGenerator`.
3.  Implement the `generate()` method. This method will receive the `config` and `null_config` sections from the YAML file.
4.  In `config_parser.py`, add your new generator's name to the `GENERATOR_MAP`.

**Example: `generators/my_generator.py`**
```python
from .base_generator import BaseGenerator
import pandas as pd

class MyCustomGenerator(BaseGenerator):
    def generate(self, config, null_config=None):
        # Use parameters from the 'config' section of the YAML
        num_records = config.get('num_records', 100)
        my_param = config.get('my_param', 'default_value')

        data = {
            'id': self.generate_ids(num_records),
            'custom_data': [f"{my_param}_{i}" for i in range(num_records)]
        }
        df = pd.DataFrame(data)

        # Apply nulls if configured
        if null_config:
            # ... apply null logic ...

        return df
```

**Update `config_parser.py`:**
```python
# ... inside ConfigParser class ...
from generators.my_generator import MyCustomGenerator

class ConfigParser:
    GENERATOR_MAP = {
        'environmental_sensor': EnvironmentalSensorGenerator,
        'business_data': BusinessDataGenerator,
        'user_data': UserDataGenerator,
        'my_generator': MyCustomGenerator,  # Add this line
    }
    # ... rest of the class
```

## Common Parameters

Most generators support these common parameters:

- `n_rows` - Number of rows to generate
- `seed` - Random seed for reproducibility
- `locale` - Faker locale (default: 'en_US')

## Dependencies

- pandas
- numpy
- faker

See `requirements.txt` in the project root for versions.
