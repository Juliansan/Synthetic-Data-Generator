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

- `generate()` - Main generation method (implemented by subclasses)
- `save_to_csv()` - Save DataFrame to CSV
- `save_to_excel()` - Save DataFrame to Excel
- `save_to_json()` - Save DataFrame to JSON
- `preview()` - Display preview of generated data
- `generate_timestamps()` - Generate timestamp sequences
- `generate_ids()` - Generate ID values
- `generate_categorical()` - Generate categorical data
- `generate_numeric()` - Generate numeric data with distributions

### EnvironmentalSensorGenerator

Generates realistic environmental sensor data with temporal patterns.

**Features:**
- Realistic temperature variations with daily/seasonal patterns
- Humidity correlated with temperature
- CO2 level fluctuations based on time of day
- Multi-sensor support with location tracking
- Anomaly injection for testing

**Example:**
```python
from generators import EnvironmentalSensorGenerator

gen = EnvironmentalSensorGenerator(seed=42)

# Single sensor
df = gen.generate(
    n_rows=100,
    freq='5min',
    temp_range=(18.0, 26.0),
    humidity_range=(35.0, 75.0),
    co2_range=(400, 1000)
)

# Multiple sensors
df = gen.generate_multi_sensor(
    n_sensors=3,
    readings_per_sensor=50,
    include_location=True
)
```

**Output columns:**
- `timestamp` - Reading timestamp
- `sensor_id` - Sensor identifier
- `temperature` - Temperature in Celsius
- `humidity` - Humidity percentage
- `co2_level` - CO2 level in ppm
- `location` - Sensor location (optional)

### BusinessDataGenerator

Generates realistic business and e-commerce data.

**Features:**
- Customer profiles with contact information
- Transaction/order data with realistic patterns
- Product catalogs with pricing
- Sales aggregates (daily/weekly/monthly)

**Example:**
```python
from generators import BusinessDataGenerator

gen = BusinessDataGenerator(seed=42)

# Generate customers
customers = gen.generate_customers(n_rows=100, include_address=True)

# Generate transactions
transactions = gen.generate_transactions(
    n_rows=500,
    n_customers=100,
    include_shipping=True
)

# Generate product catalog
products = gen.generate_products(n_rows=200, include_inventory=True)

# Generate sales aggregates
sales = gen.generate_sales_data(n_rows=90, freq='D')
```

**Available methods:**
- `generate_customers()` - Customer data with contact info and addresses
- `generate_transactions()` - Order/transaction data with products and pricing
- `generate_products()` - Product catalog with categories and inventory
- `generate_sales_data()` - Aggregated sales metrics

### UserDataGenerator

Generates realistic user and account data.

**Features:**
- User profiles with demographics
- Account and subscription data
- Login activity logs
- User preferences and settings

**Example:**
```python
from generators import UserDataGenerator

gen = UserDataGenerator(seed=42)

# Generate user profiles
users = gen.generate_user_profiles(
    n_rows=100,
    include_bio=True,
    include_social=True
)

# Generate account data
accounts = gen.generate_accounts(n_rows=100, include_subscription=True)

# Generate login activity
logins = gen.generate_login_activity(n_rows=1000, n_users=100)

# Generate preferences
prefs = gen.generate_user_preferences(n_rows=100)
```

**Available methods:**
- `generate_user_profiles()` - User profiles with personal information
- `generate_accounts()` - Account and subscription data
- `generate_login_activity()` - Login event logs
- `generate_user_preferences()` - User settings and preferences

## Creating Custom Generators

To create a new specialized generator:

1. Import and inherit from `BaseGenerator`
2. Implement the `generate()` method
3. Use base class utilities for common tasks

**Example:**
```python
from generators.base_generator import BaseGenerator
import pandas as pd

class MyCustomGenerator(BaseGenerator):
    def __init__(self, locale='en_US', seed=None):
        super().__init__(locale, seed)
    
    def generate(self, n_rows=100, **kwargs):
        data = {
            'id': self.generate_ids(n_rows),
            'timestamp': self.generate_timestamps(n_rows),
            'value': self.generate_numeric(n_rows, 0, 100)
        }
        return pd.DataFrame(data)
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
