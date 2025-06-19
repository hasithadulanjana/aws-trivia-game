#!/usr/bin/env python3
"""
AWS Trivia Game Web Server
Flask-based web interface with Socket.IO for real-time multiplayer
Multi-level progression system with difficulty-based questions
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import time
import random
import threading
from datetime import datetime
from questions_levels import levels, get_questions_for_level, get_level_info, get_max_level

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aws-trivia-game-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Game configuration
MAX_PLAYERS = 10
QUESTION_TIMEOUT = 15  # seconds
WAIT_TIME_BETWEEN_QUESTIONS = 3  # seconds
QUESTIONS_PER_GAME = 10

class WebTriviaGame:
    """Manages the web-based trivia game state with level progression"""
    
    def __init__(self):
        self.players = {}  # {session_id: {nickname, score, answered_current, level, total_correct}}
        self.game_in_progress = False
        self.current_question_index = 0
        self.current_question = None
        self.game_questions = []
        self.question_timer = None
        self.host_session = None
        self.answered_current_question = set()
        self.game_start_time = None
        self.current_level = 1  # Start at level 1
        
    def add_player(self, session_id, nickname, level=1):
        """Add a new player to the game"""
        if len(self.players) >= MAX_PLAYERS:
            return False, "Game is full"
        
        # Check for duplicate nicknames
        for player in self.players.values():
            if player['nickname'].lower() == nickname.lower():
                return False, "Nickname already taken"
        
        self.players[session_id] = {
            'nickname': nickname,
            'score': 0,
            'answered_current': False,
            'connected_at': datetime.now(),
            'level': level,
            'total_correct': 0,
            'level_progress': {i: False for i in range(1, get_max_level() + 1)}  # Track completed levels
        }
        
        # First player becomes the host
        if len(self.players) == 1:
            self.host_session = session_id
            
        return True, "Player added successfully"
    
    def remove_player(self, session_id):
        """Remove a player from the game"""
        if session_id in self.players:
            nickname = self.players[session_id]['nickname']
            del self.players[session_id]
            
            # If host left, assign new host
            if session_id == self.host_session and self.players:
                self.host_session = next(iter(self.players.keys()))
                
            return nickname
        return None
    
    def start_game(self, session_id, level=None):
        """Start the game (host only) at specified level"""
        if session_id != self.host_session:
            print(f"Non-host {session_id} attempted to start game. Host is {self.host_session}")
            return False, "Only the host can start the game"
        
        if self.game_in_progress:
            print(f"Game start attempted while game already in progress")
            return False, "Game already in progress"
        
        if len(self.players) < 1:
            print(f"Game start attempted with insufficient players: {len(self.players)}")
            return False, "Need at least 1 player to start"
        
        # Determine level to play
        if level is None:
            level = self.current_level
        
        level_info = get_level_info(level)
        if not level_info:
            return False, f"Invalid level: {level}"
        
        print(f"Host {session_id} starting game at Level {level}: {level_info['name']} with {len(self.players)} players")
        
        # Prepare questions for the specified level
        level_questions = get_questions_for_level(level)
        if not level_questions:
            return False, f"No questions available for level {level}"
            
        self.game_questions = random.sample(level_questions, min(len(level_questions), QUESTIONS_PER_GAME))
        self.game_in_progress = True
        self.current_question_index = 0
        self.current_level = level
        self.game_start_time = datetime.now()
        
        # Reset player scores for new level
        for player in self.players.values():
            player['score'] = 0
            player['total_correct'] = 0
            player['answered_current'] = False
        
        # Start the game in a separate thread
        threading.Thread(target=self._run_game, daemon=True).start()
        
        return True, f"Game started at Level {level}: {level_info['name']}"
    
    def _run_game(self):
        """Run the game loop"""
        level_info = get_level_info(self.current_level)
        
        # Notify all players that game is starting
        socketio.emit('game_starting', {
            'message': f'Starting Level {self.current_level}: {level_info["name"]}!',
            'level': self.current_level,
            'level_name': level_info["name"],
            'level_description': level_info["description"],
            'total_questions': len(self.game_questions)
        })
        
        time.sleep(2)
        self._next_question()
    
    def _next_question(self):
        """Send the next question"""
        if self.current_question_index >= len(self.game_questions):
            self._end_game()
            return
        
        # Reset answered status for all players
        self.answered_current_question = set()
        for player in self.players.values():
            player['answered_current'] = False
        
        self.current_question = self.game_questions[self.current_question_index]
        
        # Send question to all players
        socketio.emit('new_question', {
            'question_number': self.current_question_index + 1,
            'total_questions': len(self.game_questions),
            'question': self.current_question['question'],
            'options': self.current_question['options'],
            'timeout': QUESTION_TIMEOUT
        })
        
        # Set timer for question timeout
        self.question_timer = threading.Timer(QUESTION_TIMEOUT, self._handle_question_timeout)
        self.question_timer.start()
        
        self.current_question_index += 1
    
    def _handle_question_timeout(self):
        """Handle question timeout"""
        # Send correct answer to all players
        socketio.emit('question_timeout', {
            'correct_answer': self.current_question['answer'],
            'correct_option': self.current_question['options'][self.current_question['answer']]
        })
        
        # Send leaderboard
        self._send_leaderboard()
        
        # Wait before next question
        time.sleep(WAIT_TIME_BETWEEN_QUESTIONS)
        self._next_question()
    
    def submit_answer(self, session_id, answer_index):
        """Process a player's answer"""
        if session_id not in self.players:
            return False, "Player not found"
        
        if not self.game_in_progress or not self.current_question:
            return False, "No active question"
        
        if session_id in self.answered_current_question:
            return False, "Already answered this question"
        
        player = self.players[session_id]
        correct = answer_index == self.current_question['answer']
        
        if correct:
            player['score'] += 1
            player['total_correct'] += 1
        
        player['answered_current'] = True
        self.answered_current_question.add(session_id)
        
        # Send feedback to the player
        socketio.emit('answer_feedback', {
            'correct': correct,
            'correct_answer': self.current_question['answer'],
            'correct_option': self.current_question['options'][self.current_question['answer']],
            'your_answer': answer_index,
            'your_option': self.current_question['options'][answer_index] if answer_index < len(self.current_question['options']) else 'Invalid',
            'question_category': self.current_question.get('category', 'General'),
            'difficulty': self.current_question.get('difficulty', 'unknown')
        }, room=request.sid)
        
        # If all players answered, move to next question
        if len(self.answered_current_question) == len(self.players):
            if self.question_timer:
                self.question_timer.cancel()
            self._send_leaderboard()
            time.sleep(WAIT_TIME_BETWEEN_QUESTIONS)
            self._next_question()
        
        return True, "Answer submitted"
    
    def _send_leaderboard(self):
        """Send current leaderboard to all players"""
        leaderboard = sorted(
            [(p['nickname'], p['score']) for p in self.players.values()],
            key=lambda x: x[1],
            reverse=True
        )
        
        socketio.emit('leaderboard_update', {
            'leaderboard': leaderboard
        })
    
    def _end_game(self):
        """End the game and check for level progression"""
        leaderboard = sorted(
            [(p['nickname'], p['score'], p['total_correct']) for p in self.players.values()],
            key=lambda x: x[1],
            reverse=True
        )
        
        winner = leaderboard[0] if leaderboard else None
        level_info = get_level_info(self.current_level)
        
        # Check for perfect scores and level progression
        perfect_score_players = []
        for session_id, player in self.players.items():
            if player['total_correct'] == len(self.game_questions):  # 100% accuracy
                perfect_score_players.append({
                    'session_id': session_id,
                    'nickname': player['nickname'],
                    'can_advance': self.current_level < get_max_level()
                })
                # Mark current level as completed
                player['level_progress'][self.current_level] = True
        
        # Prepare game over data
        game_over_data = {
            'winner': winner[0] if winner else 'No winner',
            'final_scores': [{'nickname': score[0], 'score': score[1], 'correct_answers': score[2]} for score in leaderboard],
            'game_duration': str(datetime.now() - self.game_start_time).split('.')[0] if self.game_start_time else 'Unknown',
            'current_level': self.current_level,
            'level_name': level_info['name'],
            'level_description': level_info['description'],
            'total_questions': len(self.game_questions),
            'perfect_score_players': perfect_score_players,
            'next_level_available': self.current_level < get_max_level()
        }
        
        # Add level progression messages for perfect score players
        if perfect_score_players:
            if self.current_level < get_max_level():
                next_level_info = get_level_info(self.current_level + 1)
                game_over_data['next_level_info'] = {
                    'level': self.current_level + 1,
                    'name': next_level_info['name'],
                    'description': next_level_info['description']
                }
                game_over_data['unlock_message'] = level_info.get('unlock_message', 'Great job! Ready for the next level?')
            else:
                game_over_data['unlock_message'] = level_info.get('unlock_message', 'Congratulations! You have mastered all levels!')
        
        socketio.emit('game_over', game_over_data)
        
        # Reset game state
        self.game_in_progress = False
        self.current_question_index = 0
        self.current_question = None
        self.game_questions = []
        self.answered_current_question = set()
        
        # Reset player scores but keep level progress
        for player in self.players.values():
            player['score'] = 0
            player['total_correct'] = 0
            player['answered_current'] = False
    
    def get_game_state(self):
        """Get current game state"""
        return {
            'players': [
                {
                    'nickname': p['nickname'],
                    'score': p['score'],
                    'answered_current': p.get('answered_current', False)
                }
                for p in self.players.values()
            ],
            'game_in_progress': self.game_in_progress,
            'player_count': len(self.players),
            'current_question_number': self.current_question_index,
            'total_questions': len(self.game_questions) if self.game_questions else 0
        }

