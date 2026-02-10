import pandas as pd
import numpy as np

class DataAnalyzer:
    def compute_statistics(self, df):
        return {
            'total_count': int(len(df)),
            'avg_flowrate': float(df['Flowrate'].mean()),
            'avg_pressure': float(df['Pressure'].mean()),
            'avg_temperature': float(df['Temperature'].mean()),
            'min_flowrate': float(df['Flowrate'].min()),
            'max_flowrate': float(df['Flowrate'].max()),
            'min_pressure': float(df['Pressure'].min()),
            'max_pressure': float(df['Pressure'].max()),
            'min_temperature': float(df['Temperature'].min()),
            'max_temperature': float(df['Temperature'].max()),
        }
    
    def get_type_distribution(self, df):
        type_counts = df['Type'].value_counts()
        total = len(df)
        
        distribution = []
        for eq_type, count in type_counts.items():
            distribution.append({
                'equipment_type': eq_type,
                'count': int(count),
                'percentage': round((int(count) / total) * 100, 2)
            })
        return distribution
    
    def get_type_statistics(self, df, equipment_type):
        type_df = df[df['Type'] == equipment_type]
        return {
            'avg_flowrate': float(type_df['Flowrate'].mean()),
            'avg_pressure': float(type_df['Pressure'].mean()),
            'avg_temperature': float(type_df['Temperature'].mean()),
        }