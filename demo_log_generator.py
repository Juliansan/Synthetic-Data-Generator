#!/usr/bin/env python3
"""
Demo script for the Log Data Generator
Shows how to use the LogDataGenerator to create log entries
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from generators import LogDataGenerator
from datetime import datetime


def demo_log_strings():
    """Demo: Generate logs as formatted strings (like your example)"""
    print("=" * 80)
    print("DEMO 1: Generate Log Strings (Your Example Format)")
    print("=" * 80)
    
    generator = LogDataGenerator(seed=42)
    
    # Generate logs as strings
    log_strings = generator.generate_as_log_strings(
        n_rows=10,
        start_date=datetime(2025, 1, 15, 8, 0, 0),
        end_date=datetime(2025, 1, 15, 12, 0, 0),
        separator='|',
        timestamp_format='%Y-%m-%d %H:%M:%S'
    )
    
    print("\nGenerated Log Strings:")
    print("-" * 80)
    for log in log_strings:
        print(log)
    
    print("\n✓ Generated as Python list:")
    print(log_strings[:5])  # Show first 5 as list


def demo_dataframe():
    """Demo: Generate logs as DataFrame"""
    print("\n" + "=" * 80)
    print("DEMO 2: Generate Logs as DataFrame")
    print("=" * 80)
    
    generator = LogDataGenerator(seed=42)
    
    # Generate logs as DataFrame
    df = generator.generate(
        n_rows=20,
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 1, 31),
        duration_range=(10, 300),
        include_error_message=True,
        include_severity=True
    )
    
    print("\nDataFrame Preview:")
    print("-" * 80)
    print(df.head(10))
    
    print(f"\nDataFrame Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")


def demo_by_category():
    """Demo: Generate logs for specific job category"""
    print("\n" + "=" * 80)
    print("DEMO 3: Generate Logs by Job Category")
    print("=" * 80)
    
    generator = LogDataGenerator(seed=42)
    
    # Generate ETL job logs only
    df = generator.generate_by_category(
        category='ETL',
        n_rows=15,
        start_date=datetime(2025, 1, 15),
        duration_range=(30, 180)
    )
    
    print("\nETL Jobs Only:")
    print("-" * 80)
    print(df.head(10))
    
    print("\nUnique Jobs:")
    print(df['job_name'].unique())


def demo_custom_jobs():
    """Demo: Generate logs with custom job names"""
    print("\n" + "=" * 80)
    print("DEMO 4: Generate Logs with Custom Job Names")
    print("=" * 80)
    
    generator = LogDataGenerator(seed=42)
    
    # Custom job names
    my_jobs = [
        'api_data_fetch',
        'ml_model_training',
        'report_generation',
        'cache_update'
    ]
    
    # Custom status distribution (more failures for demo)
    custom_status = {
        'SUCCESS': 0.50,
        'FAILED': 0.30,
        'WARNING': 0.15,
        'TIMEOUT': 0.05
    }
    
    df = generator.generate(
        n_rows=12,
        job_names=my_jobs,
        status_distribution=custom_status,
        duration_range=(5, 120),
        include_error_message=True
    )
    
    print("\nCustom Jobs with More Failures:")
    print("-" * 80)
    print(df)
    
    print("\nStatus Distribution:")
    print(df['status'].value_counts())


def demo_save_to_file():
    """Demo: Generate and save logs to CSV"""
    print("\n" + "=" * 80)
    print("DEMO 5: Generate and Save to CSV")
    print("=" * 80)
    
    generator = LogDataGenerator(seed=42)
    
    df = generator.generate(
        n_rows=100,
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 1, 31),
        include_error_message=True,
        include_severity=True
    )
    
    # Save to CSV
    output_file = 'data/demo_job_logs.csv'
    generator.save_to_csv(df, output_file)
    
    print(f"\n✓ Saved {len(df)} log entries to '{output_file}'")


if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "LOG DATA GENERATOR DEMO" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Run all demos
    demo_log_strings()
    demo_dataframe()
    demo_by_category()
    demo_custom_jobs()
    demo_save_to_file()
    
    print("\n" + "=" * 80)
    print("✓ All demos completed successfully!")
    print("=" * 80)
    print()
