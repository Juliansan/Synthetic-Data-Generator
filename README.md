# Synthetic Data Generator# Synthetic Data Generator# Smart Synthetic Data Generator



A powerful CLI tool for generating realistic synthetic data using YAML configuration files. Built with Click, Rich, and specialized generators for environmental sensors, business data, and user profiles.



## FeaturesA powerful CLI tool for generating realistic synthetic data using YAML configuration files. Built with Click, Rich, and specialized generators for environmental sensors, business data, and user profiles.A powerful Python tool for generating realistic synthetic datasets for data engineering practice, testing ETL pipelines, and populating development databases.



- 🎯 **CLI-First Design**: Simple, intuitive command-line interface

- 📝 **YAML Configuration**: Declarative config files for easy customization

- 🎨 **Beautiful Output**: Rich terminal formatting with colors, tables, and progress bars## Features## 🌟 Features

- 🔍 **Null Value Support**: Configure null rates per column for realistic data

- 📊 **Multiple Generators**: Environmental sensors, business data, user profiles

- ✅ **Validation**: Built-in config validation before generation

- 🎯 **CLI-First Design**: Simple, intuitive command-line interface- **Modular Architecture** - Specialized generators for different data types:

## Quick Start

- 📝 **YAML Configuration**: Declarative config files for easy customization  - Environmental sensor data (temperature, humidity, CO2 levels)

### Installation

- 🎨 **Beautiful Output**: Rich terminal formatting with colors, tables, and progress bars  - Business/E-commerce data (customers, transactions, products)

```bash

# Create virtual environment- 🔍 **Null Value Support**: Configure null rates per column for realistic data  - User data (profiles, accounts, activity logs)

python3 -m venv .venv

source .venv/bin/activate  # On Linux/Mac- 📊 **Multiple Generators**: Environmental sensors, business data, user profiles  - General-purpose data generation

# .venv\Scripts\activate  # On Windows

- ✅ **Validation**: Built-in config validation before generation- **Intelligent Column Detection** - Automatically detects data types from column names (emails, phones, dates, prices, etc.)

# Install dependencies

pip install -r requirements.txt- **Learn from Samples** - Analyze existing datasets and generate similar data while preserving:

```

## Quick Start  - Data type patterns

### Usage

  - Value distributions (min, max, mean, std)

```bash

# Generate data from a config file### Installation  - Categorical relationships

python cli.py generate config/environmental_sensor.yaml

  - Realistic null rates

# Preview first 10 rows

python cli.py generate config/environmental_sensor.yaml --preview 10```bash- **Multiple Generation Modes**:



# Show statistics about generated data# Create virtual environment  - From column names (auto-detection)

python cli.py generate config/environmental_sensor.yaml --stats

python3 -m venv .venv  - From explicit type definitions

# List all available configurations

python cli.py list-configssource .venv/bin/activate  # On Linux/Mac  - From sample data (pattern learning)



# Validate a configuration file# .venv\Scripts\activate  # On Windows  - Interactive CLI mode

python cli.py validate config/environmental_sensor.yaml

```  - Specialized generators for specific domains



## Configuration# Install dependencies- **Maintains Statistical Properties** - Unlike pure random data, generates coherent, realistic datasets



### YAML Structurepip install -r requirements.txt- **CLI & Python API** - Use via command line or import as a library



```yaml```

generator_type: environmental_sensor  # or business_data, user_data

output_file: data/sensor_readings.csv## 📦 Installation

num_records: 288

format: csv  # or excel### Basic Usage



# Generator-specific config### Requirements

config:

  start_date: "2025-09-01"```bash

  frequency_minutes: 5

  sensor_ids: ["SENSOR_001"]# Generate data from a config file```bash

  locations: ["Building A"]

python cli.py generate config/environmental_sensor.yamlpip install pandas numpy faker

# Optional: Configure null values per column

null_config:```

  humidity:

    enabled: true# Preview first 10 rows

    rate: 0.05  # 5% null values

  co2_level:python cli.py generate config/environmental_sensor.yaml --preview 10### Optional (for Excel support)

    enabled: true

    rate: 0.02  # 2% null values

```

# Show statistics about generated data```bash

