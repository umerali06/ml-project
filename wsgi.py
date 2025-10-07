#!/usr/bin/python3
"""
WSGI entry point for production deployment
Supports both development and production environments
"""
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask application
from app import app as application

if __name__ == "__main__":
    # This should not be reached in production WSGI deployment
    # but useful for testing
    application.run()