# Global game instance
game = WebTriviaGame()

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/test')
def test_page():
    """Test Socket.IO connection page"""
    return render_template('test.html')

@app.route('/game')
def game_page():
    """Game interface page"""
    return render_template('game.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')
    nickname = game.remove_player(request.sid)
    if nickname:
        emit('player_left', {
            'nickname': nickname,
            'player_count': len(game.players)
        }, broadcast=True)

@socketio.on('join_game')
def handle_join_game(data):
    """Handle player joining the game"""
    nickname = data.get('nickname', '').strip()
    
    if not nickname:
        emit('error', {'message': 'Nickname is required'})
        return
    
    print(f"Player attempting to join: {nickname} (session: {request.sid})")
    
    success, message = game.add_player(request.sid, nickname)
    
    if success:
        print(f"Player {nickname} joined successfully. Total players: {len(game.players)}")
        
        # Notify all players
        emit('player_joined', {
            'nickname': nickname,
            'player_count': len(game.players),
            'is_host': request.sid == game.host_session
        }, broadcast=True)
        
        # Send game state to the new player
        emit('game_state', game.get_game_state())
        
        # If this is the host, give them admin rights
        if request.sid == game.host_session:
            print(f"Granting host privileges to {nickname}")
            emit('host_privileges', {'message': 'You are the host. You can start the game when ready.'})
    else:
        print(f"Failed to add player {nickname}: {message}")
        emit('error', {'message': message})

