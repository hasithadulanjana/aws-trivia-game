#!/usr/bin/env python3
"""
AWS Trivia Game Client - Fixed Version
Reliable connection handling for multiplayer games
"""

import socket
import json
import threading
import sys
import time
import curses
import argparse
from curses import wrapper
from network_utils import send_message, receive_message

# Default connection settings
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5000

# UI Constants
TITLE = "AWS Trivia Game"
BORDER_COLOR = 1
HIGHLIGHT_COLOR = 2
CORRECT_COLOR = 3
INCORRECT_COLOR = 4
TIMER_COLOR = 5
NORMAL_COLOR = 6

class TriviaClient:
    """Client for the AWS Trivia Game"""
    
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client_socket = None
        self.connected = False
        self.current_question = None
        self.current_options = None
        self.selected_option = 0
        self.answered = False
        self.answer_correct = None
        self.correct_answer = None
        self.leaderboard = []
        self.timer_value = 0
        self.timer_active = False
        self.is_admin = False
        self.game_started = False
        self.game_over = False
        self.message = "Connecting to server..."
        self.lock = threading.RLock()
        self.receive_thread = None
        
    def connect(self):
        """Connect to the server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set socket options for better reliability
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.client_socket.settimeout(10.0)  # Connection timeout
            
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            # Remove timeout after connection
            self.client_socket.settimeout(None)
            
            # Send nickname to server
            if not send_message(self.client_socket, {
                "type": "join",
                "nickname": self.nickname
            }):
                self.message = "Failed to send join message"
                return False
            
            # Start receiving messages from server
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            self.message = f"Connection error: {e}"
            self.connected = False
            return False
            
    def send_game_message(self, message):
        """Send a message to the server"""
        if self.connected and self.client_socket:
            return send_message(self.client_socket, message)
        return False
                
    def receive_messages(self):
        """Receive and process messages from the server"""
        while self.connected:
            try:
                message = receive_message(self.client_socket)
                if not message:
                    break
                self.process_message(message)
            except Exception as e:
                with self.lock:
                    self.message = f"Error receiving message: {e}"
                break
                
        self.disconnect()
        
    def process_message(self, message):
        """Process a message from the server"""
        message_type = message.get("type", "")
        
        with self.lock:
            if message_type == "error":
                self.message = message["message"]
                
            elif message_type == "admin_rights":
                self.is_admin = True
                self.message = message["message"]
                
            elif message_type == "wait_message":
                self.message = message["message"]
                
            elif message_type == "player_joined":
                self.message = f"Player {message['nickname']} joined. Total players: {message['player_count']}"
                
            elif message_type == "player_left":
                self.message = f"Player {message['nickname']} left. Total players: {message['player_count']}"
                
            elif message_type == "game_starting":
                self.game_started = True
                self.message = message["message"]
                
            elif message_type == "question":
                self.current_question = message["question"]
                self.current_options = message["options"]
                self.selected_option = 0
                self.answered = False
                self.answer_correct = None
                self.correct_answer = None
                self.timer_value = message["timeout"]
                self.timer_active = True
                self.message = f"Question {message['question_number']} of {message['total_questions']}"
                
                # Start timer thread
                timer_thread = threading.Thread(target=self.countdown_timer)
                timer_thread.daemon = True
                timer_thread.start()
                
            elif message_type == "answer_feedback":
                self.answered = True
                self.answer_correct = message["correct"]
                self.correct_answer = message["correct_answer"]
                self.timer_active = False
                
            elif message_type == "timeout":
                self.answered = True
                self.correct_answer = message["correct_answer"]
                self.timer_active = False
                
            elif message_type == "leaderboard":
                self.leaderboard = message["scores"]
                
            elif message_type == "game_over":
                self.game_over = True
                self.timer_active = False
                self.message = f"Game Over! Winner: {message['winner']}"
                self.leaderboard = message["final_scores"]
                
    def countdown_timer(self):
        """Countdown timer for questions"""
        while self.timer_active and self.timer_value > 0:
            time.sleep(1)
            with self.lock:
                self.timer_value -= 1
                
    def submit_answer(self):
        """Submit the selected answer"""
        if not self.answered and self.current_question:
            self.send_game_message({
                "type": "answer",
                "answer": self.selected_option
            })
            
    def start_game(self):
        """Start the game (admin only)"""
        if self.is_admin:
            self.send_game_message({
                "type": "start_game"
            })
            
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

    # ... (rest of the UI code remains the same)
    def draw_screen(self, stdscr):
        """Draw the game screen"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Draw title
        title_x = max(0, (width - len(TITLE)) // 2)
        stdscr.addstr(0, title_x, TITLE, curses.color_pair(BORDER_COLOR) | curses.A_BOLD)
        
        # Draw border
        stdscr.box()
        
        y_pos = 2
        
        with self.lock:
            # Draw status message
            status_text = f"Status: {self.message}"
            stdscr.addstr(y_pos, 2, status_text[:width-4])
            y_pos += 2
            
            # Draw timer if active
            if self.timer_active:
                timer_text = f"Time remaining: {self.timer_value}s"
                stdscr.addstr(y_pos, 2, timer_text, curses.color_pair(TIMER_COLOR) | curses.A_BOLD)
                y_pos += 2
            
            # Draw current question
            if self.current_question and not self.game_over:
                # Question text
                question_lines = self.wrap_text(self.current_question, width - 4)
                for line in question_lines:
                    if y_pos < height - 2:
                        stdscr.addstr(y_pos, 2, line)
                        y_pos += 1
                y_pos += 1
                
                # Options
                if self.current_options:
                    for i, option in enumerate(self.current_options):
                        if y_pos < height - 2:
                            option_text = f"{chr(65+i)}. {option}"
                            color = curses.color_pair(NORMAL_COLOR)
                            
                            if self.answered:
                                if i == self.correct_answer:
                                    color = curses.color_pair(CORRECT_COLOR) | curses.A_BOLD
                                elif i == self.selected_option and not self.answer_correct:
                                    color = curses.color_pair(INCORRECT_COLOR) | curses.A_BOLD
                            elif i == self.selected_option:
                                color = curses.color_pair(HIGHLIGHT_COLOR) | curses.A_BOLD
                            
                            stdscr.addstr(y_pos, 4, option_text[:width-6], color)
                            y_pos += 1
                y_pos += 1
            
            # Draw leaderboard
            if self.leaderboard:
                if y_pos < height - 2:
                    stdscr.addstr(y_pos, 2, "Leaderboard:", curses.color_pair(BORDER_COLOR) | curses.A_BOLD)
                    y_pos += 1
                
                for i, (nickname, score) in enumerate(self.leaderboard[:5]):  # Show top 5
                    if y_pos < height - 2:
                        leaderboard_text = f"{i+1}. {nickname}: {score} points"
                        stdscr.addstr(y_pos, 4, leaderboard_text[:width-6])
                        y_pos += 1
            
            # Draw instructions
            if y_pos < height - 4:
                y_pos = height - 4
                if self.is_admin and not self.game_started:
                    stdscr.addstr(y_pos, 2, "Press 's' to start the game", curses.color_pair(HIGHLIGHT_COLOR))
                elif self.current_question and not self.answered:
                    stdscr.addstr(y_pos, 2, "Use arrow keys to select, Enter to answer", curses.color_pair(HIGHLIGHT_COLOR))
                elif self.game_over:
                    stdscr.addstr(y_pos, 2, "Game Over! Press 'q' to quit", curses.color_pair(HIGHLIGHT_COLOR))
                
                stdscr.addstr(height-2, 2, "Press 'q' to quit", curses.color_pair(BORDER_COLOR))
        
        stdscr.refresh()
    
    def wrap_text(self, text, width):
        """Wrap text to fit within the given width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def run_ui(self, stdscr):
        """Run the curses UI"""
        # Initialize colors
        curses.start_color()
        curses.init_pair(BORDER_COLOR, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(HIGHLIGHT_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(CORRECT_COLOR, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(INCORRECT_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(TIMER_COLOR, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(NORMAL_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        # Set non-blocking input
        stdscr.nodelay(True)
        stdscr.timeout(100)  # 100ms timeout for getch()
        
        while self.connected:
            self.draw_screen(stdscr)
            
            # Handle input
            try:
                key = stdscr.getch()
                
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('s') or key == ord('S'):
                    if self.is_admin and not self.game_started:
                        self.start_game()
                elif key == curses.KEY_UP:
                    if self.current_options and not self.answered:
                        with self.lock:
                            self.selected_option = (self.selected_option - 1) % len(self.current_options)
                elif key == curses.KEY_DOWN:
                    if self.current_options and not self.answered:
                        with self.lock:
                            self.selected_option = (self.selected_option + 1) % len(self.current_options)
                elif key == ord('\n') or key == ord('\r') or key == curses.KEY_ENTER:
                    if self.current_question and not self.answered:
                        self.submit_answer()
                        
            except curses.error:
                pass  # No input available
            
            time.sleep(0.05)  # Small delay to prevent high CPU usage
        
        self.disconnect()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='AWS Trivia Game Client')
    parser.add_argument('--host', default=DEFAULT_HOST, help='Server host')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Server port')
    parser.add_argument('--nickname', required=True, help='Your nickname')
    
    args = parser.parse_args()
    
    client = TriviaClient(args.host, args.port, args.nickname)
    
    if not client.connect():
        print(f"Failed to connect to server: {client.message}")
        return
    
    try:
        wrapper(client.run_ui)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
