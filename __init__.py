# __init__.py
from .error_monitor import ErrorMonitor

def init_app(app, endpoint):
    ErrorMonitor(app, endpoint)
