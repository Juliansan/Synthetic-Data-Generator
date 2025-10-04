"""
Base Generator Class
Common functionality for all data generators
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
from typing import Dict, List, Optional, Any


class BaseGenerator:
    """
    Base class for all data generators
    Provides common functionality and utilities
    """
    
    def __init__(self, locale='en_US', seed=None):
        """
        Initialize the base generator
        
        Args:
            locale: Faker locale for data generation
            seed: Random seed for reproducibility
        """
        self.fake = Faker(locale)
        if seed:
            Faker.seed(seed)
            np.random.seed(seed)
            random.seed(seed)
        self.seed = seed
    
    def generate(self, n_rows: int = 100) -> pd.DataFrame:
        """
        Generate synthetic data
        
        Args:
            n_rows: Number of rows to generate
            
        Returns:
            DataFrame with generated data
            
        Note:
            This method should be overridden by subclasses
        """
        raise NotImplementedError("Subclasses must implement generate()")
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str, index: bool = False):
        """
        Save DataFrame to CSV file
        
        Args:
            df: DataFrame to save
            filepath: Output file path
            index: Whether to include index in CSV
        """
        df.to_csv(filepath, index=index)
        print(f"✅ Saved {len(df)} rows to '{filepath}'")
    
    def save_to_excel(self, df: pd.DataFrame, filepath: str, sheet_name: str = 'Sheet1'):
        """
        Save DataFrame to Excel file
        
        Args:
            df: DataFrame to save
            filepath: Output file path
            sheet_name: Name of the Excel sheet
        """
        df.to_excel(filepath, sheet_name=sheet_name, index=False)
        print(f"✅ Saved {len(df)} rows to '{filepath}'")
    
    def save_to_json(self, df: pd.DataFrame, filepath: str, orient: str = 'records'):
        """
        Save DataFrame to JSON file
        
        Args:
            df: DataFrame to save
            filepath: Output file path
            orient: JSON orientation (records, columns, index, etc.)
        """
        df.to_json(filepath, orient=orient, indent=2)
        print(f"✅ Saved {len(df)} rows to '{filepath}'")
    
    def preview(self, df: pd.DataFrame, n_rows: int = 5):
        """
        Print preview of DataFrame
        
        Args:
            df: DataFrame to preview
            n_rows: Number of rows to show
        """
        print(f"\nPreview (first {n_rows} rows):")
        print(df.head(n_rows))
        print(f"\nShape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    
    def add_nulls(self, series: pd.Series, null_rate: float = 0.1) -> pd.Series:
        """
        Add random null values to a series
        
        Args:
            series: Pandas Series to modify
            null_rate: Proportion of values to set as null (0.0 to 1.0)
            
        Returns:
            Modified Series with nulls
        """
        if null_rate <= 0:
            return series
        
        mask = np.random.random(len(series)) < null_rate
        series_copy = series.copy()
        series_copy[mask] = None
        return series_copy
    
    def generate_timestamps(
        self, 
        n_rows: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        freq: Optional[str] = None,
        sorted: bool = True
    ) -> List[datetime]:
        """
        Generate timestamp data
        
        Args:
            n_rows: Number of timestamps to generate
            start_date: Start of time range
            end_date: End of time range
            freq: Pandas frequency string for regular intervals (e.g., '1H', '5min')
            sorted: Whether to sort timestamps
            
        Returns:
            List of datetime objects
        """
        if freq:
            # Generate regular intervals
            if start_date is None:
                start_date = datetime.now() - timedelta(days=30)
            timestamps = pd.date_range(start=start_date, periods=n_rows, freq=freq).to_pydatetime().tolist()
        else:
            # Generate random timestamps
            if start_date is None:
                start_date = datetime.now() - timedelta(days=365)
            if end_date is None:
                end_date = datetime.now()
            
            timestamps = [
                self.fake.date_time_between(start_date=start_date, end_date=end_date)
                for _ in range(n_rows)
            ]
            
            if sorted:
                timestamps.sort()
        
        return timestamps
    
    def generate_ids(self, n_rows: int, prefix: str = '', start: int = 1) -> List[str]:
        """
        Generate ID values
        
        Args:
            n_rows: Number of IDs to generate
            prefix: Optional prefix for IDs
            start: Starting number
            
        Returns:
            List of ID strings
        """
        if prefix:
            return [f"{prefix}{i}" for i in range(start, start + n_rows)]
        return list(range(start, start + n_rows))
    
    def generate_categorical(
        self, 
        n_rows: int, 
        categories: List[str],
        weights: Optional[List[float]] = None
    ) -> List[str]:
        """
        Generate categorical data
        
        Args:
            n_rows: Number of values to generate
            categories: List of possible categories
            weights: Optional weights for each category
            
        Returns:
            List of category values
        """
        return random.choices(categories, weights=weights, k=n_rows)
    
    def generate_numeric(
        self,
        n_rows: int,
        min_val: float = 0,
        max_val: float = 100,
        distribution: str = 'uniform',
        decimals: Optional[int] = 2
    ) -> List[float]:
        """
        Generate numeric data
        
        Args:
            n_rows: Number of values to generate
            min_val: Minimum value
            max_val: Maximum value
            distribution: 'uniform' or 'normal'
            decimals: Number of decimal places (None for integers)
            
        Returns:
            List of numeric values
        """
        if distribution == 'normal':
            mean = (min_val + max_val) / 2
            std = (max_val - min_val) / 6
            values = np.random.normal(mean, std, n_rows)
            values = np.clip(values, min_val, max_val)
        else:  # uniform
            values = np.random.uniform(min_val, max_val, n_rows)
        
        if decimals is not None:
            values = np.round(values, decimals)
        else:
            values = values.astype(int)
        
        return values.tolist()
