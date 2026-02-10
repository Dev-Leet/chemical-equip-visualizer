import pandas as pd

class DataAnalyzer:
    def compute_statistics(self, df):
        return {
            'total_count': len(df),
            'avg_flowrate': df['Flowrate'].mean(),
            'avg_pressure': df['Pressure'].mean(),
            'avg_temperature': df['Temperature'].mean(),
            'min_flowrate': df['Flowrate'].min(),
            'max_flowrate': df['Flowrate'].max(),
            'min_pressure': df['Pressure'].min(),
            'max_pressure': df['Pressure'].max(),
            'min_temperature': df['Temperature'].min(),
            'max_temperature': df['Temperature'].max(),
        }
    
    def get_type_distribution(self, df):
        type_counts = df['Type'].value_counts()
        total = len(df)
        
        distribution = []
        for eq_type, count in type_counts.items():
            distribution.append({
                'equipment_type': eq_type,
                'count': int(count),
                'percentage': round((count / total) * 100, 2)
            })
        return distribution
    
    def get_type_statistics(self, df, equipment_type):
        type_df = df[df['Type'] == equipment_type]
        return {
            'avg_flowrate': type_df['Flowrate'].mean(),
            'avg_pressure': type_df['Pressure'].mean(),
            'avg_temperature': type_df['Temperature'].mean(),
        }