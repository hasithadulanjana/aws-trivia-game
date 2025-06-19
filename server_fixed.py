#!/usr/bin/env python3
"""
AWS Trivia Game Server - Fixed Version
Handles multiple client connections reliably
"""

import socket
import threading
import json
import time
import random
import signal
import sys
from questions import questions
from network_utils import send_message, receive_message

# Game configuration
HOST = '0.0.0.0'
PORT = 5000
MAX_PLAYERS = 10
QUESTION_TIMEOUT = 15
WAIT_TIME_BETWEEN_QUESTIONS = 3

class TriviaBroadcaster:
    """Manages broadcasting messages to all connected clients"""
    
    def __init__(self):
        self.clients = {}  # {client_socket: nickname}
        self.scores = {}   # {nickname: score}
        self.lock = threading.RLock()  # Use RLock for nested locking
        
    def add_client(self, client_socket, nickname):
        """Add a new client to the broadcaster"""
        with self.lock:
            # Check for duplicate nicknames
            if nickname in self.scores:
                return False
            self.clients[client_socket] = nickname
            self.scores[nickname] = 0
            return True
            
    def remove_client(self, client_socket):
        """Remove a client from the broadcaster"""
        with self.lock:
            if client_socket in self.clients:
                nickname = self.clients[client_socket]
                del self.clients[client_socket]
                if nickname in self.scores:
                    del self.scores[nickname]
                return nickname
            return None
                
    def broadcast(self, message, exclude=None):
        """Send a message to all connected clients except excluded ones"""
        with self.lock:
            disconnected = []
            clients_copy = list(self.clients.keys())  # Create a copy to avoid modification during iteration
            
            for client_socket in clients_copy:
                if client_socket != exclude:
                    if not send_message(client_socket, message):
                        disconnected.append(client_socket)
            
            # Clean up disconnected clients
            for client_socket in disconnected:
                self.remove_client(client_socket)
                
    def update_score(self, nickname, points=1):
        """Update a player's score"""
        with self.lock:
            if nickname in self.scores:
                self.scores[nickname] += points
                
    def get_leaderboard(self):
        """Get the current leaderboard sorted by score"""
        with self.lock:
            return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
            
    def get_player_count(self):
        """Get the current number of connected players"""
        with self.lock:
            return len(self.clients)
    
    def get_client_by_nickname(self, nickname):
        """Get client socket by nickname"""
        with self.lock:
            for client_socket, nick in self.clients.items():
                if nick == nickname:
                    return client_socket
            return None


