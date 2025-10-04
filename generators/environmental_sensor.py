"""
Environmental Sensor Data Generator
Generates realistic sensor data with temporal patterns and correlations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List
from .base_generator import BaseGenerator


class EnvironmentalSensorGenerator(BaseGenerator):
    """
    Generate realistic environmental sensor data
    
    Simulates sensor readings with:
    - Realistic temperature variations (daily/seasonal patterns)
    - Correlated humidity levels
    - CO2 level fluctuations
    - Optional sensor IDs and locations
    """
    
    def __init__(self, locale='en_US', seed=None):
        """
        Initialize the environmental sensor generator
        
        Args:
            locale: Faker locale for data generation
            seed: Random seed for reproducibility
        """
        super().__init__(locale, seed)
    
    def generate(
        self,
        n_rows: int = 100,
        start_date: Optional[datetime] = None,
        freq: str = '5min',
        sensor_ids: Optional[List[str]] = None,
        include_location: bool = False,
        temp_range: tuple = (15.0, 30.0),
        humidity_range: tuple = (30.0, 80.0),
        co2_range: tuple = (400, 1200),
        add_anomalies: bool = False,
        anomaly_rate: float = 0.02,
        null_config: Optional[dict] = None
    ) -> pd.DataFrame:
        """
        Generate environmental sensor data
        
        Args:
            n_rows: Number of rows to generate
            start_date: Start timestamp (default: 30 days ago)
            freq: Frequency of readings ('5min', '1H', '15min', etc.)
            sensor_ids: List of sensor IDs (default: single sensor 'SENSOR_001')
            include_location: Whether to include location data
            temp_range: Temperature range in Celsius (min, max)
            humidity_range: Humidity range in percentage (min, max)
            co2_range: CO2 range in ppm (min, max)
            add_anomalies: Whether to inject anomalous readings
            anomaly_rate: Proportion of anomalous readings (0.0 to 1.0)
            null_config: Dict with column names and their null rates
            
        Returns:
            DataFrame with environmental sensor data
        """
        if null_config is None:
            null_config = {}
        
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        
        # Generate timestamps
        timestamps = pd.date_range(start=start_date, periods=n_rows, freq=freq)
        
        # Generate sensor IDs if multiple sensors
        if sensor_ids is None:
            sensor_id_list = ['SENSOR_001'] * n_rows
        else:
            sensor_id_list = [
                sensor_ids[i % len(sensor_ids)] 
                for i in range(n_rows)
            ]
        
        # Generate temperature with daily pattern
        temperature = self._generate_temperature(
            n_rows, timestamps, temp_range, add_anomalies, anomaly_rate
        )
        
        # Generate correlated humidity
        humidity = self._generate_humidity(
            temperature, temp_range, humidity_range, add_anomalies, anomaly_rate
        )
        
        # Generate CO2 levels
        co2_level = self._generate_co2(
            n_rows, timestamps, co2_range, add_anomalies, anomaly_rate
        )
        
        # Build dataframe
        data = {
            'timestamp': timestamps,
            'sensor_id': sensor_id_list,
            'temperature': temperature,
            'humidity': humidity,
            'co2_level': co2_level
        }
        
        # Add location data if requested
        if include_location:
            if sensor_ids:
                # Generate consistent locations for each sensor
                locations = self._generate_sensor_locations(sensor_ids)
                data['location'] = [locations[sid] for sid in sensor_id_list]
            else:
                data['location'] = ['Building A - Floor 1'] * n_rows
        
        df = pd.DataFrame(data)
        
        # Apply null values based on configuration
        for column, null_rate in null_config.items():
            if column in df.columns and null_rate > 0:
                df[column] = self.add_nulls(df[column], null_rate)
        
        return df
    
    def _generate_temperature(
        self,
        n_rows: int,
        timestamps: pd.DatetimeIndex,
        temp_range: tuple,
        add_anomalies: bool,
        anomaly_rate: float
    ) -> List[float]:
        """
        Generate temperature data with daily patterns
        
        Temperature varies based on:
        - Time of day (cooler at night, warmer during day)
        - Random fluctuations
        - Optional anomalies
        """
        min_temp, max_temp = temp_range
        mean_temp = (min_temp + max_temp) / 2
        
        temperatures = []
        for i, ts in enumerate(timestamps):
            # Daily pattern: cooler at night (3-6am), warmer in afternoon (2-4pm)
            hour = ts.hour
            
            # Sinusoidal daily pattern (peak at 14:00, trough at 4:00)
            daily_variation = 0.3 * (max_temp - min_temp) * np.sin(2 * np.pi * (hour - 4) / 24)
            
            # Base temperature with daily variation
            base_temp = mean_temp + daily_variation
            
            # Add random noise
            noise = np.random.normal(0, 0.5)
            
            temp = base_temp + noise
            
            # Clip to range
            temp = np.clip(temp, min_temp, max_temp)
            
            # Add anomalies
            if add_anomalies and np.random.random() < anomaly_rate:
                temp += np.random.choice([-5, 5])  # Sudden spike or drop
                temp = np.clip(temp, min_temp - 5, max_temp + 5)
            
            temperatures.append(round(temp, 2))
        
        return temperatures
    
    def _generate_humidity(
        self,
        temperatures: List[float],
        temp_range: tuple,
        humidity_range: tuple,
        add_anomalies: bool,
        anomaly_rate: float
    ) -> List[float]:
        """
        Generate humidity data correlated with temperature
        
        Generally, humidity is inversely correlated with temperature
        """
        min_temp, max_temp = temp_range
        min_hum, max_hum = humidity_range
        
        humidities = []
        for i, temp in enumerate(temperatures):
            # Inverse correlation with temperature
            # When temp is high, humidity tends to be lower
            temp_normalized = (temp - min_temp) / (max_temp - min_temp)
            base_humidity = max_hum - (temp_normalized * (max_hum - min_hum))
            
            # Add random variation
            noise = np.random.normal(0, 5)
            humidity = base_humidity + noise
            
            # Clip to range
            humidity = np.clip(humidity, min_hum, max_hum)
            
            # Add anomalies
            if add_anomalies and np.random.random() < anomaly_rate:
                humidity += np.random.choice([-15, 15])
                humidity = np.clip(humidity, 0, 100)
            
            humidities.append(round(humidity, 2))
        
        return humidities
    
    def _generate_co2(
        self,
        n_rows: int,
        timestamps: pd.DatetimeIndex,
        co2_range: tuple,
        add_anomalies: bool,
        anomaly_rate: float
    ) -> List[int]:
        """
        Generate CO2 level data
        
        CO2 levels vary based on:
        - Time of day (higher during work hours if indoor)
        - Random fluctuations
        """
        min_co2, max_co2 = co2_range
        
        co2_levels = []
        for i, ts in enumerate(timestamps):
            hour = ts.hour
            
            # CO2 pattern: higher during work hours (8am-6pm)
            if 8 <= hour <= 18:
                # Work hours: higher CO2
                base_co2 = min_co2 + 0.6 * (max_co2 - min_co2)
            else:
                # Off hours: lower CO2
                base_co2 = min_co2 + 0.2 * (max_co2 - min_co2)
            
            # Add random variation
            noise = np.random.normal(0, 50)
            co2 = base_co2 + noise
            
            # Clip to range
            co2 = np.clip(co2, min_co2, max_co2)
            
            # Add anomalies
            if add_anomalies and np.random.random() < anomaly_rate:
                co2 += np.random.choice([-200, 300])
                co2 = np.clip(co2, min_co2 - 200, max_co2 + 500)
            
            co2_levels.append(int(co2))
        
        return co2_levels
    
    def _generate_sensor_locations(self, sensor_ids: List[str]) -> dict:
        """Generate consistent location names for sensors"""
        buildings = ['Building A', 'Building B', 'Building C']
        floors = ['Floor 1', 'Floor 2', 'Floor 3', 'Floor 4']
        rooms = ['Room 101', 'Room 102', 'Conference Room', 'Lobby', 'Lab']
        
        locations = {}
        for sid in sensor_ids:
            building = np.random.choice(buildings)
            floor = np.random.choice(floors)
            room = np.random.choice(rooms)
            locations[sid] = f"{building} - {floor} - {room}"
        
        return locations
    
    def generate_multi_sensor(
        self,
        n_sensors: int = 3,
        readings_per_sensor: int = 100,
        start_date: Optional[datetime] = None,
        freq: str = '5min',
        **kwargs
    ) -> pd.DataFrame:
        """
        Generate data from multiple sensors
        
        Args:
            n_sensors: Number of sensors to simulate
            readings_per_sensor: Number of readings per sensor
            start_date: Start timestamp
            freq: Frequency of readings
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            DataFrame with multi-sensor data
        """
        sensor_ids = [f"SENSOR_{str(i+1).zfill(3)}" for i in range(n_sensors)]
        total_rows = n_sensors * readings_per_sensor
        
        return self.generate(
            n_rows=total_rows,
            start_date=start_date,
            freq=freq,
            sensor_ids=sensor_ids,
            **kwargs
        )
