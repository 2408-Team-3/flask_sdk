import requests
import uuid

class ErrorMonitoringClient:
    def __init__(self, endpoint):
        self.id = str(uuid.uuid4())
        self.endpoint = endpoint

    def send_error(self, error_data):
        print('attempt to send error')
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(self.endpoint, json=error_data, headers=headers)
            response.raise_for_status() 
        except requests.RequestException as e:
            print(f"Failed to send error data: {e}")
