"""
Log Data Generator
Generates realistic system/job log entries
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from .base_generator import BaseGenerator


class LogDataGenerator(BaseGenerator):
    """
    Generate realistic system/job log entries
    
    Supports:
    - Job/process logs
    - ETL pipeline logs
    - Batch job logs
    - System task logs
    """
    
    def __init__(self, locale='en_US', seed=None):
        super().__init__(locale, seed)
        
        # Default job names for different categories
        self.job_categories = {
            'ETL': [
                'customer_etl', 'sales_etl', 'product_etl', 'inventory_etl',
                'user_data_etl', 'order_etl', 'analytics_etl', 'report_etl'
            ],
            'Data Processing': [
                'sales_aggregation', 'revenue_calculation', 'data_validation',
                'data_cleaning', 'data_transformation', 'data_enrichment'
            ],
            'Sync': [
                'inventory_sync', 'customer_sync', 'product_sync', 'order_sync',
                'warehouse_sync', 'crm_sync', 'erp_sync'
            ],
            'Export': [
                'user_export', 'sales_export', 'report_export', 'analytics_export',
                'audit_export', 'backup_export', 'data_export'
            ],
            'Finance': [
                'payment_reconciliation', 'invoice_generation', 'payroll_processing',
                'tax_calculation', 'billing_sync', 'financial_reporting'
            ],
            'Maintenance': [
                'database_backup', 'log_rotation', 'cache_cleanup', 'index_rebuild',
                'system_health_check', 'security_scan', 'performance_monitoring'
            ]
        }
        
        # Flatten all job names
        self.all_jobs = [job for category in self.job_categories.values() for job in category]
        
        # Status types with weights (more success than failures)
        self.status_types = ['SUCCESS', 'FAILED', 'WARNING', 'TIMEOUT', 'CANCELLED']
        self.status_weights = [0.70, 0.15, 0.10, 0.03, 0.02]  # 70% success rate
    
    def generate(
        self,
        n_rows: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        freq: str = '15min',
        job_names: Optional[List[str]] = None,
        status_distribution: Optional[Dict[str, float]] = None,
        duration_range: tuple = (10, 300),
        include_error_message: bool = False,
        include_severity: bool = False
    ) -> pd.DataFrame:
        """
        Generate log data
        
        Args:
            n_rows: Number of log entries to generate
            start_date: Start date for log timestamps (default: 30 days ago)
            end_date: End date for log timestamps (default: now)
            freq: Frequency of log entries (e.g., '15min', '1H', '30min')
            job_names: Custom list of job names (default: uses predefined jobs)
            status_distribution: Custom distribution of statuses {status: weight}
            duration_range: Tuple of (min, max) duration in seconds
            include_error_message: Include error message column for failed jobs
            include_severity: Include severity level (INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            DataFrame with log data
        """
        # Set date range
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Generate timestamps
        timestamps = pd.date_range(start=start_date, end=end_date, periods=n_rows)
        
        # Select job names
        jobs = job_names if job_names else self.all_jobs
        
        # Determine status weights
        if status_distribution:
            statuses = list(status_distribution.keys())
            weights = list(status_distribution.values())
        else:
            statuses = self.status_types
            weights = self.status_weights
        
        # Generate data
        data = {
            'timestamp': timestamps,
            'job_name': np.random.choice(jobs, n_rows),
            'status': np.random.choice(statuses, n_rows, p=weights),
            'duration_seconds': np.random.randint(duration_range[0], duration_range[1] + 1, n_rows)
        }
        
        df = pd.DataFrame(data)
        
        # Add severity based on status
        if include_severity:
            severity_map = {
                'SUCCESS': 'INFO',
                'WARNING': 'WARNING',
                'FAILED': 'ERROR',
                'TIMEOUT': 'ERROR',
                'CANCELLED': 'WARNING'
            }
            df['severity'] = df['status'].map(severity_map)
        
        # Add error messages for failed jobs
        if include_error_message:
            error_messages = [
                'Connection timeout',
                'Database locked',
                'Out of memory',
                'Permission denied',
                'File not found',
                'Invalid data format',
                'Network error',
                'Disk full',
                'Authentication failed',
                'Resource unavailable',
                'Data validation failed',
                'Deadlock detected',
                'Query timeout',
                'Service unavailable',
                'Rate limit exceeded'
            ]
            
            def generate_error_msg(row):
                if row['status'] in ['FAILED', 'TIMEOUT', 'CANCELLED']:
                    return np.random.choice(error_messages)
                return None
            
            df['error_message'] = df.apply(generate_error_msg, axis=1)
        
        return df
    
    def generate_as_log_strings(
        self,
        n_rows: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        freq: str = '15min',
        job_names: Optional[List[str]] = None,
        status_distribution: Optional[Dict[str, float]] = None,
        duration_range: tuple = (10, 300),
        separator: str = '|',
        timestamp_format: str = '%Y-%m-%d %H:%M:%S'
    ) -> List[str]:
        """
        Generate log data as formatted strings (like your example)
        
        Args:
            n_rows: Number of log entries to generate
            start_date: Start date for log timestamps
            end_date: End date for log timestamps
            freq: Frequency of log entries
            job_names: Custom list of job names
            status_distribution: Custom distribution of statuses
            duration_range: Tuple of (min, max) duration in seconds
            separator: Character to separate fields (default: '|')
            timestamp_format: Format for timestamp string
            
        Returns:
            List of formatted log strings
        """
        # Generate DataFrame
        df = self.generate(
            n_rows=n_rows,
            start_date=start_date,
            end_date=end_date,
            freq=freq,
            job_names=job_names,
            status_distribution=status_distribution,
            duration_range=duration_range,
            include_error_message=False,
            include_severity=False
        )
        
        # Convert to formatted strings
        log_strings = []
        for _, row in df.iterrows():
            timestamp_str = row['timestamp'].strftime(timestamp_format)
            log_entry = f"{timestamp_str}{separator}{row['job_name']}{separator}{row['status']}{separator}{row['duration_seconds']}"
            log_strings.append(log_entry)
        
        return log_strings
    
    def generate_by_category(
        self,
        category: str,
        n_rows: int = 100,
        **kwargs
    ) -> pd.DataFrame:
        """
        Generate logs for a specific job category
        
        Args:
            category: Job category ('ETL', 'Data Processing', 'Sync', 'Export', 'Finance', 'Maintenance')
            n_rows: Number of log entries
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            DataFrame with log data for the specified category
        """
        if category not in self.job_categories:
            raise ValueError(f"Unknown category: {category}. Available: {list(self.job_categories.keys())}")
        
        job_names = self.job_categories[category]
        return self.generate(n_rows=n_rows, job_names=job_names, **kwargs)
