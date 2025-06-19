// AWS Trivia Game - Client-side JavaScript

class TriviaGameClient {
    constructor() {
        this.socket = null;
        this.nickname = '';
        this.isHost = false;
        this.currentQuestion = null;
        this.selectedAnswer = null;
        this.answered = false;
        this.timer = null;
        this.timeLeft = 0;
        
        this.initializeElements();
        this.connectToServer();
    }
    
    initializeElements() {
        // Get DOM elements
        this.elements = {
            connectionStatus: document.getElementById('connectionStatus'),
            gameStatus: document.getElementById('gameStatus'),
            statusText: document.getElementById('statusText'),
            playerCount: document.getElementById('playerCount'),
            startGameBtn: document.getElementById('startGameBtn'),
            questionArea: document.getElementById('questionArea'),
            questionNumber: document.getElementById('questionNumber'),
            questionText: document.getElementById('questionText'),
            optionsContainer: document.getElementById('optionsContainer'),
            timer: document.getElementById('timer'),
            timeLeft: document.getElementById('timeLeft'),
            answerFeedback: document.getElementById('answerFeedback'),
            feedbackTitle: document.getElementById('feedbackTitle'),
            feedbackText: document.getElementById('feedbackText'),
            gameOverArea: document.getElementById('gameOverArea'),
            winnerText: document.getElementById('winnerText'),
            gameDuration: document.getElementById('gameDuration'),
            newGameBtn: document.getElementById('newGameBtn'),
            playersList: document.getElementById('playersList'),
            leaderboard: document.getElementById('leaderboard'),
            errorModal: new bootstrap.Modal(document.getElementById('errorModal')),
            errorMessage: document.getElementById('errorMessage')
        };
        
        // Event listeners
        this.elements.startGameBtn.addEventListener('click', () => this.startGame());
        this.elements.newGameBtn.addEventListener('click', () => this.resetForNewGame());
    }
    
    connectToServer() {
        // Get nickname from session storage
        this.nickname = sessionStorage.getItem('nickname');
        if (!this.nickname) {
            window.location.href = '/';
            return;
        }
        
        // Connect to Socket.IO server
        this.socket = io();
        
        // Socket event listeners
        this.socket.on('connect', () => this.onConnect());
        this.socket.on('disconnect', () => this.onDisconnect());
        this.socket.on('error', (data) => this.showError(data.message));
        this.socket.on('player_joined', (data) => this.onPlayerJoined(data));
        this.socket.on('player_left', (data) => this.onPlayerLeft(data));
        this.socket.on('host_privileges', (data) => this.onHostPrivileges(data));
        this.socket.on('game_state', (data) => this.updateGameState(data));
        this.socket.on('game_starting', (data) => this.onGameStarting(data));
        this.socket.on('new_question', (data) => this.onNewQuestion(data));
        this.socket.on('answer_feedback', (data) => this.onAnswerFeedback(data));
        this.socket.on('question_timeout', (data) => this.onQuestionTimeout(data));
        this.socket.on('leaderboard_update', (data) => this.updateLeaderboard(data));
        this.socket.on('game_over', (data) => this.onGameOver(data));
    }
    
    onConnect() {
        this.elements.connectionStatus.innerHTML = '<i class="fas fa-check"></i> Connected! Joining game...';
        this.elements.connectionStatus.className = 'alert alert-success';
        
        // Join the game
        this.socket.emit('join_game', { nickname: this.nickname });
    }
    
    onDisconnect() {
        this.elements.connectionStatus.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Disconnected from server';
        this.elements.connectionStatus.className = 'alert alert-danger';
        this.elements.connectionStatus.style.display = 'block';
    }
    
    onPlayerJoined(data) {
        this.elements.connectionStatus.style.display = 'none';
        this.elements.gameStatus.style.display = 'block';
        
        if (data.nickname === this.nickname) {
            this.isHost = data.is_host;
        }
        
        this.updatePlayerCount(data.player_count);
    }
    
