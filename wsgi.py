"""
WSGI entry point for production servers.

Use with gunicorn:
    gunicorn wsgi:app -w 4 -b 0.0.0.0:8000

Or with uWSGI:
    uwsgi --http :8000 --module wsgi:app --processes 4
"""
import os
from app import create_app

# Get configuration from environment variable
config_name = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(config_name)
