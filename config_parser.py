"""
YAML Configuration Parser
Loads and validates YAML configuration files for data generation
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigParser:
    """Parse and validate YAML configuration files"""
    
    VALID_GENERATORS = [
        'environmental_sensor',
        'business_customers',
        'business_transactions',
        'business_products',
        'business_sales',
        'user_profiles',
        'user_accounts',
        'user_activity',
        'user_preferences'
    ]
    
    def __init__(self, config_path: str):
        """
        Initialize config parser
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config = None
        self._load()
    
    def _load(self):
        """Load YAML configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self._validate()
    
    def _validate(self):
        """Validate configuration structure"""
        if not self.config:
            raise ValueError("Configuration file is empty")
        
        # Check required fields
        required_fields = ['generator', 'output_file', 'rows']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate generator type
        if self.config['generator'] not in self.VALID_GENERATORS:
            raise ValueError(
                f"Invalid generator: {self.config['generator']}. "
                f"Valid options: {', '.join(self.VALID_GENERATORS)}"
            )
        
        # Validate rows
        if not isinstance(self.config['rows'], int) or self.config['rows'] <= 0:
            raise ValueError("'rows' must be a positive integer")
    
    def get_generator_type(self) -> str:
        """Get the generator type"""
        return self.config['generator']
    
    def get_output_file(self) -> str:
        """Get output file path"""
        return self.config['output_file']
    
    def get_rows(self) -> int:
        """Get number of rows to generate"""
        return self.config['rows']
    
    def get_seed(self) -> Optional[int]:
        """Get random seed"""
        return self.config.get('seed')
    
    def get_settings(self) -> Dict[str, Any]:
        """Get generator-specific settings"""
        return self.config.get('settings', {})
    
    def get_column_config(self, column_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific column
        
        Args:
            column_name: Name of the column
            
        Returns:
            Dict with nullable and null_rate settings
        """
        settings = self.get_settings()
        columns_config = settings.get('columns', {})
        
        if column_name in columns_config:
            return columns_config[column_name]
        
        return {'nullable': False, 'null_rate': 0.0}
    
    def is_column_nullable(self, column_name: str) -> bool:
        """Check if a column can have null values"""
        config = self.get_column_config(column_name)
        return config.get('nullable', False)
    
    def get_null_rate(self, column_name: str) -> float:
        """Get null rate for a column"""
        config = self.get_column_config(column_name)
        return config.get('null_rate', 0.0)
    
    def parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
        
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}. Use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'")
    
    def __repr__(self) -> str:
        return f"ConfigParser(generator={self.get_generator_type()}, rows={self.get_rows()})"


def load_config(config_path: str) -> ConfigParser:
    """
    Convenience function to load a configuration file
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        ConfigParser instance
    """
    return ConfigParser(config_path)