@socketio.on('start_game')
def handle_start_game():
    """Handle game start request"""
    print(f"Game start requested by session: {request.sid}")
    success, message = game.start_game(request.sid)
    
    if not success:
        print(f"Game start failed: {message}")
        emit('error', {'message': message})
    else:
        print(f"Game started successfully by {request.sid}")

@socketio.on('submit_answer')
def handle_submit_answer(data):
    """Handle answer submission"""
    answer_index = data.get('answer_index')
    
    if answer_index is None:
        emit('error', {'message': 'Answer index is required'})
        return
    
    success, message = game.submit_answer(request.sid, answer_index)
    
    if not success:
        emit('error', {'message': message})

@socketio.on('get_game_state')
def handle_get_game_state():
    """Send current game state to requesting client"""
    emit('game_state', game.get_game_state())

@socketio.on('start_level')
def handle_start_level(data):
    """Handle starting a specific level"""
    level = data.get('level', 1)
    success, message = game.start_game(request.sid, level)
    
    if success:
        emit('game_started', {'message': message}, broadcast=True)
        print(f"Level {level} started successfully by {request.sid}")
    else:
        emit('error', {'message': message})
        print(f"Failed to start level {level}: {message}")

@socketio.on('get_available_levels')
def handle_get_available_levels():
    """Send available levels to client"""
    player = game.players.get(request.sid)
    if not player:
        emit('error', {'message': 'Player not found'})
        return
    
    available_levels = []
    for level_num in range(1, get_max_level() + 1):
        level_info = get_level_info(level_num)
        is_unlocked = level_num == 1 or player['level_progress'].get(level_num - 1, False)
        is_completed = player['level_progress'].get(level_num, False)
        
        available_levels.append({
            'level': level_num,
            'name': level_info['name'],
            'description': level_info['description'],
            'unlocked': is_unlocked,
            'completed': is_completed
        })
    
    emit('available_levels', {
        'levels': available_levels,
        'current_level': game.current_level,
        'max_level': get_max_level()
    })

@socketio.on('advance_to_next_level')
def handle_advance_to_next_level():
    """Handle advancing to next level after perfect score"""
    player = game.players.get(request.sid)
    if not player:
        emit('error', {'message': 'Player not found'})
        return
    
    # Check if player can advance
    current_level_completed = player['level_progress'].get(game.current_level, False)
    next_level = game.current_level + 1
    
    if not current_level_completed:
        emit('error', {'message': 'You must complete the current level with 100% to advance'})
        return
    
    if next_level > get_max_level():
        emit('error', {'message': 'You have already completed all levels!'})
        return
    
    # Start next level
    success, message = game.start_game(request.sid, next_level)
    
    if success:
        emit('level_advanced', {
            'message': message,
            'new_level': next_level,
            'level_info': get_level_info(next_level)
        }, broadcast=True)
        print(f"Advanced to level {next_level} by {request.sid}")
    else:
        emit('error', {'message': message})

@socketio.on('test_message')
def handle_test_message(data):
    """Handle test message"""
    print(f'Received test message: {data}')
    emit('connected', {'message': 'Test message received!'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting AWS Trivia Game Web Server on port {port}...")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
