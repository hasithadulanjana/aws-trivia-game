// AWS Trivia Game - Static Version for Netlify with Animations and Sounds
class StaticTriviaGame {
    constructor() {
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.playerName = '';
        this.gameQuestions = [];
        this.selectedAnswer = null;
        this.answered = false;
        this.timer = null;
        this.timeLeft = 15;
        
        // Sound effects
        this.sounds = {
            correct: this.createSound(800, 0.3, 'sine'),
            incorrect: this.createSound(300, 0.5, 'sawtooth'),
            tick: this.createSound(600, 0.1, 'square'),
            gameStart: this.createSound(440, 0.5, 'sine'),
            gameEnd: this.createSound(523, 1, 'sine')
        };
        
        this.initializeGame();
    }
    
    // Create sound effects using Web Audio API
    createSound(frequency, duration, type = 'sine') {
        return () => {
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.value = frequency;
                oscillator.type = type;
                
                gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + duration);
            } catch (error) {
                console.log('Audio not supported');
            }
        };
    }
    
    // Play celebration sound sequence
    playCelebrationSound() {
        const notes = [523, 659, 784, 1047]; // C, E, G, C
        notes.forEach((note, index) => {
            setTimeout(() => {
                this.createSound(note, 0.3, 'sine')();
            }, index * 200);
        });
    }
    
    // Create confetti animation
    createConfetti() {
        const colors = ['#f39c12', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6'];
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.animationDelay = Math.random() * 3 + 's';
                document.body.appendChild(confetti);
                
                setTimeout(() => {
                    confetti.remove();
                }, 3000);
            }, i * 50);
        }
    }
    
    initializeGame() {
        // Event listeners
        document.getElementById('startForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startGame();
        });
        
        document.getElementById('playAgainBtn').addEventListener('click', () => {
            this.resetGame();
        });
    }
    
    startGame() {
        this.playerName = document.getElementById('playerName').value.trim();
        if (!this.playerName) {
            alert('Please enter your name');
            return;
        }
        
        // Play game start sound
        this.sounds.gameStart();
        
        // Shuffle questions and select 10
        this.gameQuestions = this.shuffleArray([...questions]).slice(0, 10);
        this.currentQuestionIndex = 0;
        this.score = 0;
        
        // Show game screen with animation
        document.getElementById('welcomeScreen').style.display = 'none';
        const gameScreen = document.getElementById('gameScreen');
        gameScreen.style.display = 'block';
        gameScreen.classList.add('welcome-animation');
        document.getElementById('gameOverScreen').style.display = 'none';
        
        // Update UI
        document.getElementById('totalQuestions').textContent = this.gameQuestions.length;
        document.getElementById('totalQuestionsProgress').textContent = this.gameQuestions.length;
        
        this.showQuestion();
    }
    
    shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
    
    showQuestion() {
        if (this.currentQuestionIndex >= this.gameQuestions.length) {
            this.endGame();
            return;
        }
        
        const question = this.gameQuestions[this.currentQuestionIndex];
        this.selectedAnswer = null;
        this.answered = false;
        
        // Update question display
        document.getElementById('questionNumber').textContent = 
            `Question ${this.currentQuestionIndex + 1} of ${this.gameQuestions.length}`;
        document.getElementById('questionText').textContent = question.question;
        
        // Create option buttons with staggered animation
        const optionsContainer = document.getElementById('optionsContainer');
        optionsContainer.innerHTML = '';
        
        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'btn option-btn';
            button.innerHTML = `<strong>${String.fromCharCode(65 + index)}.</strong> ${option}`;
            button.style.animationDelay = `${index * 0.1}s`;
            button.addEventListener('click', () => this.selectAnswer(index, button));
            optionsContainer.appendChild(button);
        });
        
        // Update progress with animation
        const progress = ((this.currentQuestionIndex) / this.gameQuestions.length) * 100;
        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = `${progress}%`;
        progressBar.style.transition = 'width 0.5s ease-in-out';
        document.getElementById('currentQuestion').textContent = this.currentQuestionIndex;
        
        // Hide feedback
        document.getElementById('answerFeedback').style.display = 'none';
        
        // Start timer
        this.startTimer();
    }
    
    startTimer() {
        this.timeLeft = 15;
        const timerElement = document.getElementById('timeLeft');
        const timerBadge = document.getElementById('timer');
        
        timerElement.textContent = this.timeLeft;
        timerBadge.className = 'badge bg-warning fs-6';
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            timerElement.textContent = this.timeLeft;
            
            // Play tick sound for last 5 seconds
            if (this.timeLeft <= 5 && this.timeLeft > 0) {
                this.sounds.tick();
                timerBadge.className = 'badge bg-danger fs-6 timer-warning';
            }
            
            if (this.timeLeft <= 0) {
                clearInterval(this.timer);
                this.handleTimeout();
            }
        }, 1000);
    }
    
    selectAnswer(index, buttonElement) {
        if (this.answered) return;
        
        clearInterval(this.timer);
        this.answered = true;
        this.selectedAnswer = index;
        
        // Remove previous selection and add selection animation
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
            btn.disabled = true;
        });
        
        // Mark selection with animation
        buttonElement.classList.add('selected');
        
        this.checkAnswer();
    }
    
    checkAnswer() {
        const question = this.gameQuestions[this.currentQuestionIndex];
        const correct = this.selectedAnswer === question.answer;
        
        if (correct) {
            this.score++;
            this.sounds.correct();
            // Animate score update
            const scoreElement = document.getElementById('currentScore');
            scoreElement.textContent = this.score;
            scoreElement.classList.add('score-animation');
            setTimeout(() => scoreElement.classList.remove('score-animation'), 800);
        } else {
            this.sounds.incorrect();
        }
        
        // Show feedback
        this.showFeedback(correct, question);
        
        // Highlight correct/incorrect answers with animations
        document.querySelectorAll('.option-btn').forEach((btn, index) => {
            if (index === question.answer) {
                btn.classList.add('correct');
            } else if (index === this.selectedAnswer && !correct) {
                btn.classList.add('incorrect');
            }
        });
        
        // Move to next question after delay
        setTimeout(() => {
            this.currentQuestionIndex++;
            this.showQuestion();
        }, 3000);
    }
    
    handleTimeout() {
        if (this.answered) return;
        
        this.answered = true;
        const question = this.gameQuestions[this.currentQuestionIndex];
        
        // Play timeout sound
        this.sounds.incorrect();
        
        // Disable all buttons
        document.querySelectorAll('.option-btn').forEach((btn, index) => {
            btn.disabled = true;
            if (index === question.answer) {
                btn.classList.add('correct');
            }
        });
        
        // Show timeout feedback
        this.showFeedback(false, question, true);
        
        // Move to next question after delay
        setTimeout(() => {
            this.currentQuestionIndex++;
            this.showQuestion();
        }, 3000);
    }
    
    showFeedback(correct, question, timeout = false) {
        const feedbackElement = document.getElementById('answerFeedback');
        const titleElement = document.getElementById('feedbackTitle');
        const textElement = document.getElementById('feedbackText');
        
        feedbackElement.style.display = 'block';
        feedbackElement.classList.add('welcome-animation');
        
        if (timeout) {
            feedbackElement.className = 'alert alert-warning welcome-animation';
            titleElement.innerHTML = '<i class="fas fa-clock"></i> Time\'s Up!';
            textElement.textContent = `The correct answer was: ${question.options[question.answer]}`;
        } else if (correct) {
            feedbackElement.className = 'alert alert-success welcome-animation';
            titleElement.innerHTML = '<i class="fas fa-check-circle"></i> Correct!';
            textElement.textContent = `Great job! The answer was: ${question.options[question.answer]}`;
        } else {
            feedbackElement.className = 'alert alert-danger welcome-animation';
            titleElement.innerHTML = '<i class="fas fa-times-circle"></i> Incorrect';
            textElement.innerHTML = `
                Your answer: ${question.options[this.selectedAnswer]}<br>
                Correct answer: ${question.options[question.answer]}
            `;
        }
    }
    
    endGame() {
        // Play game end sound
        this.sounds.gameEnd();
        
        // Hide game screen
        document.getElementById('gameScreen').style.display = 'none';
        const gameOverScreen = document.getElementById('gameOverScreen');
        gameOverScreen.style.display = 'block';
        gameOverScreen.classList.add('welcome-animation');
        
        // Show final score
        const percentage = Math.round((this.score / this.gameQuestions.length) * 100);
        document.getElementById('finalScore').textContent = 
            `${this.score} out of ${this.gameQuestions.length} (${percentage}%)`;
        
        // Show score message with celebration for high scores
        let message = '';
        if (percentage >= 90) {
            message = `🏆 Excellent work, ${this.playerName}! You're an AWS expert! Thanks for participating in the AWS Community Challenge!`;
            this.playCelebrationSound();
            this.createConfetti();
        } else if (percentage >= 70) {
            message = `👏 Great job, ${this.playerName}! You have solid AWS knowledge! Keep learning with the AWS Community!`;
            this.playCelebrationSound();
        } else if (percentage >= 50) {
            message = `👍 Good effort, ${this.playerName}! Keep learning about AWS with the community!`;
        } else {
            message = `📚 Keep studying, ${this.playerName}! AWS has lots to learn - join the AWS Community for more resources!`;
        }
        
        document.getElementById('scoreMessage').textContent = message;
    }
    
    resetGame() {
        // Reset game state
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.selectedAnswer = null;
        this.answered = false;
        
        // Clear timer
        if (this.timer) {
            clearInterval(this.timer);
        }
        
        // Show welcome screen with animation
        const welcomeScreen = document.getElementById('welcomeScreen');
        welcomeScreen.style.display = 'block';
        welcomeScreen.classList.add('welcome-animation');
        document.getElementById('gameScreen').style.display = 'none';
        document.getElementById('gameOverScreen').style.display = 'none';
        
        // Reset form
        document.getElementById('playerName').value = '';
        document.getElementById('currentScore').textContent = '0';
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    new StaticTriviaGame();
});
