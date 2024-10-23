import traceback
import requests
import uuid
from flask import request
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException

class ErrorMonitor:
    __endpoint = None
    __is_endpoint_set = False 

    @classmethod
    def set_endpoint(cls, endpoint):
        if not cls.__is_endpoint_set:
            cls.__endpoint = endpoint
            cls.__is_endpoint_set = True 

    def __init__(self, app, endpoint=None):
        self.project_id = str(uuid.uuid4())
        self.app = app
        self.app.register_error_handler(Exception, self.handle_exception)
        if not ErrorMonitor.__is_endpoint_set:
            self.set_endpoint(endpoint)
            
        @app.before_request
        def add_request_timestamp():
            self.timestamp = datetime.now().astimezone()

    def capture_exception(self, e):
        was_handled = True
        self.handle_exception(e, was_handled)

    def log_error(self, error_data):
        print('attempt to send error')
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(ErrorMonitor.__endpoint, json=error_data, headers=headers)
            response.raise_for_status() 
        except requests.RequestException as e:
            print(f"Failed to send error data: {e}")

    def handle_exception(self, e, was_handled=False):
        raw_error_data = {
            'name': type(e).__name__,
            'message': str(e),
            'stack': traceback.format_exc(),
        }

        data = {
            'error': raw_error_data,
            'timestamp':  self.timestamp.isoformat(),
            'handled': was_handled,
            'projectID': self.project_id
        }

        # Send error data to the monitoring service
        self.log_error(data)

        if not was_handled:
            raise e