### Example Configurations

python cli.py generate config/environmental_sensor.yaml --statspip install openpyxl

The `config/` folder includes ready-to-use examples:

```

- **environmental_sensor.yaml**: Single sensor with null values

- **multi_sensor.yaml**: Multiple sensors with different locations# List all available configurations

- **business_customers.yaml**: Customer data with nullable fields

- **business_transactions.yaml**: Transaction recordspython cli.py list-configs## 🚀 Quick Start

- **user_profiles.yaml**: User profiles with optional fields



## Generators

# Validate a configuration file### Command Line Interface

### Environmental Sensor Generator

Generates realistic sensor data with temporal patterns:python cli.py validate config/environmental_sensor.yaml

- **Temperature**: Daily cycles with seasonal variations

- **Humidity**: Inverse correlation with temperature``````bash

- **CO2 Levels**: Work-hour patterns (higher during business hours)

# Show help

### Business Data Generator

Creates realistic business records:## Configurationpython data_generator.py -h

- **Customers**: Names, emails, phones, addresses, registration dates

- **Transactions**: Order IDs, products, amounts, tax, shipping



### User Data Generator### YAML Structure# Interactive mode (easiest way to get started!)

Generates user profile data:

- **Personal Info**: Names, emails, usernamespython data_generator.py -i

- **Demographics**: Age ranges, locations

- **Social**: Bios, social media handles```yaml



## CLI Commandsgenerator_type: environmental_sensor  # or business_data, user_data# Generate from column names



### Generate Dataoutput_file: data/sensor_readings.csvpython data_generator.py -c "user_id,name,email,phone,city" -n 1000

```bash

python cli.py generate <config_file> [OPTIONS]num_records: 288



Options:format: csv  # or excel# Learn from a sample file

  --preview N     Show first N rows without saving

  --stats         Display statistics about generated datapython data_generator.py -s sample_data.csv -n 5000 -o output.csv

```

# Generator-specific config

### List Configurations

```bashconfig:# Use a JSON schema file

python cli.py list-configs

```  start_date: "2025-09-01"python data_generator.py --schema my_schema.json -n 2000

Shows all available configuration files with details.

  frequency_minutes: 5```

### Validate Configuration

```bash  sensor_ids: ["SENSOR_001"]

python cli.py validate <config_file>

```  locations: ["Building A"]### Python API - Specialized Generators

Validates YAML syntax and structure before generation.



## Project Structure

# Optional: Configure null values per column#### Environmental Sensor Data

```

.null_config:

├── cli.py                      # Main CLI entry point

├── config_parser.py           # YAML configuration parser  humidity:```python

├── requirements.txt           # Python dependencies

├── README.md                  # This file    enabled: truefrom generators import EnvironmentalSensorGenerator

│

├── config/                    # Configuration files    rate: 0.05  # 5% null valuesfrom datetime import datetime, timedelta

│   ├── environmental_sensor.yaml

│   ├── multi_sensor.yaml  co2_level:

│   ├── business_customers.yaml

│   ├── business_transactions.yaml    enabled: true# Initialize generator

│   └── user_profiles.yaml

│    rate: 0.02  # 2% null valuesgenerator = EnvironmentalSensorGenerator(seed=42)

├── generators/                # Data generators

│   ├── base_generator.py```

│   ├── environmental_sensor.py

│   ├── business_data.py# Generate single sensor data

│   └── user_data.py

│### Example Configurationsdf = generator.generate(

├── data/                      # Generated output files

│    n_rows=100,

└── docs/                      # Additional documentation

    ├── CLI_DOCUMENTATION.md   # Detailed CLI referenceThe `config/` folder includes ready-to-use examples:    freq='5min',  # 5-minute intervals

    ├── QUICK_REFERENCE.md     # Command cheat sheet

    └── PROJECT_STRUCTURE.md   # Architecture guide    temp_range=(18.0, 26.0),

```

- **environmental_sensor.yaml**: Single sensor with null values    humidity_range=(35.0, 75.0),

## Examples

- **multi_sensor.yaml**: Multiple sensors with different locations    co2_range=(400, 1000)

### Generate environmental sensor data with nulls

