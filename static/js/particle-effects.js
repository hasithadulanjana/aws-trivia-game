/**
 * Advanced Particle Effects Library for AWS Trivia Game
 * Creates stunning visual effects for correct/wrong answers, explosions, and achievements
 */

class ParticleSystem {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.particles = [];
        this.emitters = [];
    }
    
    update() {
        // Update particles
        this.particles.forEach((particle, index) => {
            particle.update();
            if (particle.isDead()) {
                this.particles.splice(index, 1);
            }
        });
        
        // Update emitters
        this.emitters.forEach((emitter, index) => {
            emitter.update();
            if (emitter.isDead()) {
                this.emitters.splice(index, 1);
            }
        });
    }
    
    render() {
        this.particles.forEach(particle => particle.render(this.ctx));
        this.emitters.forEach(emitter => emitter.render(this.ctx));
    }
    
    // Effect creators
    createCorrectAnswerEffect(x, y) {
        // Green sparkles and stars
        for (let i = 0; i < 20; i++) {
            this.particles.push(new SparkleParticle(x, y, '#00ff00'));
        }
        
        // Success burst
        this.emitters.push(new BurstEmitter(x, y, {
            color: '#00ff00',
            particleCount: 15,
            speed: 8,
            life: 60
        }));
        
        // Floating text
        this.particles.push(new FloatingText(x, y, 'CORRECT!', '#00ff00', 48));
        
        // Ring explosion
        this.particles.push(new RingExplosion(x, y, '#00ff00', 100));
    }
    
    createWrongAnswerEffect(x, y) {
        // Red sparks and smoke
        for (let i = 0; i < 15; i++) {
            this.particles.push(new SmokeParticle(x, y, '#ff0000'));
        }
        
        // Error burst
        this.emitters.push(new BurstEmitter(x, y, {
            color: '#ff0000',
            particleCount: 12,
            speed: 6,
            life: 45
        }));
        
        // Floating text
        this.particles.push(new FloatingText(x, y, 'WRONG!', '#ff0000', 36));
        
        // Screen shake effect
        this.createScreenShake();
    }
    
    createPowerUpEffect(x, y) {
        // Golden particles
        for (let i = 0; i < 25; i++) {
            this.particles.push(new GoldenParticle(x, y));
        }
        
        // Power-up aura
        this.particles.push(new AuraEffect(x, y, '#ffff00', 80));
        
        // Floating text
        this.particles.push(new FloatingText(x, y, 'POWER UP!', '#ffff00', 32));
    }
    
    createLevelUpEffect(x, y) {
        // Rainbow explosion
        const colors = ['#ff0000', '#ff8800', '#ffff00', '#00ff00', '#0088ff', '#8800ff'];
        
        for (let i = 0; i < 30; i++) {
            const color = colors[i % colors.length];
            this.particles.push(new FireworkParticle(x, y, color));
        }
        
        // Level up text
        this.particles.push(new FloatingText(x, y, 'LEVEL UP!', '#ffff00', 56));
        
        // Confetti
        this.createConfetti(x, y);
    }
    
    createShootingEffect(startX, startY, endX, endY) {
        // Bullet trail
        this.particles.push(new BulletTrail(startX, startY, endX, endY));
        
        // Muzzle flash
        this.particles.push(new MuzzleFlash(startX, startY));
    }
    
    createExplosionEffect(x, y, size = 50) {
        // Main explosion
        this.particles.push(new ExplosionCore(x, y, size));
        
        // Debris
        for (let i = 0; i < 10; i++) {
            this.particles.push(new DebrisParticle(x, y));
        }
        
        // Shockwave
        this.particles.push(new Shockwave(x, y, size * 2));
    }
    
    createConfetti(x, y) {
        const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'];
        
        for (let i = 0; i < 50; i++) {
            const color = colors[Math.floor(Math.random() * colors.length)];
            this.particles.push(new ConfettiPiece(x, y, color));
        }
    }
    
    createScreenShake() {
        this.particles.push(new ScreenShakeEffect(this.canvas));
    }
    
    clear() {
        this.particles = [];
        this.emitters = [];
    }
}

