#!/usr/bin/env python3
"""
Simple example: Generate logs as a Python list
This matches the format from your example:
    "2025-01-15 08:30:00|customer_etl|SUCCESS|45"
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from generators import LogDataGenerator
from datetime import datetime


def main():
    # Create the generator
    generator = LogDataGenerator(seed=42)
    
    # Generate logs as formatted strings
    log_list = generator.generate_as_log_strings(
        n_rows=10,
        start_date=datetime(2025, 1, 15, 8, 0, 0),
        end_date=datetime(2025, 1, 15, 12, 0, 0),
        separator='|',
        timestamp_format='%Y-%m-%d %H:%M:%S'
    )
    
    # Print as Python list
    print("Generated Log List:")
    print(log_list)
    
    print("\nFormatted output:")
    for log in log_list:
        print(f'    "{log}",')


if __name__ == '__main__':
    main()