```bash- **business_customers.yaml**: Customer data with nullable fields)

python cli.py generate config/environmental_sensor.yaml --stats

```- **business_transactions.yaml**: Transaction records



### Preview business customer data- **user_profiles.yaml**: User profiles with optional fields# Generate multi-sensor data with location

```bash

python cli.py generate config/business_customers.yaml --preview 10df_multi = generator.generate_multi_sensor(

```

## Generators    n_sensors=3,

### Generate multi-sensor readings

```bash    readings_per_sensor=50,

python cli.py generate config/multi_sensor.yaml

```### Environmental Sensor Generator    include_location=True



## DocumentationGenerates realistic sensor data with temporal patterns:)



For detailed information, see the `docs/` folder:- **Temperature**: Daily cycles with seasonal variations

- **[CLI_DOCUMENTATION.md](docs/CLI_DOCUMENTATION.md)**: Comprehensive CLI reference

- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)**: Quick command cheat sheet  - **Humidity**: Inverse correlation with temperature# Save to CSV

- **[PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)**: Architecture and developer guide

- **CO2 Levels**: Work-hour patterns (higher during business hours)generator.save_to_csv(df, 'sensor_data.csv')

## Dependencies

```

- **pandas**: DataFrame manipulation

- **numpy**: Numerical operations```yaml

- **faker**: Realistic fake data generation

- **click**: Modern CLI frameworkgenerator_type: environmental_sensor#### Business/E-commerce Data

- **rich**: Beautiful terminal formatting

- **pyyaml**: YAML configuration parsingconfig:

- **openpyxl**: Excel file support

  start_date: "2025-09-01"```python

## License

  frequency_minutes: 5from generators import BusinessDataGenerator

MIT License

  sensor_ids: ["SENSOR_001", "SENSOR_002"]

## Contributing

  locations: ["Building A", "Building B"]# Initialize generator

Contributions are welcome! Please feel free to submit a Pull Request.

```generator = BusinessDataGenerator(seed=42)



### Business Data Generator# Generate customer data

Creates realistic business records:df_customers = generator.generate_customers(

- **Customers**: Names, emails, phones, addresses, registration dates    n_rows=100,

- **Transactions**: Order IDs, products, amounts, tax, shipping    include_address=True,

    include_signup_date=True

```yaml)

generator_type: business_data

config:# Generate transaction data

  data_type: customers  # or transactionsdf_transactions = generator.generate_transactions(

  include_addresses: true    n_rows=500,

  business_type: retail    n_customers=100,

```    include_shipping=True

)

### User Data Generator

Generates user profile data:# Generate product catalog

- **Personal Info**: Names, emails, usernamesdf_products = generator.generate_products(n_rows=200, include_inventory=True)

- **Demographics**: Age ranges, locations

- **Social**: Bios, social media handles# Generate daily sales aggregates

df_sales = generator.generate_sales_data(n_rows=90, freq='D')

```yaml```

generator_type: user_data

config:#### User/Account Data

  include_bio: true

  include_social: true```python

  age_range: [18, 65]from generators import UserDataGenerator

```

# Initialize generator

## CLI Commandsgenerator = UserDataGenerator(seed=42)



### Generate Data# Generate user profiles

```bashdf_users = generator.generate_user_profiles(

python cli.py generate <config_file> [OPTIONS]    n_rows=100,

    include_bio=True,

Options:    include_social=True

  --preview N     Show first N rows without saving)

  --stats         Display statistics about generated data

```# Generate account data

df_accounts = generator.generate_accounts(n_rows=100, include_subscription=True)

### List Configurations

```bash# Generate login activity

python cli.py list-configsdf_logins = generator.generate_login_activity(n_rows=1000, n_users=100)

```

Shows all available configuration files with details.# Generate user preferences

df_prefs = generator.generate_user_preferences(n_rows=100)

### Validate Configuration```

```bash

python cli.py validate <config_file>### General-Purpose Generator (Original)

```

Validates YAML syntax and structure before generation.```python

from data_generator import SmartDataGenerator

## Project Structure

# Initialize generator

```generator = SmartDataGenerator(seed=42)

.

