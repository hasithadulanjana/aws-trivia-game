#!/usr/bin/env python3
"""
AWS Trivia Game GUI Client
Connects to the server and provides a graphical UI for playing the game
"""

import socket
import json
import threading
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import argparse

# Default connection settings
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5000

# UI Constants
TITLE = "AWS Trivia Game"
BG_COLOR = "#f0f0f0"
HIGHLIGHT_COLOR = "#e1f5fe"
CORRECT_COLOR = "#c8e6c9"
INCORRECT_COLOR = "#ffcdd2"
BUTTON_COLOR = "#2196f3"
BUTTON_TEXT_COLOR = "white"

class TriviaClientGUI:
    """GUI Client for the AWS Trivia Game"""
    
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client_socket = None
        self.connected = False
        self.current_question = None
        self.current_options = None
        self.selected_option = None
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
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(TITLE)
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create UI elements
        self.create_widgets()
        
        # Connect to server
        self.connect()
        
        # Start UI update loop
        self.update_ui()
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status frame (top)
        self.status_frame = ttk.Frame(self.main_frame, padding=5)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        # Status message
        self.status_label = ttk.Label(self.status_frame, text="", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT)
        
        # Timer
        self.timer_label = ttk.Label(self.status_frame, text="", font=("Arial", 12, "bold"))
        self.timer_label.pack(side=tk.RIGHT)
        
        # Question frame
        self.question_frame = ttk.Frame(self.main_frame, padding=10)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Question label
        self.question_label = ttk.Label(self.question_frame, text="", font=("Arial", 14), wraplength=700)
        self.question_label.pack(fill=tk.X, pady=10)
        
        # Options frame
        self.options_frame = ttk.Frame(self.question_frame, padding=5)
        self.options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Option buttons (will be created dynamically)
        self.option_buttons = []
        
        # Admin button (for starting the game)
        self.admin_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game)
        self.admin_button.pack(pady=10)
        self.admin_button.pack_forget()  # Hide initially
        
        # Leaderboard frame
        self.leaderboard_frame = ttk.LabelFrame(self.main_frame, text="Leaderboard", padding=10)
        self.leaderboard_frame.pack(fill=tk.X, pady=10)
        
        # Leaderboard treeview
        self.leaderboard_tree = ttk.Treeview(self.leaderboard_frame, columns=("Player", "Score"), show="headings", height=5)
        self.leaderboard_tree.heading("Player", text="Player")
        self.leaderboard_tree.heading("Score", text="Score")
        self.leaderboard_tree.column("Player", width=150)
        self.leaderboard_tree.column("Score", width=50)
        self.leaderboard_tree.pack(fill=tk.X)
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12), background=BG_COLOR)
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR)
        style.configure("TLabelframe.Label", font=("Arial", 12, "bold"), background=BG_COLOR)
        
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
            
        except Exception as e:
            self.message = f"Connection error: {e}"
            messagebox.showerror("Connection Error", str(e))
            self.root.after(1000, self.root.destroy)
            
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
                # Show admin button
                self.root.after(0, lambda: self.admin_button.pack(pady=10))
                
            elif message_type == "wait_message":
                self.message = message["message"]
                
            elif message_type == "player_joined":
                self.message = f"Player {message['nickname']} joined. Total players: {message['player_count']}"
                
            elif message_type == "player_left":
                self.message = f"Player {message['nickname']} left. Total players: {message['player_count']}"
                
            elif message_type == "game_starting":
                self.game_started = True
                self.message = message["message"]
                # Hide admin button
                self.root.after(0, lambda: self.admin_button.pack_forget())
                
            elif message_type == "question":
                self.current_question = message["question"]
                self.current_options = message["options"]
                self.selected_option = None
                self.answered = False
                self.answer_correct = None
                self.correct_answer = None
                self.timer_value = message["timeout"]
                self.timer_active = True
                self.message = f"Question {message['question_number']} of {message['total_questions']}"
                
                # Update question and options in UI
                self.root.after(0, self.update_question_ui)
                
            elif message_type == "answer_feedback":
                self.answered = True
                self.answer_correct = message["correct"]
                self.correct_answer = message["correct_answer"]
                self.timer_active = False
                
                # Update options to show correct/incorrect
                self.root.after(0, self.update_answer_feedback)
                
            elif message_type == "timeout":
                self.answered = True
                self.correct_answer = message["correct_answer"]
                self.timer_active = False
                self.message = "Time's up!"
                
                # Update options to show correct answer
                self.root.after(0, self.update_answer_feedback)
                
            elif message_type == "leaderboard":
                self.leaderboard = message["scores"]
                
                # Update leaderboard in UI
                self.root.after(0, self.update_leaderboard_ui)
                
            elif message_type == "game_over":
                self.game_over = True
                self.game_started = False
                self.leaderboard = message["final_scores"]
                self.message = f"Game over! Winner: {message['winner']}"
                
                # Show game over message
                self.root.after(0, lambda: messagebox.showinfo("Game Over", f"Game over! Winner: {message['winner']}"))
                
    def update_question_ui(self):
        """Update the question and options in the UI"""
        # Update question text
        self.question_label.config(text=self.current_question)
        
        # Clear existing option buttons
        for button in self.option_buttons:
            button.destroy()
        self.option_buttons = []
        
        # Create new option buttons
        for i, option in enumerate(self.current_options):
            option_text = f"{chr(65 + i)}. {option}"
            button = ttk.Button(
                self.options_frame,
                text=option_text,
                command=lambda idx=i: self.select_option(idx),
                style="TButton",
                width=60
            )
            button.pack(fill=tk.X, pady=5)
            self.option_buttons.append(button)
            
    def update_answer_feedback(self):
        """Update the UI to show answer feedback"""
        for i, button in enumerate(self.option_buttons):
            if i == self.correct_answer:
                # Correct answer
                button.config(style="Correct.TButton")
            elif self.selected_option == i and i != self.correct_answer:
                # Incorrect answer
                button.config(style="Incorrect.TButton")
                
        # Configure styles for correct/incorrect buttons
        style = ttk.Style()
        style.configure("Correct.TButton", background=CORRECT_COLOR)
        style.configure("Incorrect.TButton", background=INCORRECT_COLOR)
        
    def update_leaderboard_ui(self):
        """Update the leaderboard in the UI"""
        # Clear existing items
        for item in self.leaderboard_tree.get_children():
            self.leaderboard_tree.delete(item)
            
        # Add new items
        for player, score in self.leaderboard:
            self.leaderboard_tree.insert("", tk.END, values=(player, score))
            
    def select_option(self, option_index):
        """Handle option selection"""
        if not self.answered:
            self.selected_option = option_index
            
            # Highlight selected option
            for i, button in enumerate(self.option_buttons):
                if i == option_index:
                    button.config(style="Selected.TButton")
                else:
                    button.config(style="TButton")
                    
            # Configure style for selected button
            style = ttk.Style()
            style.configure("Selected.TButton", background=HIGHLIGHT_COLOR)
            
            # Submit answer
            self.submit_answer()
            
    def submit_answer(self):
        """Submit the selected answer to the server"""
        if not self.answered and self.selected_option is not None:
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
            
    def update_ui(self):
        """Update UI elements periodically"""
        if self.connected:
            # Update status message
            self.status_label.config(text=self.message)
            
            # Update timer
            if self.timer_active and self.timer_value >= 0:
                self.timer_label.config(text=f"Time left: {self.timer_value}s")
                if self.timer_value <= 5:
                    self.timer_label.config(foreground="red")
                else:
                    self.timer_label.config(foreground="black")
            else:
                self.timer_label.config(text="")
                
            # Schedule next update
            self.root.after(100, self.update_ui)
            
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
                
        # Show disconnection message and close after delay
        self.message = "Disconnected from server"
        self.root.after(0, lambda: messagebox.showinfo("Disconnected", "Disconnected from server"))
        self.root.after(1000, self.root.destroy)
        
    def on_closing(self):
        """Handle window closing"""
        self.disconnect()
        self.root.destroy()
        
    def run(self):
        """Run the GUI main loop"""
        self.root.mainloop()


def main():
    """Main function to parse arguments and start the client"""
    parser = argparse.ArgumentParser(description='AWS Trivia Game GUI Client')
    parser.add_argument('--host', default=DEFAULT_HOST, help='Server hostname or IP')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Server port')
    parser.add_argument('--nickname', help='Your player nickname')
    args = parser.parse_args()
    
    # If nickname not provided, prompt for it
    nickname = args.nickname
    if not nickname:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        nickname = simpledialog.askstring("Nickname", "Enter your nickname:", parent=root)
        if not nickname:
            sys.exit(0)
        root.destroy()
        
    # Create and run client
    client = TriviaClientGUI(args.host, args.port, nickname)
    client.run()


if __name__ == "__main__":
    main()
