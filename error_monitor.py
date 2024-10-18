import traceback
from flask import request, jsonify
from .client import ErrorMonitoringClient
from datetime import datetime
from werkzeug.exceptions import HTTPException

class ErrorMonitor:
    def __init__(self, app, endpoint):
        print('hello error monitor')
        self.app = app
        self.client = ErrorMonitoringClient(endpoint)
        @app.before_request
        def add_request_timestamp():
            request.timestamp = datetime.utcnow()

        self.app.register_error_handler(Exception, self.handle_exception)


    def handle_exception(self, e):
        # set default error status code
        status_code = 500

        if isinstance(e, HTTPException):
            status_code = e.code
        
        error_data = {
            'type': type(e).__name__,
            'status_code': status_code,
            'message': str(e),
            'stack_trace': traceback.format_exc(),
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers),
            'body': request.get_data(as_text=True),
            'remote_addr': request.remote_addr,
            'timestamp':  request.timestamp.isoformat()
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

        return jsonify(response), status_code
