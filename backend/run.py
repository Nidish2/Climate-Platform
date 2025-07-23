#!/usr/bin/env python3
"""
Climate Platform Backend Runner
"""
import os
from app import app

if __name__ == '__main__':
    # Get configuration from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"Starting Climate Platform Backend on {host}:{port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        threaded=True
    )
