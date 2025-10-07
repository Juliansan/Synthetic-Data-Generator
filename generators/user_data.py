"""
User Data Generator
Generates realistic user profile and account data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
from .base_generator import BaseGenerator


class UserDataGenerator(BaseGenerator):
    """
    Generate realistic user and account data
    
    Supports:
    - User profiles
    - Account information
    - Authentication data
    - Activity logs
    """
    
    def __init__(self, locale='en_US', seed=None):
        super().__init__(locale, seed)
    
    def generate_user_profiles(
        self,
        n_rows: int = 100,
        include_bio: bool = False,
        include_social: bool = False
    ) -> pd.DataFrame:
        """
        Generate user profile data
        
        Args:
            n_rows: Number of user profiles to generate
            include_bio: Whether to include biography/about text
            include_social: Whether to include social media links
            
        Returns:
            DataFrame with user profile data
        """
        data = {
            'user_id': self.generate_ids(n_rows, prefix='USER_'),
            'username': [self.fake.user_name() for _ in range(n_rows)],
            'email': [self.fake.email() for _ in range(n_rows)],
            'first_name': [self.fake.first_name() for _ in range(n_rows)],
            'last_name': [self.fake.last_name() for _ in range(n_rows)],
            'date_of_birth': [
                self.fake.date_of_birth(minimum_age=18, maximum_age=80)
                for _ in range(n_rows)
            ],
            'phone': [self.fake.phone_number() for _ in range(n_rows)],
            'city': [self.fake.city() for _ in range(n_rows)],
            'country': [self.fake.country() for _ in range(n_rows)],
            'account_created': self.generate_timestamps(
                n_rows,
                start_date=datetime.now() - timedelta(days=1095),
                end_date=datetime.now(),
                sorted=False
            )
        }
        
        if include_bio:
            data['bio'] = [self.fake.text(max_nb_chars=200) for _ in range(n_rows)]
        
        if include_social:
            data['website'] = [self.fake.url() for _ in range(n_rows)]
            data['twitter_handle'] = [f"@{self.fake.user_name()}" for _ in range(n_rows)]
        
        return pd.DataFrame(data)
    
    def generate_accounts(
        self,
        n_rows: int = 100,
        include_subscription: bool = True
    ) -> pd.DataFrame:
        """
        Generate account/subscription data
        
        Args:
            n_rows: Number of accounts to generate
            include_subscription: Whether to include subscription details
            
        Returns:
            DataFrame with account data
        """
        data = {
            'account_id': self.generate_ids(n_rows, prefix='ACC_'),
            'user_id': self.generate_ids(n_rows, prefix='USER_'),
            'account_type': self.generate_categorical(
                n_rows,
                ['Free', 'Basic', 'Premium', 'Enterprise'],
                weights=[0.5, 0.25, 0.15, 0.1]
            ),
            'status': self.generate_categorical(
                n_rows,
                ['Active', 'Inactive', 'Suspended', 'Pending'],
                weights=[0.8, 0.1, 0.05, 0.05]
            ),
            'created_date': self.generate_timestamps(
                n_rows,
                start_date=datetime.now() - timedelta(days=730),
                end_date=datetime.now(),
                sorted=False
            )
        }
        
        if include_subscription:
            data['subscription_start'] = self.generate_timestamps(
                n_rows,
                start_date=datetime.now() - timedelta(days=365),
                end_date=datetime.now(),
                sorted=False
            )
            data['subscription_end'] = [
                start + timedelta(days=np.random.choice([30, 90, 365]))
                for start in data['subscription_start']
            ]
            data['monthly_fee'] = self.generate_categorical(
                n_rows,
                ['0', '9.99', '19.99', '99.99'],
                weights=[0.5, 0.25, 0.15, 0.1]
            )
        
        return pd.DataFrame(data)
    
    def generate_login_activity(
        self,
        n_rows: int = 100,
        n_users: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Generate login activity logs
        
        Args:
            n_rows: Number of login events to generate
            n_users: Number of unique users (default: n_rows // 5)
            start_date: Start of activity period
            end_date: End of activity period
            
        Returns:
            DataFrame with login activity data
        """
        if n_users is None:
            n_users = max(1, n_rows // 5)
        
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()
        
        data = {
            'log_id': self.generate_ids(n_rows, prefix='LOG_'),
            'user_id': [
                f"USER_{str(np.random.randint(1, n_users + 1)).zfill(len(str(n_users)))}"
                for _ in range(n_rows)
            ],
            'login_timestamp': self.generate_timestamps(
                n_rows, start_date, end_date, sorted=True
            ),
            'ip_address': [self.fake.ipv4() for _ in range(n_rows)],
            'device': self.generate_categorical(
                n_rows,
                ['Desktop', 'Mobile', 'Tablet'],
                weights=[0.5, 0.4, 0.1]
            ),
            'browser': self.generate_categorical(
                n_rows,
                ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera'],
                weights=[0.5, 0.2, 0.15, 0.1, 0.05]
            ),
            'os': self.generate_categorical(
                n_rows,
                ['Windows', 'macOS', 'Linux', 'iOS', 'Android'],
                weights=[0.4, 0.25, 0.05, 0.15, 0.15]
            ),
            'login_success': self.generate_categorical(
                n_rows,
                ['True', 'False'],
                weights=[0.95, 0.05]
            )
        }
        
        return pd.DataFrame(data)
    
    def generate_user_preferences(
        self,
        n_rows: int = 100
    ) -> pd.DataFrame:
        """
        Generate user preferences/settings data
        
        Args:
            n_rows: Number of preference records to generate
            
        Returns:
            DataFrame with user preferences data
        """
        data = {
            'user_id': self.generate_ids(n_rows, prefix='USER_'),
            'language': self.generate_categorical(
                n_rows,
                ['en', 'es', 'fr', 'de', 'ja', 'zh'],
                weights=[0.5, 0.15, 0.1, 0.1, 0.08, 0.07]
            ),
            'timezone': self.generate_categorical(
                n_rows,
                ['UTC', 'EST', 'PST', 'CST', 'GMT', 'JST'],
                weights=[0.15, 0.25, 0.25, 0.15, 0.1, 0.1]
            ),
            'theme': self.generate_categorical(
                n_rows,
                ['light', 'dark', 'auto'],
                weights=[0.4, 0.4, 0.2]
            ),
            'email_notifications': self.generate_categorical(
                n_rows,
                ['True', 'False'],
                weights=[0.7, 0.3]
            ),
            'push_notifications': self.generate_categorical(
                n_rows,
                ['True', 'False'],
                weights=[0.6, 0.4]
            ),
            'privacy_mode': self.generate_categorical(
                n_rows,
                ['public', 'friends', 'private'],
                weights=[0.3, 0.4, 0.3]
            )
        }
        
        return pd.DataFrame(data)