    onPlayerLeft(data) {
        this.updatePlayerCount(data.player_count);
    }
    
    onHostPrivileges(data) {
        this.isHost = true;
        this.elements.startGameBtn.style.display = 'block';
        this.elements.statusText.textContent = 'You are the host! Start the game when ready.';
    }
    
    updateGameState(data) {
        this.updatePlayersList(data.players);
        this.updatePlayerCount(data.player_count);
        
        if (data.game_in_progress) {
            this.elements.statusText.textContent = `Game in progress (${data.current_question_number}/${data.total_questions})`;
            this.elements.startGameBtn.style.display = 'none';
        }
    }
    
    updatePlayerCount(count) {
        this.elements.playerCount.textContent = `${count} player${count !== 1 ? 's' : ''} connected`;
    }
    
    updatePlayersList(players) {
        this.elements.playersList.innerHTML = '';
        
        players.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player-item';
            
            const nameSpan = document.createElement('span');
            nameSpan.className = 'player-name';
            nameSpan.textContent = player.nickname;
            
            const statusDiv = document.createElement('div');
            
            if (player.nickname === this.nickname && this.isHost) {
                const hostBadge = document.createElement('span');
                hostBadge.className = 'host-badge';
                hostBadge.textContent = 'HOST';
                statusDiv.appendChild(hostBadge);
            }
            
            if (player.answered_current) {
                const answeredBadge = document.createElement('span');
                answeredBadge.className = 'badge bg-success ms-2';
                answeredBadge.innerHTML = '<i class="fas fa-check"></i>';
                statusDiv.appendChild(answeredBadge);
            }
            
            playerDiv.appendChild(nameSpan);
            playerDiv.appendChild(statusDiv);
            this.elements.playersList.appendChild(playerDiv);
        });
    }
    
    startGame() {
        this.socket.emit('start_game');
        this.elements.startGameBtn.disabled = true;
    }
    
    onGameStarting(data) {
        this.elements.gameStatus.style.display = 'none';
        this.elements.statusText.textContent = `Game starting! ${data.total_questions} questions total.`;
        
        // Hide other areas
        this.elements.answerFeedback.style.display = 'none';
        this.elements.gameOverArea.style.display = 'none';
    }
    
    onNewQuestion(data) {
        this.currentQuestion = data;
        this.selectedAnswer = null;
        this.answered = false;
        
        // Update question display
        this.elements.questionNumber.textContent = `Question ${data.question_number} of ${data.total_questions}`;
        this.elements.questionText.textContent = data.question;
        
        // Create option buttons
        this.elements.optionsContainer.innerHTML = '';
        data.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'btn option-btn';
            button.innerHTML = `<strong>${String.fromCharCode(65 + index)}.</strong> ${option}`;
            button.addEventListener('click', () => this.selectAnswer(index, button));
            this.elements.optionsContainer.appendChild(button);
        });
        
        // Start timer
        this.timeLeft = data.timeout;
        this.startTimer();
        
        // Show question area
        this.elements.questionArea.style.display = 'block';
        this.elements.answerFeedback.style.display = 'none';
    }
    
    selectAnswer(index, buttonElement) {
        if (this.answered) return;
        
        // Remove previous selection
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        // Mark new selection
        buttonElement.classList.add('selected');
        this.selectedAnswer = index;
        
        // Submit answer
        this.socket.emit('submit_answer', { answer_index: index });
        this.answered = true;
        
        // Disable all buttons
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.disabled = true;
        });
    }
    
    startTimer() {
        this.elements.timeLeft.textContent = this.timeLeft;
        this.elements.timer.className = 'badge bg-warning fs-6';
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            this.elements.timeLeft.textContent = this.timeLeft;
            
            if (this.timeLeft <= 5) {
                this.elements.timer.className = 'badge bg-danger fs-6 timer-warning';
            }
            
            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.onTimeUp();
            }
        }, 1000);
    }
    
    onTimeUp() {
        if (!this.answered) {
            document.querySelectorAll('.option-btn').forEach(btn => {
                btn.disabled = true;
            });
        }
    }
    
    onAnswerFeedback(data) {
        clearInterval(this.timer);
        
        // Show feedback
        this.elements.answerFeedback.style.display = 'block';
        
        if (data.correct) {
            this.elements.answerFeedback.className = 'alert alert-success';
            this.elements.feedbackTitle.innerHTML = '<i class="fas fa-check-circle"></i> Correct!';
            this.elements.feedbackText.textContent = `Great job! The answer was: ${data.correct_option}`;
        } else {
            this.elements.answerFeedback.className = 'alert alert-danger';
            this.elements.feedbackTitle.innerHTML = '<i class="fas fa-times-circle"></i> Incorrect';
            this.elements.feedbackText.innerHTML = `
                Your answer: ${data.your_option}<br>
                Correct answer: ${data.correct_option}
            `;
        }
        
        // Highlight correct/incorrect answers
        document.querySelectorAll('.option-btn').forEach((btn, index) => {
            if (index === data.correct_answer) {
                btn.classList.add('correct');
            } else if (index === data.your_answer && !data.correct) {
                btn.classList.add('incorrect');
            }
        });
    }
    
    onQuestionTimeout(data) {
        clearInterval(this.timer);
        
        if (!this.answered) {
            this.elements.answerFeedback.style.display = 'block';
            this.elements.answerFeedback.className = 'alert alert-warning';
            this.elements.feedbackTitle.innerHTML = '<i class="fas fa-clock"></i> Time\'s Up!';
            this.elements.feedbackText.textContent = `The correct answer was: ${data.correct_option}`;
            
            // Highlight correct answer
            document.querySelectorAll('.option-btn').forEach((btn, index) => {
                if (index === data.correct_answer) {
                    btn.classList.add('correct');
                }
            });
        }
    }
    
    updateLeaderboard(data) {
        this.elements.leaderboard.innerHTML = '';
        
        if (data.leaderboard.length === 0) {
            this.elements.leaderboard.innerHTML = '<p class="text-muted text-center">No scores yet</p>';
            return;
        }
        
        data.leaderboard.forEach((player, index) => {
            const playerDiv = document.createElement('div');
            playerDiv.className = `leaderboard-item rank-${index + 1}`;
            
            playerDiv.innerHTML = `
                <span class="leaderboard-rank">#${index + 1}</span>
                <span class="leaderboard-name">${player[0]}</span>
                <span class="leaderboard-score">${player[1]}</span>
            `;
            
            this.elements.leaderboard.appendChild(playerDiv);
        });
    }
    
    onGameOver(data) {
        clearInterval(this.timer);
        
        // Hide question area
        this.elements.questionArea.style.display = 'none';
        this.elements.answerFeedback.style.display = 'none';
        
        // Show game over
        this.elements.gameOverArea.style.display = 'block';
        this.elements.winnerText.innerHTML = `<i class="fas fa-crown"></i> Winner: ${data.winner}`;
        this.elements.gameDuration.textContent = `Game duration: ${data.game_duration}`;
        
        // Update final leaderboard
        this.updateLeaderboard({ leaderboard: data.final_scores });
    }
    
    resetForNewGame() {
        // Reset UI state
        this.elements.gameOverArea.style.display = 'none';
        this.elements.questionArea.style.display = 'none';
        this.elements.answerFeedback.style.display = 'none';
        this.elements.gameStatus.style.display = 'block';
        
        if (this.isHost) {
            this.elements.startGameBtn.style.display = 'block';
            this.elements.startGameBtn.disabled = false;
            this.elements.statusText.textContent = 'Ready for a new game!';
        } else {
            this.elements.statusText.textContent = 'Waiting for host to start new game...';
        }
        
        // Reset leaderboard
        this.elements.leaderboard.innerHTML = '<p class="text-muted text-center">Game not started</p>';
    }
    
    showError(message) {
        this.elements.errorMessage.textContent = message;
        this.elements.errorModal.show();
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TriviaGameClient();
});
