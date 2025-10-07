"""
Business Data Generator
Generates realistic business and e-commerce data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List
from .base_generator import BaseGenerator


class BusinessDataGenerator(BaseGenerator):
    """
    Generate realistic business and e-commerce data
    
    Supports:
    - Customer data
    - Transaction/order data
    - Product catalogs
    - Sales data
    """
    
    def __init__(self, locale='en_US', seed=None):
        super().__init__(locale, seed)
        
        # Product categories and items
        self.products = {
            'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Headphones', 
                          'Monitor', 'Keyboard', 'Mouse', 'Camera', 'Speaker'],
            'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 
                        'Sweater', 'Shorts', 'Skirt', 'Coat', 'Sneakers'],
            'Home & Garden': ['Chair', 'Table', 'Lamp', 'Rug', 'Plant', 
                            'Desk', 'Bookshelf', 'Mirror', 'Vase', 'Cushion'],
            'Books': ['Fiction Novel', 'Business Book', 'Cookbook', 'Biography', 
                     'Self-Help', 'Science Fiction', 'Mystery', 'Romance', 'History', 'Art Book'],
            'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbell Set', 'Tennis Racket', 
                      'Basketball', 'Bicycle', 'Fitness Tracker', 'Protein Powder', 'Water Bottle', 'Gym Bag']
        }
        
        self.product_prices = {
            'Electronics': (50, 2000),
            'Clothing': (15, 200),
            'Home & Garden': (20, 500),
            'Books': (10, 50),
            'Sports': (15, 800)
        }
    
    def generate_customers(
        self,
        n_rows: int = 100,
        include_address: bool = True,
        include_signup_date: bool = True
    ) -> pd.DataFrame:
        """
        Generate customer data
        
        Args:
            n_rows: Number of customers to generate
            include_address: Whether to include address fields
            include_signup_date: Whether to include signup date
            
        Returns:
            DataFrame with customer data
        """
        data = {
            'customer_id': self.generate_ids(n_rows, prefix='CUST_'),
            'first_name': [self.fake.first_name() for _ in range(n_rows)],
            'last_name': [self.fake.last_name() for _ in range(n_rows)],
            'email': [self.fake.email() for _ in range(n_rows)],
            'phone': [self.fake.phone_number() for _ in range(n_rows)],
        }
        
        if include_address:
            data.update({
                'street_address': [self.fake.street_address() for _ in range(n_rows)],
                'city': [self.fake.city() for _ in range(n_rows)],
                'state': [self.fake.state() for _ in range(n_rows)],
                'zip_code': [self.fake.zipcode() for _ in range(n_rows)],
                'country': [self.fake.country() for _ in range(n_rows)]
            })
        
        if include_signup_date:
            data['signup_date'] = [ts.isoformat() for ts in self.generate_timestamps(
                n_rows, 
                start_date=datetime.now() - timedelta(days=730),
                end_date=datetime.now(),
                sorted=False
            )]
        
        return pd.DataFrame(data)
    
    def generate_transactions(
        self,
        n_rows: int = 100,
        n_customers: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        include_shipping: bool = True
    ) -> pd.DataFrame:
        """
        Generate transaction/order data
        
        Args:
            n_rows: Number of transactions to generate
            n_customers: Number of unique customers (default: n_rows // 3)
            start_date: Start of transaction period
            end_date: End of transaction period
            include_shipping: Whether to include shipping information
            
        Returns:
            DataFrame with transaction data
        """
        if n_customers is None:
            n_customers = max(1, n_rows // 3)
        
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        # Generate product details
        categories = []
        products = []
        prices = []
        
        for _ in range(n_rows):
            category = np.random.choice(list(self.products.keys()))
            product = np.random.choice(self.products[category])
            min_price, max_price = self.product_prices[category]
            price = round(np.random.uniform(min_price, max_price), 2)
            
            categories.append(category)
            products.append(product)
            prices.append(price)
        
        # Generate quantities and calculate totals
        quantities = np.random.randint(1, 5, n_rows).tolist()
        subtotals = [round(p * q, 2) for p, q in zip(prices, quantities)]
        
        # Generate tax and shipping
        tax_rate = 0.08  # 8% tax
        taxes = [round(s * tax_rate, 2) for s in subtotals]
        
        if include_shipping:
            shipping_costs = [round(np.random.uniform(0, 15), 2) for _ in range(n_rows)]
            totals = [round(s + t + sh, 2) for s, t, sh in zip(subtotals, taxes, shipping_costs)]
        else:
            shipping_costs = [0.0] * n_rows
            totals = [round(s + t, 2) for s, t in zip(subtotals, taxes)]
        
        data = {
            'transaction_id': self.generate_ids(n_rows, prefix='TXN_'),
            'customer_id': [f"CUST_{str(np.random.randint(1, n_customers + 1)).zfill(len(str(n_customers)))}" 
                          for _ in range(n_rows)],
            'transaction_date': self.generate_timestamps(n_rows, start_date, end_date, sorted=True),
            'product_name': products,
            'category': categories,
            'unit_price': prices,
            'quantity': quantities,
            'subtotal': subtotals,
            'tax': taxes,
            'status': self.generate_categorical(
                n_rows, 
                ['Completed', 'Pending', 'Shipped', 'Cancelled', 'Processing'],
                weights=[0.7, 0.1, 0.1, 0.05, 0.05]
            )
        }
        
        if include_shipping:
            data['shipping_cost'] = shipping_costs
        
        data['total_amount'] = totals
        
        return pd.DataFrame(data)
    
    def generate_products(
        self,
        n_rows: int = 100,
        include_inventory: bool = True
    ) -> pd.DataFrame:
        """
        Generate product catalog data
        
        Args:
            n_rows: Number of products to generate
            include_inventory: Whether to include inventory levels
            
        Returns:
            DataFrame with product data
        """
        categories = []
        products = []
        prices = []
        
        for _ in range(n_rows):
            category = np.random.choice(list(self.products.keys()))
            product = np.random.choice(self.products[category])
            min_price, max_price = self.product_prices[category]
            price = round(np.random.uniform(min_price, max_price), 2)
            
            categories.append(category)
            products.append(product)
            prices.append(price)
        
        data = {
            'product_id': self.generate_ids(n_rows, prefix='PROD_'),
            'product_name': products,
            'category': categories,
            'price': prices,
            'supplier': [self.fake.company() for _ in range(n_rows)],
            'description': [self.fake.sentence(nb_words=10) for _ in range(n_rows)]
        }
        
        if include_inventory:
            data['stock_quantity'] = np.random.randint(0, 500, n_rows).tolist()
            data['reorder_level'] = np.random.randint(10, 50, n_rows).tolist()
        
        return pd.DataFrame(data)
    
    def generate_sales_data(
        self,
        n_rows: int = 100,
        start_date: Optional[datetime] = None,
        freq: str = 'D'
    ) -> pd.DataFrame:
        """
        Generate aggregated sales data (daily/weekly/monthly)
        
        Args:
            n_rows: Number of time periods to generate
            start_date: Start date
            freq: Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
            
        Returns:
            DataFrame with sales data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        
        timestamps = pd.date_range(start=start_date, periods=n_rows, freq=freq)
        
        # Generate sales metrics
        data = {
            'date': timestamps,
            'total_revenue': self.generate_numeric(n_rows, 5000, 50000, decimals=2),
            'total_orders': np.random.randint(50, 500, n_rows).tolist(),
            'unique_customers': np.random.randint(30, 300, n_rows).tolist(),
            'avg_order_value': self.generate_numeric(n_rows, 50, 200, decimals=2),
            'total_units_sold': np.random.randint(100, 1000, n_rows).tolist()
        }
        
        return pd.DataFrame(data)
