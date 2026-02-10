import os

def validate_csv_file(file_path):
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    if not file_path.endswith('.csv'):
        return False, "Only CSV files are allowed"
    
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:
        return False, "File size must be less than 10MB"
    
    return True, "Valid"