├── cli.py                      # Main CLI entry point# Generate from column names

├── config_parser.py           # YAML configuration parsercolumns = ['user_id', 'name', 'email', 'signup_date']

├── requirements.txt           # Python dependenciesdf = generator.generate_from_schema(columns, n_rows=1000)

├── config/                    # Configuration files

│   ├── environmental_sensor.yaml# Save to CSV

│   ├── multi_sensor.yamldf.to_csv('output.csv', index=False)

│   ├── business_customers.yaml```

│   ├── business_transactions.yaml

│   └── user_profiles.yaml## 🎨 Interactive Mode

├── generators/                # Data generators

│   ├── base_generator.pyThe easiest way to create datasets:

│   ├── environmental_sensor.py

│   ├── business_data.py```bash

│   └── user_data.py$ python data_generator.py -i

└── data/                      # Generated output files

```🎨 INTERACTIVE MODE - Build Your Dataset

======================================================================

## Advanced Features

Enter column definitions (type 'done' when finished)

### Null Value ConfigurationFormat: column_name [type]



Control null values per column for realistic data:Available types:

  id, name, email, phone, address, city, country, company

```yaml  date, price, age, product, category, status, description

null_config:  url, percentage, integer, float, text

  column_name:

    enabled: trueColumn: user_id id

    rate: 0.10  # 10% null values  ✓ Added 'user_id' as id

```Column: customer_name

  ✓ Added 'customer_name' (auto-detected as name)

### Custom Date RangesColumn: email_address

  ✓ Added 'email_address' (auto-detected as email)

Specify exact date ranges for time-series data:Column: signup_date date

  ✓ Added 'signup_date' as date

```yamlColumn: done

config:

  start_date: "2025-01-01"Number of rows to generate [100]: 500

  end_date: "2025-12-31"Output file [synthetic_data.csv]: customers.csv

  frequency_minutes: 15

```🔄 Generating 500 rows...

✅ Generated 500 rows and saved to 'customers.csv'

### Multiple Output Formats```



Support for CSV and Excel:## 📋 CLI Options



```yaml| Flag | Description | Default |

format: csv    # or excel|------|-------------|---------|

output_file: data/output.csv  # or .xlsx| `-i, --interactive` | Launch interactive mode | - |

```| `-c, --columns` | Comma-separated column names | - |

| `-s, --sample` | Sample file to learn from (.csv, .xlsx, .json) | - |

## Examples| `--schema` | JSON schema file with column definitions | - |

| `-n, --rows` | Number of rows to generate | 100 |

### Generate environmental sensor data with nulls| `-o, --output` | Output CSV filename | synthetic_data.csv |

```bash| `--seed` | Random seed for reproducibility | None |

python cli.py generate config/environmental_sensor.yaml --stats| `-p, --preview` | Number of preview rows to display | 5 |

```| `--locale` | Faker locale (e.g., en_US, es_ES) | en_US |



### Preview business customer data## 💡 Usage Examples

```bash

python cli.py generate config/business_customers.yaml --preview 10### 1. E-commerce Dataset

```

```bash

### Generate multi-sensor readingspython data_generator.py \

```bash  -c "order_id,customer_email,product_name,price,order_date,status" \

python cli.py generate config/multi_sensor.yaml  -n 10000 -o ecommerce_transactions.csv

``````



## Documentation### 2. Learn from Existing Data



- **CLI_DOCUMENTATION.md**: Detailed CLI command reference```bash

- **NEW_CLI_SUMMARY.md**: Implementation details and architecture# Generator will learn patterns and distributions from your sample

- **FINAL_SUMMARY.md**: Complete feature overviewpython data_generator.py -s production_sample.csv -n 100000 -o test_data.csv

- **QUICK_REFERENCE.md**: Quick command cheat sheet```



## Dependencies### 3. Reproducible Test Data



- **pandas**: DataFrame manipulation```bash

- **numpy**: Numerical operations# Use --seed for consistent results across runs

- **faker**: Realistic fake data generationpython data_generator.py \

- **click**: Modern CLI framework  -c "id,name,email,created_at" \

- **rich**: Beautiful terminal formatting  -n 1000 --seed 123 -o test_users.csv

- **pyyaml**: YAML configuration parsing```

