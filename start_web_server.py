#!/usr/bin/env python3
"""
Simple startup script for the web server
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_server import app, socketio

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 AWS Trivia Game Web Server Starting...")
    print("=" * 50)
    print("📱 Access the game at: http://localhost:8080")
    print("🌐 Or from other devices: http://YOUR_IP:8080")
    print("=" * 50)
    
    try:
        socketio.run(app, host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
