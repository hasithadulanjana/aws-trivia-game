/**
 * AWS Trivia Interactive Game Engine
 * Features shooting mechanics, particle effects, and interactive gameplay
 */

class GameEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width = window.innerWidth * 0.8;
        this.height = this.canvas.height = window.innerHeight * 0.6;
        
        // Game state
        this.gameState = 'menu'; // menu, playing, paused, gameOver
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        this.timeLeft = 60;
        
        // Game objects
        this.player = new Player(this.width / 2, this.height - 100);
        this.bullets = [];
        this.targets = [];
        this.particles = [];
        this.powerUps = [];
        this.explosions = [];
        
        // Input handling
        this.keys = {};
        this.mouse = { x: 0, y: 0, clicked: false };
        
        // Game settings
        this.targetSpawnRate = 0.02;
        this.powerUpSpawnRate = 0.005;
        
        // Current question data
        this.currentQuestion = null;
        this.questionTargets = [];
        
        this.initializeEventListeners();
        this.gameLoop();
    }
    
    initializeEventListeners() {
        // Keyboard events
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            
            // Shooting with spacebar or continue
            if (e.code === 'Space') {
                e.preventDefault();
                if (this.gameState === 'playing') {
                    this.player.shoot(this.bullets);
                } else if (this.gameState === 'waiting_continue') {
                    this.handleContinueInput();
                }
            }
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
        
        // Mouse events
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('click', (e) => {
            if (this.gameState === 'playing') {
                this.player.shootAt(this.mouse.x, this.mouse.y, this.bullets);
            } else if (this.gameState === 'waiting_continue') {
                this.handleContinueInput();
            }
        });
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            const rect = this.canvas.getBoundingClientRect();
            const touch = e.touches[0];
            this.mouse.x = touch.clientX - rect.left;
            this.mouse.y = touch.clientY - rect.top;
            
            if (this.gameState === 'playing') {
                this.player.shootAt(this.mouse.x, this.mouse.y, this.bullets);
            } else if (this.gameState === 'waiting_continue') {
                this.handleContinueInput();
            }
        });
        
        // Resize handling
        window.addEventListener('resize', () => {
            this.width = this.canvas.width = window.innerWidth * 0.8;
            this.height = this.canvas.height = window.innerHeight * 0.6;
        });
    }
    
    gameLoop() {
        this.update();
        this.render();
        requestAnimationFrame(() => this.gameLoop());
    }
    
    update() {
        if (this.gameState !== 'playing' && this.gameState !== 'waiting_continue') return;
        
        // Update player (only if playing, not waiting)
        if (this.gameState === 'playing') {
            this.player.update(this.keys, this.width, this.height);
        }
        
        // Always update visual effects
        // Update bullets
        this.bullets.forEach((bullet, index) => {
            bullet.update();
            if (bullet.y < 0 || bullet.x < 0 || bullet.x > this.width) {
                this.bullets.splice(index, 1);
            }
        });
        
        // Update targets (only if playing)
        if (this.gameState === 'playing') {
            this.targets.forEach((target, index) => {
                target.update();
                if (target.y > this.height + 50) {
                    this.targets.splice(index, 1);
                }
            });
        }
        
        // Update particles
        this.particles.forEach((particle, index) => {
            particle.update();
            if (particle.life <= 0) {
                this.particles.splice(index, 1);
            }
        });
        
        // Update explosions
        this.explosions.forEach((explosion, index) => {
            explosion.update();
            if (explosion.finished) {
                this.explosions.splice(index, 1);
            }
        });
        
        // Update continue prompt pulse
        if (this.continuePrompt && this.continuePrompt.active) {
            this.continuePrompt.pulse += 0.1;
        }
        
        // Check collisions (only if playing)
        if (this.gameState === 'playing') {
            this.checkCollisions();
            
            // Spawn new targets (question options)
            if (this.currentQuestion && this.questionTargets.length === 0) {
                this.spawnQuestionTargets();
            }
            
            // Update timer
            this.timeLeft -= 1/60; // Assuming 60 FPS
            if (this.timeLeft <= 0) {
                this.gameOver();
            }
        }
    }
    
    render() {
        // Clear canvas with gradient background
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.height);
        gradient.addColorStop(0, '#1a1a2e');
        gradient.addColorStop(0.5, '#16213e');
        gradient.addColorStop(1, '#0f3460');
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw stars background
        this.drawStars();
        
        if (this.gameState === 'playing' || this.gameState === 'waiting_continue') {
            // Draw game objects
            this.particles.forEach(particle => particle.render(this.ctx));
            this.targets.forEach(target => target.render(this.ctx));
            this.bullets.forEach(bullet => bullet.render(this.ctx));
            this.explosions.forEach(explosion => explosion.render(this.ctx));
            this.player.render(this.ctx);
            
            // Draw UI
            this.drawUI();
            
            // Draw question (only if playing)
            if (this.currentQuestion && this.gameState === 'playing') {
                this.drawQuestion();
            }
            
            // Draw continue prompt if waiting
            if (this.gameState === 'waiting_continue') {
                this.drawContinuePrompt();
            }
        } else if (this.gameState === 'menu') {
            this.drawMenu();
        } else if (this.gameState === 'gameOver') {
            this.drawGameOver();
        }
    }
    
    drawStars() {
        this.ctx.fillStyle = 'white';
        for (let i = 0; i < 100; i++) {
            const x = (i * 37) % this.width;
            const y = (i * 73) % this.height;
            const size = Math.random() * 2;
            this.ctx.fillRect(x, y, size, size);
        }
    }
    
    drawUI() {
        this.ctx.fillStyle = 'white';
        this.ctx.font = '20px Arial';
        
        // Score
        this.ctx.fillText(`Score: ${this.score}`, 20, 30);
        
        // Lives
        this.ctx.fillText(`Lives: ${this.lives}`, 20, 60);
        
        // Level
        this.ctx.fillText(`Level: ${this.level}`, 20, 90);
        
        // Timer
        this.ctx.fillStyle = this.timeLeft < 10 ? 'red' : 'white';
        this.ctx.fillText(`Time: ${Math.ceil(this.timeLeft)}s`, this.width - 120, 30);
        
        // Crosshair
        this.drawCrosshair();
    }
    
    drawCrosshair() {
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        
        // Horizontal line
        this.ctx.moveTo(this.mouse.x - 15, this.mouse.y);
        this.ctx.lineTo(this.mouse.x + 15, this.mouse.y);
        
        // Vertical line
        this.ctx.moveTo(this.mouse.x, this.mouse.y - 15);
        this.ctx.lineTo(this.mouse.x, this.mouse.y + 15);
        
        this.ctx.stroke();
        
        // Center dot
        this.ctx.fillStyle = 'rgba(255, 0, 0, 0.8)';
        this.ctx.beginPath();
        this.ctx.arc(this.mouse.x, this.mouse.y, 3, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    drawQuestion() {
        if (!this.currentQuestion) return;
        
        // Question background
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        this.ctx.fillRect(50, 50, this.width - 100, 120);
        
        this.ctx.strokeStyle = '#00ff00';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(50, 50, this.width - 100, 120);
        
        // Question text
        this.ctx.fillStyle = 'white';
        this.ctx.font = '18px Arial';
        this.ctx.textAlign = 'center';
        
        const questionText = this.wrapText(this.currentQuestion.question, this.width - 120);
        questionText.forEach((line, index) => {
            this.ctx.fillText(line, this.width / 2, 80 + (index * 25));
        });
        
        this.ctx.textAlign = 'left';
        
        // Instructions
        this.ctx.fillStyle = '#ffff00';
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('🎯 Shoot the correct answer! 🎯', this.width / 2, 200);
        this.ctx.textAlign = 'left';
    }
    
    drawMenu() {
        // Title
        this.ctx.fillStyle = '#00ff00';
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('AWS TRIVIA SHOOTER', this.width / 2, this.height / 2 - 100);
        
        // Subtitle
        this.ctx.fillStyle = 'white';
        this.ctx.font = '24px Arial';
        this.ctx.fillText('Shoot the correct answers to score points!', this.width / 2, this.height / 2 - 50);
        
        // Instructions
        this.ctx.font = '18px Arial';
        this.ctx.fillStyle = '#ffff00';
        this.ctx.fillText('🎮 Controls:', this.width / 2, this.height / 2);
        this.ctx.fillText('• Move: Arrow Keys or WASD', this.width / 2, this.height / 2 + 30);
        this.ctx.fillText('• Shoot: Click or Spacebar', this.width / 2, this.height / 2 + 60);
        this.ctx.fillText('• Mobile: Touch to move and shoot', this.width / 2, this.height / 2 + 90);
        
        // Start button
        this.ctx.fillStyle = '#ff6600';
        this.ctx.fillRect(this.width / 2 - 100, this.height / 2 + 130, 200, 50);
        this.ctx.fillStyle = 'white';
        this.ctx.font = 'bold 20px Arial';
        this.ctx.fillText('START GAME', this.width / 2, this.height / 2 + 160);
        
        this.ctx.textAlign = 'left';
    }
    
    drawGameOver() {
        // Game Over background
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Game Over text
        this.ctx.fillStyle = '#ff0000';
        this.ctx.font = 'bold 48px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('GAME OVER', this.width / 2, this.height / 2 - 100);
        
        // Final score
        this.ctx.fillStyle = 'white';
        this.ctx.font = '24px Arial';
        this.ctx.fillText(`Final Score: ${this.score}`, this.width / 2, this.height / 2 - 50);
        this.ctx.fillText(`Level Reached: ${this.level}`, this.width / 2, this.height / 2 - 20);
        
        // Play again button
        this.ctx.fillStyle = '#00ff00';
        this.ctx.fillRect(this.width / 2 - 100, this.height / 2 + 20, 200, 50);
        this.ctx.fillStyle = 'black';
        this.ctx.font = 'bold 20px Arial';
        this.ctx.fillText('PLAY AGAIN', this.width / 2, this.height / 2 + 50);
        
        this.ctx.textAlign = 'left';
    }
    
    drawContinuePrompt() {
        if (!this.continuePrompt || !this.continuePrompt.active) return;
        
        // Pulsing background
        const pulse = Math.sin(this.continuePrompt.pulse) * 0.3 + 0.7;
        this.ctx.fillStyle = `rgba(255, 255, 0, ${pulse * 0.3})`;
        this.ctx.fillRect(0, this.height - 150, this.width, 150);
        
        // Continue message
        this.ctx.fillStyle = '#ffff00';
        this.ctx.font = 'bold 32px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('READY FOR NEXT QUESTION?', this.width / 2, this.height - 100);
        
        // Instructions with pulsing effect
        this.ctx.fillStyle = `rgba(255, 255, 255, ${pulse})`;
        this.ctx.font = 'bold 24px Arial';
        this.ctx.fillText('Press SPACE or CLICK to continue', this.width / 2, this.height - 60);
        
        // Visual indicator
        const indicatorSize = 10 + Math.sin(this.continuePrompt.pulse * 2) * 5;
        this.ctx.fillStyle = `rgba(255, 255, 0, ${pulse})`;
        this.ctx.beginPath();
        this.ctx.arc(this.width / 2, this.height - 30, indicatorSize, 0, Math.PI * 2);
        this.ctx.fill();
        
        this.ctx.textAlign = 'left';
    }
    
    checkCollisions() {
        // Bullet-Target collisions
        for (let bulletIndex = this.bullets.length - 1; bulletIndex >= 0; bulletIndex--) {
            const bullet = this.bullets[bulletIndex];
            let bulletHit = false;
            
            for (let targetIndex = this.targets.length - 1; targetIndex >= 0; targetIndex--) {
                const target = this.targets[targetIndex];
                
                if (this.isColliding(bullet, target)) {
                    // Create explosion
                    this.explosions.push(new Explosion(target.x, target.y));
                    
                    // Create particles
                    this.createParticles(target.x, target.y, target.isCorrect ? '#00ff00' : '#ff0000');
                    
                    // Handle scoring
                    if (target.isCorrect) {
                        this.score += 100;
                        this.correctAnswer();
                        
                        // Correct answer hit - clear all remaining targets and show continue prompt
                        this.clearAllTargets();
                        this.showContinuePrompt();
                        
                        // Remove the bullet that hit the correct answer
                        this.bullets.splice(bulletIndex, 1);
                        bulletHit = true;
                        break; // Exit target loop since we're clearing all targets
                        
                    } else {
                        this.lives--;
                        this.wrongAnswer();
                        
                        // Wrong answer - remove this target and bullet
                        this.bullets.splice(bulletIndex, 1);
                        this.targets.splice(targetIndex, 1);
                        
                        // Remove from question targets
                        const qtIndex = this.questionTargets.indexOf(target);
                        if (qtIndex > -1) {
                            this.questionTargets.splice(qtIndex, 1);
                        }
                        
                        bulletHit = true;
                        break; // Exit target loop for this bullet
                    }
                }
            }
            
            // If bullet hit something, continue to next bullet
            if (bulletHit) {
                continue;
            }
        }
        
        // Check if all question targets are gone (for wrong answers only)
        if (this.currentQuestion && this.questionTargets.length === 0 && this.targets.length === 0 && this.gameState === 'playing') {
            // All wrong answers were shot, but correct answer wasn't found
            // This shouldn't happen in normal gameplay, but handle it gracefully
            this.showContinuePrompt();
        }
        
        // Check game over conditions
        if (this.lives <= 0) {
            this.gameOver();
        }
    }
    
    clearAllTargets() {
        // Create fade-out effect for remaining targets
        this.targets.forEach(target => {
            if (!target.isCorrect) {
                // Create small particle effect for cleared targets
                this.createParticles(target.x, target.y, '#888888');
            }
        });
        
        // Clear all targets and question targets
        this.targets = [];
        this.questionTargets = [];
        
        // Remove any remaining bullets
        this.bullets = [];
    }
    
    showContinuePrompt() {
        // Change game state to waiting
        this.gameState = 'waiting_continue';
        
        // Show continue message with instructions
        this.showMessage('Press SPACE or CLICK to continue', '#ffff00');
        
        // Create pulsing continue indicator
        this.continuePrompt = {
            active: true,
            pulse: 0,
            x: this.width / 2,
            y: this.height - 100
        };
    }
    
    handleContinueInput() {
        if (this.gameState === 'waiting_continue') {
            this.gameState = 'playing';
            this.continuePrompt = null;
            
            // Add a brief delay before next question for smooth transition
            setTimeout(() => {
                this.nextQuestion();
            }, 500);
        }
    }
    
    isColliding(obj1, obj2) {
        const dx = obj1.x - obj2.x;
        const dy = obj1.y - obj2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < (obj1.radius + obj2.radius);
    }
    
    createParticles(x, y, color) {
        for (let i = 0; i < 15; i++) {
            this.particles.push(new Particle(x, y, color));
        }
    }
    
    spawnQuestionTargets() {
        if (!this.currentQuestion) return;
        
        this.questionTargets = [];
        const options = this.currentQuestion.options;
        const correctAnswer = this.currentQuestion.answer;
        
        // Create targets for each option
        options.forEach((option, index) => {
            const x = (this.width / (options.length + 1)) * (index + 1);
            const y = 100 + Math.random() * 100;
            const isCorrect = index === correctAnswer;
            
            const target = new Target(x, y, option, isCorrect);
            this.targets.push(target);
            this.questionTargets.push(target);
        });
    }
    
    correctAnswer() {
        // Play success sound
        this.playSound('correct');
        
        // Add bonus particles at center and around the screen
        this.createParticles(this.width / 2, this.height / 2, '#ffff00');
        this.createParticles(this.width / 4, this.height / 3, '#00ff00');
        this.createParticles(3 * this.width / 4, this.height / 3, '#00ff00');
        
        // Show success message
        this.showMessage('CORRECT! +100 points', '#00ff00');
        
        // Create celebration effect
        this.createCelebrationEffect();
        
        // Show brief pause message before continue prompt
        setTimeout(() => {
            this.showMessage('Great job! Take a moment to review...', '#ffffff');
        }, 1000);
    }
    
    createCelebrationEffect() {
        // Create a burst of golden particles
        for (let i = 0; i < 25; i++) {
            const angle = (i / 25) * Math.PI * 2;
            const speed = 5 + Math.random() * 5;
            const particle = {
                x: this.width / 2,
                y: this.height / 2,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                color: '#ffd700',
                life: 60,
                maxLife: 60,
                size: 3 + Math.random() * 3
            };
            this.particles.push(particle);
        }
    }
    
    wrongAnswer() {
        // Play error sound
        this.playSound('wrong');
        
        // Screen shake effect
        this.screenShake();
        
        // Show error message
        this.showMessage('WRONG! -1 life', '#ff0000');
    }
    
    nextQuestion() {
        // Clear current question state
        this.currentQuestion = null;
        this.questionTargets = [];
        
        // Increase difficulty
        if (this.score > 0 && this.score % 500 === 0) {
            this.level++;
            this.targetSpawnRate += 0.01;
            this.showMessage(`LEVEL UP! Level ${this.level}`, '#ffff00');
        }
        
        // Trigger event for next question loading
        if (this.onQuestionComplete) {
            this.onQuestionComplete();
        }
        
        // Show brief pause message
        this.showMessage('Get Ready...', '#ffffff');
    }
    
    loadQuestion(questionData) {
        this.currentQuestion = questionData;
        this.questionTargets = [];
        
        // Clear any existing targets and bullets
        this.targets = [];
        this.bullets = [];
        
        // Show question loading effect
        this.showMessage('New Question!', '#00ffff');
        
        // Create loading particles
        this.createParticles(this.width / 2, this.height / 4, '#00ffff');
    }
    
    startGame() {
        this.gameState = 'playing';
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        this.timeLeft = 60;
        this.bullets = [];
        this.targets = [];
        this.particles = [];
        this.explosions = [];
        this.questionTargets = [];
    }
    
    gameOver() {
        this.gameState = 'gameOver';
        this.playSound('gameOver');
    }
    
    playSound(type) {
        // Web Audio API sound generation
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        switch (type) {
            case 'correct':
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
                break;
            case 'wrong':
                oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(100, audioContext.currentTime + 0.3);
                break;
            case 'shoot':
                oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.1);
                break;
            case 'gameOver':
                oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(50, audioContext.currentTime + 1);
                break;
        }
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    }
    
    screenShake() {
        const originalTransform = this.canvas.style.transform;
        let shakeCount = 0;
        const maxShakes = 10;
        
        const shake = () => {
            if (shakeCount < maxShakes) {
                const x = (Math.random() - 0.5) * 10;
                const y = (Math.random() - 0.5) * 10;
                this.canvas.style.transform = `translate(${x}px, ${y}px)`;
                shakeCount++;
                setTimeout(shake, 50);
            } else {
                this.canvas.style.transform = originalTransform;
            }
        };
        
        shake();
    }
    
    showMessage(text, color) {
        // Create floating message
        const message = {
            text: text,
            x: this.width / 2,
            y: this.height / 2,
            color: color,
            life: 60,
            maxLife: 60
        };
        
        const renderMessage = () => {
            if (message.life > 0) {
                this.ctx.save();
                this.ctx.fillStyle = message.color;
                this.ctx.font = 'bold 24px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.globalAlpha = message.life / message.maxLife;
                this.ctx.fillText(message.text, message.x, message.y - (60 - message.life));
                this.ctx.restore();
                
                message.life--;
                requestAnimationFrame(renderMessage);
            }
        };
        
        renderMessage();
    }
    
    wrapText(text, maxWidth) {
        const words = text.split(' ');
        const lines = [];
        let currentLine = '';
        
        this.ctx.font = '18px Arial';
        
        for (let word of words) {
            const testLine = currentLine + word + ' ';
            const metrics = this.ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && currentLine !== '') {
                lines.push(currentLine.trim());
                currentLine = word + ' ';
            } else {
                currentLine = testLine;
            }
        }
        
        lines.push(currentLine.trim());
        return lines;
    }
}

