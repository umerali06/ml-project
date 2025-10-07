#!/usr/bin/env python3
"""
Startup script for Flask ML Application
Supports development, production, and testing modes
"""
import os
import sys
from pathlib import Path

def load_env_file(env_file):
    """Load environment variables from file"""
    if Path(env_file).exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def main():
    """Main startup function"""
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Load environment file if it exists
    env_file = f'env.{env}'
    load_env_file(env_file)
    
    # Import and run the application
    from app import app
    
    print(f"🚀 Starting Flask ML App in {env.upper()} mode")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🐛 Debug mode: {os.environ.get('FLASK_DEBUG', 'false')}")
    
    # Get configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1' if env == 'development' else '0.0.0.0')
    
    print(f"🌐 Server: http://{host}:{port}")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=debug_mode)

if __name__ == '__main__':
    main()
