#!/usr/bin/env python3
"""
Debug version of the web server to test Socket.IO connections
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'debug-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Socket.IO Test</title>
    </head>
    <body>
        <h1>Socket.IO Connection Test</h1>
        <div id="status">Connecting...</div>
        <div id="messages"></div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io();
            const status = document.getElementById('status');
            const messages = document.getElementById('messages');
            
            socket.on('connect', function() {
                status.innerHTML = 'Connected!';
                status.style.color = 'green';
                console.log('Connected to server');
                socket.emit('test_message', {data: 'Hello from client'});
            });
            
            socket.on('disconnect', function() {
                status.innerHTML = 'Disconnected';
                status.style.color = 'red';
                console.log('Disconnected from server');
            });
            
            socket.on('connect_error', function(error) {
                status.innerHTML = 'Connection Error: ' + error;
                status.style.color = 'red';
                console.error('Connection error:', error);
            });
            
            socket.on('test_response', function(data) {
                messages.innerHTML += '<p>Server says: ' + data.message + '</p>';
            });
        </script>
    </body>
    </html>
    '''

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('test_response', {'message': 'Welcome! Connection successful.'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('test_message')
def handle_test_message(data):
    print(f'Received test message: {data}')
    emit('test_response', {'message': 'Test message received!'})

if __name__ == '__main__':
    print("Starting debug server on http://localhost:8080")
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
