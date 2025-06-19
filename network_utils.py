#!/usr/bin/env python3
"""
Network utilities for reliable message transmission
"""

import json
import struct
import socket

def send_message(sock, message):
    """Send a JSON message with length prefix"""
    try:
        # Convert message to JSON bytes
        message_bytes = json.dumps(message).encode('utf-8')
        # Send length first (4 bytes)
        length = struct.pack('!I', len(message_bytes))
        sock.sendall(length + message_bytes)
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def receive_message(sock):
    """Receive a JSON message with length prefix"""
    try:
        # First, receive the length (4 bytes)
        length_bytes = receive_all(sock, 4)
        if not length_bytes:
            return None
        
        # Unpack the length
        length = struct.unpack('!I', length_bytes)[0]
        
        # Now receive the actual message
        message_bytes = receive_all(sock, length)
        if not message_bytes:
            return None
            
        # Parse JSON
        return json.loads(message_bytes.decode('utf-8'))
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

def receive_all(sock, n):
    """Helper function to receive exactly n bytes"""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
