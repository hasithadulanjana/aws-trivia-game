#!/usr/bin/env python3
"""
Test script to simulate multiple players connecting
"""

import threading
import time
import socket
import json
from network_utils import send_message, receive_message

def test_client(nickname, host='localhost', port=5000):
    """Test client that connects and stays connected"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Send join message
        if not send_message(sock, {"type": "join", "nickname": nickname}):
            print(f"{nickname}: Failed to send join message")
            return
        
        print(f"{nickname}: Connected successfully")
        
        # Listen for messages
        while True:
            message = receive_message(sock)
            if not message:
                break
            print(f"{nickname}: Received {message['type']}")
            
            # Auto-start game if admin
            if message['type'] == 'admin_rights':
                time.sleep(2)  # Wait a bit
                send_message(sock, {"type": "start_game"})
                print(f"{nickname}: Started game")
            
            # Auto-answer questions
            elif message['type'] == 'question':
                time.sleep(1)  # Think time
                send_message(sock, {"type": "answer", "answer": 0})  # Always answer A
                print(f"{nickname}: Answered question")
        
    except Exception as e:
        print(f"{nickname}: Error - {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print(f"{nickname}: Disconnected")

def main():
    """Test with multiple clients"""
    print("Starting multiplayer test...")
    
    # Create multiple test clients
    clients = []
    for i in range(5):  # Test with 5 clients
        nickname = f"Player{i+1}"
        client_thread = threading.Thread(target=test_client, args=(nickname,))
        client_thread.daemon = True
        client_thread.start()
        clients.append(client_thread)
        time.sleep(0.5)  # Stagger connections
    
    # Wait for all clients
    try:
        for client in clients:
            client.join()
    except KeyboardInterrupt:
        print("Test interrupted")

if __name__ == "__main__":
    main()
