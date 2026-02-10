import configparser
import os

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        config['API'] = {
            'base_url': 'http://localhost:8000/api',
            'timeout': '30'
        }
        config['APP'] = {
            'window_width': '1280',
            'window_height': '800',
            'theme': 'light'
        }
        
        with open(config_file, 'w') as f:
            config.write(f)
    
    return config