#!/usr/bin/env python3
"""
AWS Trivia Game Client
Connects to the server and provides a terminal UI for playing the game
"""

import socket
import json
import threading
import sys
import time
import curses
import argparse
from curses import wrapper

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
        self.lock = threading.Lock()
        
    def connect(self):
        """Connect to the server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            # Send nickname to server
            self.send_message({
                "type": "join",
                "nickname": self.nickname
            })
            
            # Start receiving messages from server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
        except Exception as e:
            self.message = f"Connection error: {e}"
            return False
            
    def send_message(self, message):
        """Send a message to the server"""
        if self.connected:
            try:
                self.client_socket.sendall(json.dumps(message).encode('utf-8'))
            except Exception as e:
                self.message = f"Error sending message: {e}"
                self.disconnect()
                
    def receive_messages(self):
        """Receive and process messages from the server"""
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode('utf-8'))
                self.process_message(message)
            except Exception as e:
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
                self.message = "Time's up!"
                
            elif message_type == "leaderboard":
                self.leaderboard = message["scores"]
                
            elif message_type == "game_over":
                self.game_over = True
                self.game_started = False
                self.leaderboard = message["final_scores"]
                self.message = f"Game over! Winner: {message['winner']}"
                
    def countdown_timer(self):
        """Countdown timer for questions"""
        while self.timer_active and self.timer_value > 0:
            time.sleep(1)
            with self.lock:
                if self.timer_active:
                    self.timer_value -= 1
                    
    def submit_answer(self):
        """Submit the selected answer to the server"""
        if not self.answered and self.current_question:
            self.send_message({
                "type": "answer",
                "answer": self.selected_option
            })
            
    def start_game(self):
        """Send request to start the game (admin only)"""
        if self.is_admin and not self.game_started:
            self.send_message({
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
                
    def run_ui(self, stdscr):
        """Run the terminal UI"""
        # Set up colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(BORDER_COLOR, curses.COLOR_CYAN, -1)
        curses.init_pair(HIGHLIGHT_COLOR, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(CORRECT_COLOR, curses.COLOR_GREEN, -1)
        curses.init_pair(INCORRECT_COLOR, curses.COLOR_RED, -1)
        curses.init_pair(TIMER_COLOR, curses.COLOR_YELLOW, -1)
        curses.init_pair(NORMAL_COLOR, curses.COLOR_WHITE, -1)
        
        # Hide cursor
        curses.curs_set(0)
        
        # Enable keypad mode
        stdscr.keypad(True)
        
        # Set non-blocking input
        stdscr.nodelay(True)
        
        while self.connected:
            # Clear screen
            stdscr.clear()
            
            # Get terminal dimensions
            max_y, max_x = stdscr.getmaxyx()
            
            # Draw border
            stdscr.attron(curses.color_pair(BORDER_COLOR))
            stdscr.box()
            stdscr.attroff(curses.color_pair(BORDER_COLOR))
            
            # Draw title
            title = f" {TITLE} - {self.nickname} "
            stdscr.attron(curses.color_pair(BORDER_COLOR))
            stdscr.addstr(0, (max_x - len(title)) // 2, title)
            stdscr.attroff(curses.color_pair(BORDER_COLOR))
            
            # Lock to prevent race conditions with the receive thread
            with self.lock:
                # Draw message
                if self.message:
                    stdscr.addstr(2, 2, self.message)
                    
                # Draw timer if active
                if self.timer_active and self.timer_value >= 0:
                    timer_text = f"Time left: {self.timer_value}s"
                    stdscr.attron(curses.color_pair(TIMER_COLOR))
                    stdscr.addstr(2, max_x - len(timer_text) - 2, timer_text)
                    stdscr.attroff(curses.color_pair(TIMER_COLOR))
                    
                # Draw question and options
                if self.current_question and not self.game_over:
                    # Draw question
                    question_y = 4
                    question_lines = self.wrap_text(self.current_question, max_x - 4)
                    for i, line in enumerate(question_lines):
                        stdscr.addstr(question_y + i, 2, line)
                        
                    # Draw options
                    options_y = question_y + len(question_lines) + 2
                    for i, option in enumerate(self.current_options):
                        option_text = f"{chr(65 + i)}. {option}"
                        option_lines = self.wrap_text(option_text, max_x - 8)
                        
                        for j, line in enumerate(option_lines):
                            if i == self.selected_option and not self.answered:
                                # Highlight selected option
                                stdscr.attron(curses.color_pair(HIGHLIGHT_COLOR))
                                stdscr.addstr(options_y + j, 4, line)
                                stdscr.attroff(curses.color_pair(HIGHLIGHT_COLOR))
                            elif self.answered and i == self.correct_answer:
                                # Show correct answer
                                stdscr.attron(curses.color_pair(CORRECT_COLOR))
                                stdscr.addstr(options_y + j, 4, line)
                                stdscr.attroff(curses.color_pair(CORRECT_COLOR))
                            elif self.answered and i == self.selected_option and not self.answer_correct:
                                # Show incorrect answer
                                stdscr.attron(curses.color_pair(INCORRECT_COLOR))
                                stdscr.addstr(options_y + j, 4, line)
                                stdscr.attroff(curses.color_pair(INCORRECT_COLOR))
                            else:
                                stdscr.addstr(options_y + j, 4, line)
                                
                        options_y += len(option_lines) + 1
                        
                # Draw leaderboard
                if self.leaderboard:
                    leaderboard_y = max_y - len(self.leaderboard) - 4
                    stdscr.attron(curses.color_pair(BORDER_COLOR))
                    stdscr.addstr(leaderboard_y, 2, "Leaderboard:")
                    stdscr.attroff(curses.color_pair(BORDER_COLOR))
                    
                    for i, (player, score) in enumerate(self.leaderboard):
                        if player == self.nickname:
                            stdscr.attron(curses.A_BOLD)
                        stdscr.addstr(leaderboard_y + i + 1, 2, f"{player}: {score}")
                        if player == self.nickname:
                            stdscr.attroff(curses.A_BOLD)
                            
                # Draw instructions
                instructions = []
                if self.is_admin and not self.game_started:
                    instructions.append("Press 'S' to start the game")
                if self.current_question and not self.answered:
                    instructions.append("Use UP/DOWN to select, ENTER to submit")
                instructions.append("Press 'Q' to quit")
                
                for i, instruction in enumerate(instructions):
                    stdscr.addstr(max_y - len(instructions) + i - 1, 2, instruction)
                    
            # Refresh screen
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
                
                if key == ord('q') or key == ord('Q'):
                    break
                    
                elif key == ord('s') or key == ord('S'):
                    if self.is_admin and not self.game_started:
                        self.start_game()
                        
                elif key == curses.KEY_UP:
                    if self.current_question and not self.answered:
                        self.selected_option = max(0, self.selected_option - 1)
                        
                elif key == curses.KEY_DOWN:
                    if self.current_question and not self.answered:
                        self.selected_option = min(len(self.current_options) - 1, self.selected_option + 1)
                        
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    if self.current_question and not self.answered:
                        self.submit_answer()
                        
            except:
                pass
                
            # Sleep to reduce CPU usage
            time.sleep(0.05)
            
        # Disconnect when UI exits
        self.disconnect()
        
    def wrap_text(self, text, width):
        """Wrap text to fit within a given width"""
        lines = []
        for line in text.split('\n'):
            while len(line) > width:
                # Find the last space before the width limit
                space_index = line[:width].rfind(' ')
                if space_index == -1:  # No space found, force break
                    lines.append(line[:width])
                    line = line[width:]
                else:
                    lines.append(line[:space_index])
                    line = line[space_index+1:]
            lines.append(line)
        return lines


def main():
    """Main function to parse arguments and start the client"""
    parser = argparse.ArgumentParser(description='AWS Trivia Game Client')
    parser.add_argument('--host', default=DEFAULT_HOST, help='Server hostname or IP')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Server port')
    parser.add_argument('--nickname', help='Your player nickname')
    args = parser.parse_args()
    
    # If nickname not provided, prompt for it
    nickname = args.nickname
    if not nickname:
        nickname = input("Enter your nickname: ")
        
    # Create client
    client = TriviaClient(args.host, args.port, nickname)
    
    # Connect to server
    if client.connect():
        try:
            # Start UI
            wrapper(client.run_ui)
        except KeyboardInterrupt:
            pass
        finally:
            client.disconnect()
    else:
        print(client.message)


if __name__ == "__main__":
    # Check if running on Windows and curses is available
    try:
        import curses
    except ImportError:
        print("Error: curses module not found.")
        print("If you're on Windows, install windows-curses with:")
        print("pip install windows-curses")
        sys.exit(1)
        
    main()
