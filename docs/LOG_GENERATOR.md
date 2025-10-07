# Log Data Generator

Generate realistic job/process log entries for testing and development.

## Features

- **Multiple Output Formats**: Generate logs as DataFrames or formatted strings
- **Customizable Job Types**: Choose from predefined jobs or define your own
- **Configurable Status Distribution**: Control success/failure rates
- **Time-based Generation**: Specify date ranges and frequencies
- **Error Messages**: Include error details for failed jobs
- **Severity Levels**: Add severity indicators (INFO, WARNING, ERROR, CRITICAL)

## Quick Start

### Option 1: Python Script

```python
from generators import LogDataGenerator
from datetime import datetime

# Create generator
generator = LogDataGenerator(seed=42)

# Generate logs as strings (like your example)
logs = generator.generate_as_log_strings(
    n_rows=10,
    start_date=datetime(2025, 1, 15, 8, 0, 0),
    end_date=datetime(2025, 1, 15, 12, 0, 0),
    separator='|'
)

# Output:
# ['2025-01-15 08:00:00|customer_etl|SUCCESS|45',
#  '2025-01-15 08:15:00|sales_aggregation|FAILED|120',
#  ...]
```

### Option 2: CLI with YAML Config

```bash
# Use the pre-configured YAML file
python cli.py generate config/job_logs.yaml --preview 10

# Or create your own config (see below)
```

### Option 3: Generate as DataFrame

```python
# Generate as pandas DataFrame
df = generator.generate(
    n_rows=100,
    duration_range=(10, 300),
    include_error_message=True,
    include_severity=True
)

# Save to CSV
generator.save_to_csv(df, 'data/my_logs.csv')
```

## Configuration (YAML)

Create a YAML configuration file:

```yaml
generator: job_logs
output_file: data/job_logs.csv
rows: 500
seed: 42

settings:
  # Time range
  start_date: "2025-01-01 00:00:00"
  end_date: "2025-01-31 23:59:59"
  
  # Log frequency
  frequency: '15min'  # Options: '5min', '15min', '30min', '1H', etc.
  
  # Custom job names (optional)
  job_names:
    - custom_job_1
    - custom_job_2
  
  # Status distribution (optional)
  status_distribution:
    SUCCESS: 0.70
    FAILED: 0.15
    WARNING: 0.10
    TIMEOUT: 0.03
    CANCELLED: 0.02
  
  # Duration range in seconds
  duration:
    min: 10
    max: 300
  
  # Additional fields
  include_error_message: true
  include_severity: true
```

## Predefined Job Categories

The generator includes realistic job names across categories:

- **ETL**: `customer_etl`, `sales_etl`, `product_etl`, etc.
- **Data Processing**: `sales_aggregation`, `data_validation`, etc.
- **Sync**: `inventory_sync`, `customer_sync`, `warehouse_sync`, etc.
- **Export**: `user_export`, `sales_export`, `report_export`, etc.
- **Finance**: `payment_reconciliation`, `invoice_generation`, etc.
- **Maintenance**: `database_backup`, `log_rotation`, `cache_cleanup`, etc.

### Generate by Category

```python
# Generate only ETL job logs
df = generator.generate_by_category(
    category='ETL',
    n_rows=100
)
```

## Output Formats

### 1. Log Strings (Your Format)
```python
logs = generator.generate_as_log_strings(
    n_rows=5,
    separator='|',
    timestamp_format='%Y-%m-%d %H:%M:%S'
)
# Output: List of strings
# "2025-01-15 08:30:00|customer_etl|SUCCESS|45"
```

### 2. DataFrame with Full Details
```python
df = generator.generate(
    n_rows=100,
    include_error_message=True,
    include_severity=True
)
# Columns: timestamp, job_name, status, duration_seconds, severity, error_message
```

## Customization Examples

### Custom Job Names
```python
my_jobs = ['api_data_fetch', 'ml_model_training', 'report_generation']

logs = generator.generate_as_log_strings(
    n_rows=20,
    job_names=my_jobs
)
```

### Custom Status Distribution
```python
# More failures for testing
custom_status = {
    'SUCCESS': 0.50,
    'FAILED': 0.30,
    'WARNING': 0.15,
    'TIMEOUT': 0.05
}

df = generator.generate(
    n_rows=100,
    status_distribution=custom_status
)
```

### Time-based Logs
```python
# Generate logs for a specific time range
from datetime import datetime, timedelta

start = datetime(2025, 1, 1)
end = start + timedelta(days=7)

logs = generator.generate_as_log_strings(
    n_rows=100,
    start_date=start,
    end_date=end,
    freq='1H'  # One log per hour
)
```

## Example Scripts

Run the included example scripts:

```bash
# Simple list format (your example)
python example_log_list.py

# Full demo with all features
python demo_log_generator.py
```

## Status Types

- **SUCCESS**: Job completed successfully (default: 70%)
- **FAILED**: Job failed with error (default: 15%)
- **WARNING**: Job completed with warnings (default: 10%)
- **TIMEOUT**: Job timed out (default: 3%)
- **CANCELLED**: Job was cancelled (default: 2%)

## Error Messages (for FAILED/TIMEOUT/CANCELLED)

When `include_error_message=True`, failed jobs include realistic error messages:
- Connection timeout
- Database locked
- Out of memory
- Permission denied
- File not found
- Invalid data format
- Network error
- Disk full
- Authentication failed
- Resource unavailable
- And more...

## Generated Log Output

The generator creates the exact format you need:

```python
[
    "2025-01-15 08:30:00|customer_etl|SUCCESS|45",
    "2025-01-15 08:45:00|sales_aggregation|FAILED|120",
    "2025-01-15 09:00:00|inventory_sync|SUCCESS|30",
    "2025-01-15 09:15:00|user_export|FAILED|95",
    "2025-01-15 09:30:00|payment_reconciliation|SUCCESS|180"
]
```

Perfect for testing log parsers, monitoring systems, or data pipelines!