- **openpyxl**: Excel file support

### 4. Custom Schema with JSON

## License

Create `schema.json`:

MIT License```json

{

## Contributing  "user_id": "id",

  "full_name": "name",

Contributions are welcome! Please feel free to submit a Pull Request.  "email": "email",

  "registration_date": "date",
  "age": "age",
  "subscription_type": "category",
  "account_status": "status"
}
```

Generate:
```bash
python data_generator.py --schema schema.json -n 5000 -o users.csv
```

### 5. No Preview (Faster for Large Datasets)

```bash
python data_generator.py \
  -c "user_id,username,email" \
  -n 1000000 -p 0 -o big_dataset.csv
```

## 🐍 Python API Examples

### Basic Usage

```python
from data_generator import SmartDataGenerator

generator = SmartDataGenerator(seed=42)

# From column names (auto-detection)
df = generator.generate_from_schema(
    ['customer_id', 'name', 'email', 'phone'],
    n_rows=1000
)
```

### Explicit Type Definitions

```python
schema = {
    'user_id': 'id',
    'username': 'name',
    'user_email': 'email',
    'registration_date': 'date',
    'age': 'age',
    'subscription_type': 'category',
    'account_status': 'status'
}

df = generator.generate_from_schema(schema, n_rows=5000)
df.to_csv('users.csv', index=False)
```

### Learn from Sample Data

```python
import pandas as pd

# Load your sample
sample_df = pd.read_csv('sample_data.csv')

# Generate similar data
df = generator.generate_from_sample(sample_df, n_rows=10000)
df.to_csv('generated_data.csv', index=False)
```

### Advanced: Pattern Detection

```python
# The generator automatically detects patterns
sample = pd.DataFrame({
    'product_id': [1, 2, 3],
    'category': ['Electronics', 'Tools', 'Electronics'],
    'price': [29.99, 49.99, 15.50],
    'stock': [100, 50, 200]
})

# Generated data will:
# - Preserve categorical values (Electronics, Tools)
# - Match price distributions
# - Use similar stock levels
df = generator.generate_from_sample(sample, n_rows=1000)
```

## 🎯 Available Data Types

The generator intelligently detects or allows you to specify these types:

| Type | Description | Example Output |
|------|-------------|----------------|
| `id` | Sequential or unique identifiers | 1, 2, 3, ... |
| `name` | Full names | John Smith, Jane Doe |
| `email` | Email addresses | john.smith@example.com |
| `phone` | Phone numbers | +1-555-123-4567 |
| `address` | Street addresses | 123 Main St, Apt 4B |
| `city` | City names | New York, London |
| `country` | Country names | United States, France |
| `company` | Company names | Acme Corp, TechCo |
| `date` | Dates and timestamps | 2024-01-15 14:30:00 |
| `price` | Monetary values | 29.99, 149.50 |
| `age` | Age values | 25, 34, 52 |
| `product` | Product names | Laptop, Phone, Tablet |
| `category` | Categories/types | Premium, Standard, Basic |
| `status` | Status values | Active, Pending, Completed |
| `description` | Text descriptions | Lorem ipsum dolor sit... |
| `url` | URLs | https://example.com |
| `percentage` | Percentage values | 23.45, 78.90 |
| `integer` | Integer numbers | 42, 108, 256 |
| `float` | Floating-point numbers | 3.14, 2.718 |
| `text` | General text | Random text content |

## 🔍 Pattern Detection

The generator uses intelligent pattern matching on column names:

```python
# These columns are auto-detected:
'user_email' or 'email' → email type
'customer_name' or 'username' → name type
'signup_date' or 'created_at' → date type
'product_price' or 'amount' → price type
'user_id' or 'id' → id type
```

## 📊 Real-World Use Cases

### 1. Testing ETL Pipelines

```bash
# Generate realistic test data
python data_generator.py \
  -c "transaction_id,customer_id,amount,transaction_date,status" \
  -n 100000 -o etl_test_data.csv
```

## 📚 Example Scripts

Check the `examples/` folder for complete working examples:

- `example_environmental_sensors.py` - Environmental sensor data generation
- `example_business_data.py` - E-commerce and business data examples
- `example_user_data.py` - User profiles and activity data examples

Run any example:
```bash
python examples/example_environmental_sensors.py
python examples/example_business_data.py
python examples/example_user_data.py
```

## 💡 Use Cases

### 1. Environmental Monitoring System

```python
from generators import EnvironmentalSensorGenerator
from datetime import datetime, timedelta

generator = EnvironmentalSensorGenerator(seed=42)

# Generate a week of hourly sensor readings
df = generator.generate(
    n_rows=168,  # 24 hours * 7 days
    start_date=datetime.now() - timedelta(days=7),
    freq='1H',
    add_anomalies=True,
    anomaly_rate=0.03
)

df.to_csv('./data/sensor_weekly.csv', index=False)
```

### 2. Database Population

```python
from data_generator import SmartDataGenerator
import pandas as pd

generator = SmartDataGenerator()

# Users table
users = generator.generate_from_schema({
    'user_id': 'id',
    'email': 'email',
    'name': 'name',
    'created_at': 'date'
}, n_rows=10000)

# Orders table
orders = generator.generate_from_schema({
    'order_id': 'id',
    'user_id': 'integer',  # Will match user_id range
    'product': 'product',
    'amount': 'price',
    'order_date': 'date'
}, n_rows=50000)
```

### 3. ML Model Development

```bash
# Create training data with consistent distributions
python data_generator.py \
  -s ml_sample.csv \
  -n 1000000 \
  --seed 42 \
  -o ml_training_data.csv
```

### 4. Data Engineering Practice

```bash
# Generate various datasets for practice
python data_generator.py -c "sensor_id,timestamp,temperature,humidity" -n 10000
python data_generator.py -c "log_id,user_id,event_type,timestamp" -n 50000
python data_generator.py -c "customer_id,purchase_amount,category" -n 25000
```

## 🌍 Localization

Generate data in different locales:

```bash
# Spanish data
python data_generator.py -c "nombre,email,telefono,ciudad" --locale es_ES -n 1000

# French data
python data_generator.py -c "nom,email,telephone,ville" --locale fr_FR -n 1000

# German data
python data_generator.py -c "name,email,telefon,stadt" --locale de_DE -n 1000
```

## 🔧 Advanced Features

### Save and Reuse Schemas

```python
generator = SmartDataGenerator()

# Analyze and save schema
sample_df = pd.read_csv('sample.csv')
generator.save_schema(sample_df, 'my_schema.json')

# Later, use the schema
# (Load JSON and use with generate_from_schema)
```

### Control Null Values

The generator learns null rates from samples:

```python
# If your sample has 10% nulls in 'phone' column,
# generated data will also have ~10% nulls
sample = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob'],
    'phone': ['555-1234', None, '555-5678']  # 33% null
})

df = generator.generate_from_sample(sample, n_rows=1000)
# phone column will have ~33% nulls
```

## 📝 Tips & Best Practices

1. **Use meaningful column names** - Better names = better auto-detection
   - ✅ `customer_email` → auto-detects as email
   - ❌ `col1` → defaults to generic text

2. **Provide samples for complex patterns** - Let the generator learn:
   ```bash
   python data_generator.py -s real_data_sample.csv -n 100000
   ```

3. **Set seed for reproducibility** in testing:
   ```bash
   python data_generator.py -c "id,name,email" --seed 42 -n 1000
   ```

4. **Use interactive mode** when exploring:
   ```bash
   python data_generator.py -i
   ```

5. **Disable preview** for large datasets:
   ```bash
   python data_generator.py -c "id,name" -n 10000000 -p 0
   ```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new data type patterns
- Improve pattern detection
- Add support for more file formats
- Enhance documentation

## 📄 License

MIT License - Feel free to use in your projects!

## 🙏 Acknowledgments

Built with:
- [Faker](https://faker.readthedocs.io/) - For generating fake data
- [Pandas](https://pandas.pydata.org/) - For data manipulation
- [NumPy](https://numpy.org/) - For numerical operations

---

**Happy Data Generating! 🚀**

For issues or questions, please open an issue on the repository.