class TriviaServer:
    """Main server class that manages the game"""
    
    def __init__(self):
        self.server_socket = None
        self.broadcaster = TriviaBroadcaster()
        self.game_in_progress = False
        self.accepting_players = True
        self.current_question_index = 0
        self.answered_current_question = set()
        self.question_timer = None
        self.game_questions = []
        self.server_lock = threading.Lock()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
    def start(self):
        """Start the trivia server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(MAX_PLAYERS)
            print(f"Server started on {HOST}:{PORT}")
            print("Waiting for players to connect...")
            
            # Prepare questions (shuffle them)
            self.game_questions = random.sample(questions, min(len(questions), 20))  # Limit to 20 questions
            
            # Accept client connections
            while self.accepting_players:
                try:
                    client_socket, addr = self.server_socket.accept()
                    
                    with self.server_lock:
                        if self.broadcaster.get_player_count() >= MAX_PLAYERS:
                            # Reject connection if max players reached
                            send_message(client_socket, {
                                "type": "error",
                                "message": "Game is full. Try again later."
                            })
                            client_socket.close()
                            continue
                    
                    print(f"New connection from {addr}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    if self.accepting_players:
                        print("Socket error occurred")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.shutdown()
            
    def handle_client(self, client_socket, addr):
        """Handle communication with a client"""
        nickname = None
        
        try:
            # Set socket timeout to prevent hanging
            client_socket.settimeout(30.0)
            
            # First message should be the nickname
            message = receive_message(client_socket)
            if not message:
                return
            
            if message["type"] == "join":
                nickname = message["nickname"]
                
                # Validate nickname
                if not nickname or len(nickname.strip()) == 0:
                    send_message(client_socket, {
                        "type": "error",
                        "message": "Invalid nickname"
                    })
                    return
                
                nickname = nickname.strip()[:20]  # Limit nickname length
                
                if not self.broadcaster.add_client(client_socket, nickname):
                    send_message(client_socket, {
                        "type": "error",
                        "message": "Nickname already taken"
                    })
                    return
                
                print(f"Player {nickname} joined from {addr}")
                
                # Notify all clients about the new player
                self.broadcaster.broadcast({
                    "type": "player_joined",
                    "nickname": nickname,
                    "player_count": self.broadcaster.get_player_count()
                })
                
                # If this is the first player, give them admin controls
                if self.broadcaster.get_player_count() == 1:
                    send_message(client_socket, {
                        "type": "admin_rights",
                        "message": "You are the host. Type 'start' to begin the game."
                    })
                else:
                    send_message(client_socket, {
                        "type": "wait_message",
                        "message": "Waiting for the host to start the game..."
                    })
                
                # Remove timeout for game communication
                client_socket.settimeout(None)
                
                # Main client communication loop
                while True:
                    message = receive_message(client_socket)
                    if not message:
                        break
                    
                    if message["type"] == "start_game":
                        with self.server_lock:
                            if not self.game_in_progress and self.broadcaster.get_player_count() >= 1:
                                self.game_in_progress = True
                                self.accepting_players = False
                                game_thread = threading.Thread(target=self.run_game)
                                game_thread.daemon = True
                                game_thread.start()
                    
                    elif message["type"] == "answer" and self.game_in_progress:
                        self.process_answer(client_socket, nickname, message["answer"])
            
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            if nickname:
                print(f"Client {nickname} disconnected")
                self.broadcaster.broadcast({
                    "type": "player_left",
                    "nickname": nickname,
                    "player_count": max(0, self.broadcaster.get_player_count() - 1)
                })
            self.broadcaster.remove_client(client_socket)
            try:
                client_socket.close()
            except:
                pass
            
    def process_answer(self, client_socket, nickname, answer_index):
        """Process a player's answer to the current question"""
        if client_socket in self.answered_current_question:
            return  # Player already answered this question
            
        if self.current_question_index <= 0 or self.current_question_index > len(self.game_questions):
            return  # Invalid question index
            
        current_question = self.game_questions[self.current_question_index - 1]
        correct = answer_index == current_question["answer"]
        
        if correct:
            self.broadcaster.update_score(nickname)
            
        # Mark this client as having answered
        self.answered_current_question.add(client_socket)
        
        # Send feedback to the player
        send_message(client_socket, {
            "type": "answer_feedback",
            "correct": correct,
            "correct_answer": current_question["answer"]
        })
        
        # If all players have answered, move to the next question
        if len(self.answered_current_question) == self.broadcaster.get_player_count():
            if self.question_timer:
                self.question_timer.cancel()
            self.send_leaderboard()
            time.sleep(WAIT_TIME_BETWEEN_QUESTIONS)
            self.next_question()
            
    def run_game(self):
        """Run the trivia game"""
        self.broadcaster.broadcast({
            "type": "game_starting",
            "message": "Game is starting!",
            "player_count": self.broadcaster.get_player_count()
        })
        
        time.sleep(2)
        self.current_question_index = 0
        self.next_question()
        
    def next_question(self):
        """Send the next question to all clients"""
        if self.current_question_index >= len(self.game_questions):
            self.end_game()
            return
            
        # Reset the set of clients who have answered
        self.answered_current_question = set()
        
        current_question = self.game_questions[self.current_question_index]
        
        # Send the question to all clients
        self.broadcaster.broadcast({
            "type": "question",
            "question_number": self.current_question_index + 1,
            "total_questions": len(self.game_questions),
            "question": current_question["question"],
            "options": current_question["options"],
            "timeout": QUESTION_TIMEOUT
        })
        
        # Set a timer to move to the next question after the timeout
        self.question_timer = threading.Timer(QUESTION_TIMEOUT, self.handle_question_timeout)
        self.question_timer.start()
        
        self.current_question_index += 1
        
    def handle_question_timeout(self):
        """Handle timeout for the current question"""
        if self.current_question_index <= 0 or self.current_question_index > len(self.game_questions):
            return
            
        # Send the correct answer to all clients
        current_question = self.game_questions[self.current_question_index - 1]
        self.broadcaster.broadcast({
            "type": "timeout",
            "correct_answer": current_question["answer"]
        })
        
        # Send the current leaderboard
        self.send_leaderboard()
        
        # Wait a bit before sending the next question
        time.sleep(WAIT_TIME_BETWEEN_QUESTIONS)
        
        # Move to the next question
        self.next_question()
        
    def send_leaderboard(self):
        """Send the current leaderboard to all clients"""
        leaderboard = self.broadcaster.get_leaderboard()
        self.broadcaster.broadcast({
            "type": "leaderboard",
            "scores": leaderboard
        })
        
    def end_game(self):
        """End the game and announce the winner"""
        leaderboard = self.broadcaster.get_leaderboard()
        winner = leaderboard[0] if leaderboard else None
        
        self.broadcaster.broadcast({
            "type": "game_over",
            "winner": winner[0] if winner else "No winner",
            "final_scores": leaderboard
        })
        
        # Reset game state
        with self.server_lock:
            self.game_in_progress = False
            self.accepting_players = True
            self.current_question_index = 0
        
    def shutdown(self, *args):
        """Shutdown the server gracefully"""
        print("\nShutting down server...")
        self.accepting_players = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        sys.exit(0)


if __name__ == "__main__":
    server = TriviaServer()
    server.start()