// Game object classes
class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 20;
        this.speed = 5;
        this.color = '#00ff00';
    }
    
    update(keys, canvasWidth, canvasHeight) {
        // Movement
        if (keys['ArrowLeft'] || keys['KeyA']) {
            this.x -= this.speed;
        }
        if (keys['ArrowRight'] || keys['KeyD']) {
            this.x += this.speed;
        }
        if (keys['ArrowUp'] || keys['KeyW']) {
            this.y -= this.speed;
        }
        if (keys['ArrowDown'] || keys['KeyS']) {
            this.y += this.speed;
        }
        
        // Keep player in bounds
        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(this.radius, Math.min(canvasHeight - this.radius, this.y));
    }
    
    render(ctx) {
        // Player ship
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Ship details
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(this.x, this.y - 5, 5, 0, Math.PI * 2);
        ctx.fill();
        
        // Thruster effect
        ctx.fillStyle = '#ff6600';
        ctx.fillRect(this.x - 3, this.y + 15, 6, 10);
    }
    
    shoot(bullets) {
        bullets.push(new Bullet(this.x, this.y - this.radius, 0, -10));
        // Play shoot sound would go here
    }
    
    shootAt(targetX, targetY, bullets) {
        const dx = targetX - this.x;
        const dy = targetY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        const speed = 12;
        const vx = (dx / distance) * speed;
        const vy = (dy / distance) * speed;
        
        bullets.push(new Bullet(this.x, this.y, vx, vy));
    }
}

