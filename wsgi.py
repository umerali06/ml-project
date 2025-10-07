#!/usr/bin/python3
"""
WSGI entry point for Hostinger deployment
"""
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Import the Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
