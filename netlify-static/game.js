// AWS Trivia Game - Static Version for Netlify
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
        
        this.initializeGame();
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
        
        // Shuffle questions and select 10
        this.gameQuestions = this.shuffleArray([...questions]).slice(0, 10);
        this.currentQuestionIndex = 0;
        this.score = 0;
        
        // Show game screen
        document.getElementById('welcomeScreen').style.display = 'none';
        document.getElementById('gameScreen').style.display = 'block';
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
        
        // Create option buttons
        const optionsContainer = document.getElementById('optionsContainer');
        optionsContainer.innerHTML = '';
        
        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'btn option-btn';
            button.innerHTML = `<strong>${String.fromCharCode(65 + index)}.</strong> ${option}`;
            button.addEventListener('click', () => this.selectAnswer(index, button));
            optionsContainer.appendChild(button);
        });
        
        // Update progress
        const progress = ((this.currentQuestionIndex) / this.gameQuestions.length) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
        document.getElementById('currentQuestion').textContent = this.currentQuestionIndex;
        
        // Hide feedback
        document.getElementById('answerFeedback').style.display = 'none';
        
        // Start timer
        this.startTimer();
    }
    
    startTimer() {
        this.timeLeft = 15;
        document.getElementById('timeLeft').textContent = this.timeLeft;
        document.getElementById('timer').className = 'badge bg-warning fs-6';
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            document.getElementById('timeLeft').textContent = this.timeLeft;
            
            if (this.timeLeft <= 5) {
                document.getElementById('timer').className = 'badge bg-danger fs-6 timer-warning';
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
        
        // Remove previous selection
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
            btn.disabled = true;
        });
        
        // Mark selection
        buttonElement.classList.add('selected');
        
        this.checkAnswer();
    }
    
    checkAnswer() {
        const question = this.gameQuestions[this.currentQuestionIndex];
        const correct = this.selectedAnswer === question.answer;
        
        if (correct) {
            this.score++;
            document.getElementById('currentScore').textContent = this.score;
        }
        
        // Show feedback
        this.showFeedback(correct, question);
        
        // Highlight correct/incorrect answers
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
        
        if (timeout) {
            feedbackElement.className = 'alert alert-warning';
            titleElement.innerHTML = '<i class="fas fa-clock"></i> Time\'s Up!';
            textElement.textContent = `The correct answer was: ${question.options[question.answer]}`;
        } else if (correct) {
            feedbackElement.className = 'alert alert-success';
            titleElement.innerHTML = '<i class="fas fa-check-circle"></i> Correct!';
            textElement.textContent = `Great job! The answer was: ${question.options[question.answer]}`;
        } else {
            feedbackElement.className = 'alert alert-danger';
            titleElement.innerHTML = '<i class="fas fa-times-circle"></i> Incorrect';
            textElement.innerHTML = `
                Your answer: ${question.options[this.selectedAnswer]}<br>
                Correct answer: ${question.options[question.answer]}
            `;
        }
    }
    
    endGame() {
        // Hide game screen
        document.getElementById('gameScreen').style.display = 'none';
        document.getElementById('gameOverScreen').style.display = 'block';
        
        // Show final score
        const percentage = Math.round((this.score / this.gameQuestions.length) * 100);
        document.getElementById('finalScore').textContent = 
            `${this.score} out of ${this.gameQuestions.length} (${percentage}%)`;
        
        // Show score message
        let message = '';
        if (percentage >= 90) {
            message = `🏆 Excellent work, ${this.playerName}! You're an AWS expert! Thanks for participating in the AWS Community Challenge!`;
        } else if (percentage >= 70) {
            message = `👏 Great job, ${this.playerName}! You have solid AWS knowledge! Keep learning with the AWS Community!`;
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
        
        // Show welcome screen
        document.getElementById('welcomeScreen').style.display = 'block';
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
