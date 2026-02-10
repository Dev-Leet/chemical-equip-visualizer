import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
        
        retry = Retry(total=3, backoff_factor=0.3)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def login(self, username, password):
        response = self.session.post(
            f'{self.base_url}/auth/login/',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data['token']
            return data
        else:
            raise Exception(response.json().get('error', 'Login failed'))
    
    def upload_csv(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Token {self.token}'}
            response = self.session.post(
                f'{self.base_url}/upload/',
                files=files,
                headers=headers
            )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(response.json().get('error', 'Upload failed'))
    
    def list_datasets(self, active_only=True):
        params = {'active_only': 'true' if active_only else 'false'}
        response = self.session.get(
            f'{self.base_url}/datasets/list/',
            headers=self._get_headers(),
            params=params
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to list datasets')
    
    def get_dataset(self, dataset_id):
        response = self.session.get(
            f'{self.base_url}/datasets/{dataset_id}/',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to get dataset')
    
    def get_summary(self, dataset_id):
        response = self.session.get(
            f'{self.base_url}/summary/{dataset_id}/',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to get summary')
    
    def get_pdf_report(self, dataset_id):
        response = self.session.get(
            f'{self.base_url}/report/{dataset_id}/pdf/',
            headers={'Authorization': f'Token {self.token}'}
        )
        if response.status_code == 200:
            return response.content
        else:
            raise Exception('Failed to generate PDF')
    
    def delete_dataset(self, dataset_id):
        response = self.session.delete(
            f'{self.base_url}/datasets/{dataset_id}/delete/',
            headers=self._get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to delete dataset')