class Bullet {
    constructor(x, y, vx, vy) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radius = 3;
        this.color = '#ffff00';
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
    }
    
    render(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Bullet trail
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.x - this.vx, this.y - this.vy);
        ctx.lineTo(this.x, this.y);
        ctx.stroke();
    }
}

class Target {
    constructor(x, y, text, isCorrect) {
        this.x = x;
        this.y = y;
        this.text = text;
        this.isCorrect = isCorrect;
        this.radius = 40;
        this.speed = 1;
        this.color = isCorrect ? '#00ff00' : '#ff6600';
        this.pulsePhase = Math.random() * Math.PI * 2;
    }
    
    update() {
        this.y += this.speed;
        this.pulsePhase += 0.1;
    }
    
    render(ctx) {
        // Pulsing effect
        const pulse = Math.sin(this.pulsePhase) * 5;
        const currentRadius = this.radius + pulse;
        
        // Target circle
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, currentRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Border
        ctx.strokeStyle = this.isCorrect ? '#ffffff' : '#ffff00';
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Text
        ctx.fillStyle = 'white';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        
        // Wrap text for long options
        const maxWidth = this.radius * 1.5;
        const words = this.text.split(' ');
        let lines = [];
        let currentLine = '';
        
        for (let word of words) {
            const testLine = currentLine + word + ' ';
            const metrics = ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && currentLine !== '') {
                lines.push(currentLine.trim());
                currentLine = word + ' ';
            } else {
                currentLine = testLine;
            }
        }
        lines.push(currentLine.trim());
        
