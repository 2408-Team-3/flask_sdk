import traceback
from flask import request, make_response
from .client import ErrorMonitoringClient
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException

class ErrorMonitor:
    def __init__(self, app, endpoint):
        print('hello error monitor')
        self.app = app
        self.client = ErrorMonitoringClient(endpoint)
        @app.before_request
        def add_request_timestamp():
            request.timestamp = datetime.now(timezone.utc)

        self.app.register_error_handler(Exception, self.handle_exception)

    def handle_exception(self, e):
        # set default error status code
        status_code = 500

        if isinstance(e, HTTPException):
            status_code = e.code
        
        raw_error_data = {
            'type': type(e).__name__,  # Exception class name
            'message': str(e),  # Exception message
            'args': e.args,  # Exception arguments
            'stack_trace': traceback.format_exc(),  # Full stack trace
        }

        error_data = {
            'error': raw_error_data,
            'timestamp':  request.timestamp.isoformat(),
            'method': request.method,
            'status_code': status_code
        }

        # Send error data to the monitoring service
        self.client.send_error(error_data)
        # if self.app.handle_exception:
        #     self.app.handle_exception(e)

        response = {
            "error": str(e),
            "stack_trace": traceback.format_exc(),
            "timestamp": request.timestamp.isoformat(),
            'method': request.method,
            'headers': dict(request.headers),
            'body': request.get_data(as_text=True),
            'remote_addr': request.remote_addr,
        }

        raise e
