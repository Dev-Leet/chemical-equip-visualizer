import pandas as pd
import hashlib
from io import BytesIO

class CSVParser:
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    def parse_file(self, file):
        try:
            df = pd.read_csv(file)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")
        
        self.validate_structure(df)
        self.validate_data_types(df)
        return df
    
    def validate_structure(self, df):
        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
    
    def validate_data_types(self, df):
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    raise ValueError(f"Column '{col}' must contain numeric values")
            
            if df[col].isnull().any():
                raise ValueError(f"Column '{col}' contains invalid numeric values")
        
        if (df['Flowrate'] < 0).any() or (df['Pressure'] < 0).any():
            raise ValueError("Flowrate and Pressure must be positive values")
    
    def generate_hash(self, file):
        file.seek(0)
        content = file.read()
        file.seek(0)
        return hashlib.sha256(content).hexdigest()