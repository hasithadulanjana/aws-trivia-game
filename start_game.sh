#!/bin/bash

echo "🚀 Starting AWS Trivia Game Web Server..."
echo "=================================="

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "🌐 Server will be available at:"
echo "   Local:   http://localhost:8080"
echo "   Network: http://$(ipconfig getifaddr en0):8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

python3 web_server.py
