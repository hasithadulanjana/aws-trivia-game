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
            playerCountBadge: document.getElementById('playerCountBadge'),
            startGameBtn: document.getElementById('startGameBtn'),
            gameProgress: document.getElementById('gameProgress'),
            progressText: document.getElementById('progressText'),
            progressBar: document.getElementById('progressBar'),
            gameScore: document.getElementById('gameScore'),
            exitGameBtn: document.getElementById('exitGameBtn')
            questionArea: document.getElementById('questionArea'),
            questionNumber: document.getElementById('questionNumber'),
            questionText: document.getElementById('questionText'),
            optionsContainer: document.getElementById('optionsContainer'),
            answerStatus: document.getElementById('answerStatus'),
            timer: document.getElementById('timer'),
            timeLeft: document.getElementById('timeLeft'),
            answerFeedback: document.getElementById('answerFeedback'),
            feedbackTitle: document.getElementById('feedbackTitle'),
            feedbackText: document.getElementById('feedbackText'),
            gameOverArea: document.getElementById('gameOverArea'),
            winnerText: document.getElementById('winnerText'),
            gameDuration: document.getElementById('gameDuration'),
            newGameBtn: document.getElementById('newGameBtn'),
            leaveGameBtn: document.getElementById('leaveGameBtn'),
            playersList: document.getElementById('playersList'),
            leaderboard: document.getElementById('leaderboard'),
            totalQuestions: document.getElementById('totalQuestions'),
            timePerQuestion: document.getElementById('timePerQuestion'),
            confirmModal: new bootstrap.Modal(document.getElementById('confirmModal')),
            confirmTitle: document.getElementById('confirmTitle'),
            confirmMessage: document.getElementById('confirmMessage'),
            confirmBtn: document.getElementById('confirmBtn'),
            errorModal: new bootstrap.Modal(document.getElementById('errorModal')),
            errorMessage: document.getElementById('errorMessage')
        };
        
        // Event listeners
        this.elements.startGameBtn.addEventListener('click', () => this.confirmStartGame());
        this.elements.newGameBtn.addEventListener('click', () => this.resetForNewGame());
        this.elements.leaveGameBtn.addEventListener('click', () => this.confirmLeaveGame());
        
        // Exit game button (during gameplay)
        if (this.elements.exitGameBtn) {
            this.elements.exitGameBtn.addEventListener('click', () => this.handleExitGame());
        }
        
        // Keyboard shortcut for exit (ESC key)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentQuestion) {
                this.handleExitGame();
            }
        });
    }
    
    connectToServer() {
        // Get nickname from session storage
        this.nickname = sessionStorage.getItem('nickname');
        if (!this.nickname) {
            window.location.href = '/';
            return;
        }
        
        // Connect to Socket.IO server with explicit configuration
        this.socket = io({
            transports: ['websocket', 'polling'],
            timeout: 5000,
            forceNew: true
        });
        
        // Add connection timeout
        setTimeout(() => {
            if (!this.socket.connected) {
                this.showError('Failed to connect to game server. Please refresh and try again.');
            }
        }, 10000);
        
        // Socket event listeners
        this.socket.on('connect', () => {
            console.log('Socket.IO connected successfully');
            this.onConnect();
        });
        this.socket.on('disconnect', () => {
            console.log('Socket.IO disconnected');
            this.onDisconnect();
        });
        this.socket.on('connect_error', (error) => {
            console.error('Socket.IO connection error:', error);
            this.showError('Connection failed: ' + error.message);
        });
        this.socket.on('error', (data) => {
            console.error('Socket.IO error:', data);
            this.showError(data.message);
        });
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
        this.updateConnectionStatus('check', 'Connected! Joining game...', 'success');
        
        // Join the game
        this.socket.emit('join_game', { nickname: this.nickname });
    }
    
    onDisconnect() {
        this.updateConnectionStatus('exclamation-triangle', 'Disconnected from server. Trying to reconnect...', 'danger');
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
        this.elements.startGameBtn.disabled = false;
        this.elements.statusText.innerHTML = '<i class="fas fa-crown"></i> You are the host! Click "Start Game" when ready.';
        
        // Add visual emphasis for host
        this.elements.gameStatus.classList.add('border-warning');
        
        // Show host instructions
        this.showHostInstructions();
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
        this.elements.playerCountBadge.textContent = count;
        
        // Update players list if empty
        if (count === 0) {
            this.elements.playersList.innerHTML = '<p class="text-muted text-center">No players connected</p>';
        }
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
        // Add confirmation for host
        if (!confirm('Are you ready to start the game? All connected players will participate.')) {
            return;
        }
        
        this.socket.emit('start_game');
        this.elements.startGameBtn.disabled = true;
        this.elements.startGameBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';
        this.elements.statusText.textContent = 'Starting game...';
    }
    
    onGameStarting(data) {
        this.elements.gameStatus.style.display = 'none';
        this.elements.connectionStatus.style.display = 'none';
        
        // Update game info
        this.elements.totalQuestions.textContent = data.total_questions;
        this.updateGameProgress(0, data.total_questions);
        
        // Hide other areas
        this.elements.answerFeedback.style.display = 'none';
        this.elements.gameOverArea.style.display = 'none';
        
        // Show starting message
        this.showTemporaryMessage(`Game starting! ${data.total_questions} questions total.`, 'info');
    }
    
    onNewQuestion(data) {
        this.currentQuestion = data;
        this.selectedAnswer = null;
        this.answered = false;
        
        // Update progress
        this.updateGameProgress(data.question_number, data.total_questions);
        
        // Update question display
        this.elements.questionNumber.textContent = `Question ${data.question_number} of ${data.total_questions}`;
        this.elements.questionText.textContent = data.question;
        this.elements.answerStatus.textContent = 'Select your answer';
        this.elements.answerStatus.className = 'text-muted';
        
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
        
        // Update status
        this.elements.answerStatus.textContent = 'Answer submitted!';
        this.elements.answerStatus.className = 'text-success';
        
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
    
    showHostInstructions() {
        // Create a temporary notification for host
        const notification = document.createElement('div');
        notification.className = 'alert alert-info alert-dismissible fade show mt-3';
        notification.innerHTML = `
            <i class="fas fa-info-circle"></i>
            <strong>Host Instructions:</strong>
            <ul class="mb-0 mt-2">
                <li>Wait for other players to join (optional)</li>
                <li>Click "Start Game" when you're ready to begin</li>
                <li>The game will start immediately after clicking</li>
                <li>All connected players will participate</li>
            </ul>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert after game status
        this.elements.gameStatus.parentNode.insertBefore(notification, this.elements.gameStatus.nextSibling);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 10000);
    }
    
    updateConnectionStatus(status, message, type = 'info') {
        this.elements.connectionStatus.className = `alert alert-${type}`;
        this.elements.connectionStatus.innerHTML = `<i class="fas fa-${status}"></i> ${message}`;
        this.elements.connectionStatus.style.display = 'block';
    }
    
    confirmStartGame() {
        this.elements.confirmTitle.textContent = 'Start Game';
        this.elements.confirmMessage.textContent = 'Are you ready to start the game? All connected players will participate and the game will begin immediately.';
        
        // Set up confirm button
        this.elements.confirmBtn.onclick = () => {
            this.elements.confirmModal.hide();
            this.startGame();
        };
        
        this.elements.confirmModal.show();
    }
    
    confirmLeaveGame() {
        this.elements.confirmTitle.textContent = 'Leave Game';
        this.elements.confirmMessage.textContent = 'Are you sure you want to leave the game? You will be disconnected and cannot rejoin this session.';
        
        // Set up confirm button
        this.elements.confirmBtn.onclick = () => {
            this.elements.confirmModal.hide();
            this.leaveGame();
        };
        
        this.elements.confirmModal.show();
    }
    
    leaveGame() {
        // Disconnect from the game
        if (this.socket) {
            this.socket.disconnect();
        }
        
        // Clear session storage
        sessionStorage.removeItem('nickname');
        
        // Redirect to home page
        window.location.href = '/';
    }
    
    handleExitGame() {
        this.elements.confirmTitle.textContent = 'Exit Current Game';
        this.elements.confirmMessage.textContent = 'Are you sure you want to exit the current game? You will return to the lobby but remain connected.';
        
        // Set up confirm button
        this.elements.confirmBtn.onclick = () => {
            this.elements.confirmModal.hide();
            this.exitCurrentGame();
        };
        
        this.elements.confirmModal.show();
    }
    
    exitCurrentGame() {
        // Clear current question state
        this.currentQuestion = null;
        this.answered = false;
        this.selectedAnswer = null;
        
        // Clear timer
        if (this.timer) {
            clearInterval(this.timer);
        }
        
        // Emit exit game event
        this.socket.emit('exit_game');
        
        // Hide game areas and show lobby
        this.hideAllGameScreens();
        this.showLobby();
        
        // Show exit notification
        this.showExitNotification();
        
        // Update status
        this.updateStatus('Game exited. Returned to lobby.', 'info');
    }
    
    hideAllGameScreens() {
        // Hide all game-related screens
        const gameScreens = [
            'questionArea',
            'gameArea', 
            'gameOverArea'
        ];
        
        gameScreens.forEach(screenId => {
            const screen = document.getElementById(screenId);
            if (screen) {
                screen.style.display = 'none';
            }
        });
    }
    
    showExitNotification() {
        // Create exit notification
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        notification.innerHTML = `
            <i class="fas fa-sign-out-alt"></i> Successfully exited game!
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification && notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
    
    updateGameProgress(current, total) {
        const percentage = (current / total) * 100;
        this.elements.progressBar.style.width = `${percentage}%`;
        this.elements.progressText.textContent = `Question ${current} of ${total}`;
        
        if (current > 0) {
            this.elements.gameProgress.style.display = 'block';
        }
    }
    
    updatePlayerScore(score) {
        this.elements.gameScore.textContent = `Score: ${score}`;
    }
    
    showTemporaryMessage(message, type = 'info', duration = 3000) {
        // Create temporary alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at the top of the game area
        const gameArea = document.querySelector('.col-lg-8');
        gameArea.insertBefore(alert, gameArea.firstChild);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, duration);
    }
}
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TriviaGameClient();
});