// Particle classes
class Particle {
    constructor(x, y, color = '#ffffff') {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.color = color;
        this.life = 60;
        this.maxLife = 60;
        this.size = 2;
        this.alpha = 1;
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life--;
        this.alpha = this.life / this.maxLife;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
    
    isDead() {
        return this.life <= 0;
    }
}

class SparkleParticle extends Particle {
    constructor(x, y, color) {
        super(x, y, color);
        this.vx = (Math.random() - 0.5) * 8;
        this.vy = (Math.random() - 0.5) * 8;
        this.size = Math.random() * 4 + 2;
        this.sparkle = 0;
    }
    
    update() {
        super.update();
        this.sparkle += 0.3;
        this.size = (Math.sin(this.sparkle) + 1) * 2 + 1;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        
        // Star shape
        const spikes = 5;
        const outerRadius = this.size;
        const innerRadius = this.size / 2;
        
        ctx.beginPath();
        for (let i = 0; i < spikes * 2; i++) {
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const angle = (i * Math.PI) / spikes;
            const x = this.x + Math.cos(angle) * radius;
            const y = this.y + Math.sin(angle) * radius;
            
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
}

class SmokeParticle extends Particle {
    constructor(x, y, color) {
        super(x, y, color);
        this.vx = (Math.random() - 0.5) * 4;
        this.vy = -Math.random() * 3 - 1;
        this.size = Math.random() * 8 + 4;
        this.life = 90;
        this.maxLife = 90;
    }
    
    update() {
        super.update();
        this.size += 0.2;
        this.vy += 0.05; // Gravity
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha * 0.7;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

class GoldenParticle extends Particle {
    constructor(x, y) {
        super(x, y, '#ffd700');
        this.vx = (Math.random() - 0.5) * 6;
        this.vy = (Math.random() - 0.5) * 6;
        this.size = Math.random() * 3 + 2;
        this.rotation = 0;
        this.rotationSpeed = (Math.random() - 0.5) * 0.3;
    }
    
    update() {
        super.update();
        this.rotation += this.rotationSpeed;
        this.vy += 0.1; // Slight gravity
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // Diamond shape
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(0, -this.size);
        ctx.lineTo(this.size, 0);
        ctx.lineTo(0, this.size);
        ctx.lineTo(-this.size, 0);
        ctx.closePath();
        ctx.fill();
        
        ctx.restore();
    }
}

class FireworkParticle extends Particle {
    constructor(x, y, color) {
        super(x, y, color);
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 10 + 5;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.size = Math.random() * 4 + 2;
        this.life = 120;
        this.maxLife = 120;
        this.trail = [];
    }
    
    update() {
        // Store trail positions
        this.trail.push({ x: this.x, y: this.y });
        if (this.trail.length > 10) {
            this.trail.shift();
        }
        
        super.update();
        this.vy += 0.2; // Gravity
    }
    
    render(ctx) {
        ctx.save();
        
        // Draw trail
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = this.alpha * 0.5;
        
        if (this.trail.length > 1) {
            ctx.beginPath();
            ctx.moveTo(this.trail[0].x, this.trail[0].y);
            for (let i = 1; i < this.trail.length; i++) {
                ctx.lineTo(this.trail[i].x, this.trail[i].y);
            }
            ctx.stroke();
        }
        
        // Draw particle
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
}

class FloatingText extends Particle {
    constructor(x, y, text, color, fontSize) {
        super(x, y, color);
        this.text = text;
        this.fontSize = fontSize;
        this.vy = -2;
        this.life = 120;
        this.maxLife = 120;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.font = `bold ${this.fontSize}px Arial`;
        ctx.textAlign = 'center';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.strokeText(this.text, this.x, this.y);
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

class RingExplosion extends Particle {
    constructor(x, y, color, maxRadius) {
        super(x, y, color);
        this.radius = 0;
        this.maxRadius = maxRadius;
        this.life = 60;
        this.maxLife = 60;
    }
    
    update() {
        super.update();
        this.radius = (1 - this.life / this.maxLife) * this.maxRadius;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }
}

class BulletTrail extends Particle {
    constructor(startX, startY, endX, endY) {
        super(startX, startY, '#ffff00');
        this.endX = endX;
        this.endY = endY;
        this.life = 30;
        this.maxLife = 30;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.endX, this.endY);
        ctx.stroke();
        ctx.restore();
    }
}

class MuzzleFlash extends Particle {
    constructor(x, y) {
        super(x, y, '#ffff00');
        this.size = 15;
        this.life = 10;
        this.maxLife = 10;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        
        // Flash shape
        const spikes = 8;
        ctx.beginPath();
        for (let i = 0; i < spikes; i++) {
            const angle = (i * Math.PI * 2) / spikes;
            const radius = i % 2 === 0 ? this.size : this.size / 2;
            const x = this.x + Math.cos(angle) * radius;
            const y = this.y + Math.sin(angle) * radius;
            
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
}

class ConfettiPiece extends Particle {
    constructor(x, y, color) {
        super(x, y, color);
        this.vx = (Math.random() - 0.5) * 10;
        this.vy = -Math.random() * 15 - 5;
        this.width = Math.random() * 8 + 4;
        this.height = Math.random() * 8 + 4;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = (Math.random() - 0.5) * 0.3;
        this.life = 180;
        this.maxLife = 180;
    }
    
    update() {
        super.update();
        this.vy += 0.3; // Gravity
        this.rotation += this.rotationSpeed;
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.fillStyle = this.color;
        ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
        ctx.restore();
    }
}

class ScreenShakeEffect extends Particle {
    constructor(canvas) {
        super(0, 0);
        this.canvas = canvas;
        this.intensity = 10;
        this.life = 20;
        this.maxLife = 20;
        this.originalTransform = canvas.style.transform;
    }
    
    update() {
        super.update();
        const shake = this.intensity * (this.life / this.maxLife);
        const x = (Math.random() - 0.5) * shake;
        const y = (Math.random() - 0.5) * shake;
        this.canvas.style.transform = `translate(${x}px, ${y}px)`;
    }
    
    render(ctx) {
        // No visual rendering needed
    }
    
    isDead() {
        if (this.life <= 0) {
            this.canvas.style.transform = this.originalTransform;
            return true;
        }
        return false;
    }
}

// Emitter classes
class BurstEmitter {
    constructor(x, y, options = {}) {
        this.x = x;
        this.y = y;
        this.color = options.color || '#ffffff';
        this.particleCount = options.particleCount || 10;
        this.speed = options.speed || 5;
        this.life = options.life || 60;
        this.maxLife = this.life;
        this.particles = [];
        
        this.createParticles();
    }
    
    createParticles() {
        for (let i = 0; i < this.particleCount; i++) {
            const angle = (i / this.particleCount) * Math.PI * 2;
            const particle = new Particle(this.x, this.y, this.color);
            particle.vx = Math.cos(angle) * this.speed;
            particle.vy = Math.sin(angle) * this.speed;
            particle.life = this.life;
            particle.maxLife = this.life;
            this.particles.push(particle);
        }
    }
    
    update() {
        this.particles.forEach((particle, index) => {
            particle.update();
            if (particle.isDead()) {
                this.particles.splice(index, 1);
            }
        });
        this.life--;
    }
    
    render(ctx) {
        this.particles.forEach(particle => particle.render(ctx));
    }
    
    isDead() {
        return this.particles.length === 0;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ParticleSystem };
} else if (typeof window !== 'undefined') {
    window.ParticleSystem = ParticleSystem;
}