        // Draw text lines
        const lineHeight = 14;
        const startY = this.y - (lines.length - 1) * lineHeight / 2;
        
        lines.forEach((line, index) => {
            ctx.fillText(line, this.x, startY + index * lineHeight);
        });
        
        ctx.textAlign = 'left';
    }
}

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 10;
        this.vy = (Math.random() - 0.5) * 10;
        this.color = color;
        this.life = 30;
        this.maxLife = 30;
        this.size = Math.random() * 4 + 2;
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.2; // Gravity
        this.life--;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.life / this.maxLife;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

class Explosion {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 0;
        this.maxRadius = 50;
        this.life = 20;
        this.maxLife = 20;
        this.finished = false;
    }
    
    update() {
        this.radius += 3;
        this.life--;
        
        if (this.life <= 0) {
            this.finished = true;
        }
    }
    
    render(ctx) {
        if (this.finished) return;
        
        ctx.save();
        ctx.globalAlpha = this.life / this.maxLife;
        
        // Outer ring
        ctx.strokeStyle = '#ff6600';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.stroke();
        
        // Inner ring
        ctx.strokeStyle = '#ffff00';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 0.7, 0, Math.PI * 2);
        ctx.stroke();
        
        ctx.restore();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GameEngine;
} else if (typeof window !== 'undefined') {
    window.GameEngine = GameEngine;
}
