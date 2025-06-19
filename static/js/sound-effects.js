/**
 * Advanced Sound Effects Library for AWS Trivia Game
 * Web Audio API based sound generation for immersive gaming experience
 */

class SoundEngine {
    constructor() {
        this.audioContext = null;
        this.masterGain = null;
        this.enabled = true;
        this.volume = 0.3;
        
        this.initializeAudio();
    }
    
    initializeAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.masterGain = this.audioContext.createGain();
            this.masterGain.connect(this.audioContext.destination);
            this.masterGain.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
        } catch (error) {
            console.warn('Web Audio API not supported:', error);
            this.enabled = false;
        }
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        if (this.masterGain) {
            this.masterGain.gain.setValueAtTime(this.volume, this.audioContext.currentTime);
        }
    }
    
    setEnabled(enabled) {
        this.enabled = enabled;
    }
    
    // Core sound generation methods
    playTone(frequency, duration, type = 'sine', volume = 1) {
        if (!this.enabled || !this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = type;
        oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(volume * 0.1, this.audioContext.currentTime + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    playChord(frequencies, duration, type = 'sine', volume = 1) {
        frequencies.forEach(freq => {
            this.playTone(freq, duration, type, volume / frequencies.length);
        });
    }
    
    playNoise(duration, volume = 1, filterFreq = 1000) {
        if (!this.enabled || !this.audioContext) return;
        
        const bufferSize = this.audioContext.sampleRate * duration;
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const data = buffer.getChannelData(0);
        
        // Generate white noise
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * volume;
        }
        
        const source = this.audioContext.createBufferSource();
        const gainNode = this.audioContext.createGain();
        const filter = this.audioContext.createBiquadFilter();
        
        source.buffer = buffer;
        source.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(filterFreq, this.audioContext.currentTime);
        
        gainNode.gain.setValueAtTime(volume * 0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);
        
        source.start(this.audioContext.currentTime);
    }
    
    // Game-specific sound effects
    playCorrectAnswer() {
        // Success chord progression
        const chord1 = [523.25, 659.25, 783.99]; // C5, E5, G5
        const chord2 = [659.25, 783.99, 987.77]; // E5, G5, B5
        
        this.playChord(chord1, 0.3, 'sine', 0.8);
        setTimeout(() => {
            this.playChord(chord2, 0.4, 'sine', 0.6);
        }, 200);
        
        // Sparkle effect
        setTimeout(() => {
            for (let i = 0; i < 5; i++) {
                setTimeout(() => {
                    this.playTone(1000 + i * 200, 0.1, 'sine', 0.3);
                }, i * 50);
            }
        }, 400);
    }
    
    playWrongAnswer() {
        // Dissonant chord
        const dissonantChord = [220, 233.08, 246.94]; // A3, A#3, B3
        this.playChord(dissonantChord, 0.8, 'sawtooth', 0.6);
        
        // Descending tone
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'square';
        oscillator.frequency.setValueAtTime(300, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(100, this.audioContext.currentTime + 0.5);
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.5);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.5);
    }
    
    playShoot() {
        // Laser sound effect
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.masterGain);
        
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(200, this.audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.1);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.1);
    }
    
    playExplosion() {
        // Explosion sound with noise and low frequency
        this.playNoise(0.3, 0.8, 200);
        
        // Low frequency rumble
        this.playTone(60, 0.5, 'sine', 0.6);
        
        // High frequency crack
        setTimeout(() => {
            this.playTone(2000, 0.1, 'square', 0.4);
        }, 50);
    }
    
    playPowerUp() {
        // Ascending arpeggio
        const notes = [261.63, 329.63, 392.00, 523.25, 659.25]; // C4, E4, G4, C5, E5
        
        notes.forEach((freq, index) => {
            setTimeout(() => {
                this.playTone(freq, 0.2, 'sine', 0.5);
            }, index * 100);
        });
        
        // Sparkle overlay
        setTimeout(() => {
            for (let i = 0; i < 8; i++) {
                setTimeout(() => {
                    this.playTone(1500 + Math.random() * 1000, 0.1, 'sine', 0.2);
                }, i * 30);
            }
        }, 300);
    }
    
    playLevelUp() {
        // Triumphant fanfare
        const melody = [
            { freq: 523.25, duration: 0.2 }, // C5
            { freq: 659.25, duration: 0.2 }, // E5
            { freq: 783.99, duration: 0.2 }, // G5
            { freq: 1046.50, duration: 0.4 } // C6
        ];
        
        melody.forEach((note, index) => {
            setTimeout(() => {
                this.playTone(note.freq, note.duration, 'sine', 0.7);
            }, index * 200);
        });
        
        // Harmony
        setTimeout(() => {
            this.playChord([523.25, 659.25, 783.99], 0.8, 'sine', 0.4);
        }, 600);
    }
    
    playGameOver() {
        // Sad descending melody
        const melody = [
            { freq: 523.25, duration: 0.3 }, // C5
            { freq: 493.88, duration: 0.3 }, // B4
            { freq: 440.00, duration: 0.3 }, // A4
            { freq: 392.00, duration: 0.3 }, // G4
            { freq: 349.23, duration: 0.6 }  // F4
        ];
        
        melody.forEach((note, index) => {
            setTimeout(() => {
                this.playTone(note.freq, note.duration, 'sine', 0.6);
            }, index * 300);
        });
        
        // Minor chord at the end
        setTimeout(() => {
            this.playChord([349.23, 415.30, 523.25], 1.0, 'sine', 0.4); // F4, G#4, C5
        }, 1500);
    }
    
    playMenuMusic() {
        if (!this.enabled || !this.audioContext) return;
        
        // Simple ambient loop
        const playAmbientTone = () => {
            const frequencies = [220, 330, 440, 550];
            const freq = frequencies[Math.floor(Math.random() * frequencies.length)];
            this.playTone(freq, 2.0, 'sine', 0.1);
            
            setTimeout(playAmbientTone, 3000 + Math.random() * 2000);
        };
        
        playAmbientTone();
    }
    
    playCountdown() {
        // Tick sound
        this.playTone(800, 0.1, 'square', 0.5);
    }
    
    playFinalCountdown() {
        // Urgent tick
        this.playTone(1200, 0.1, 'square', 0.8);
    }
    
    playAchievement() {
        // Achievement jingle
        const jingle = [
            { freq: 659.25, duration: 0.15 }, // E5
            { freq: 783.99, duration: 0.15 }, // G5
            { freq: 1046.50, duration: 0.15 }, // C6
            { freq: 1318.51, duration: 0.3 }   // E6
        ];
        
        jingle.forEach((note, index) => {
            setTimeout(() => {
                this.playTone(note.freq, note.duration, 'sine', 0.6);
            }, index * 150);
        });
    }
    
    playButtonClick() {
        this.playTone(600, 0.05, 'square', 0.3);
    }
    
    playButtonHover() {
        this.playTone(400, 0.03, 'sine', 0.2);
    }
    
    // Background music methods
    startBackgroundMusic() {
        if (!this.enabled || !this.audioContext) return;
        
        this.backgroundMusicPlaying = true;
        this.playBackgroundLoop();
    }
    
    stopBackgroundMusic() {
        this.backgroundMusicPlaying = false;
    }
    
    playBackgroundLoop() {
        if (!this.backgroundMusicPlaying) return;
        
        // Simple chord progression
        const chords = [
            [261.63, 329.63, 392.00], // C major
            [293.66, 369.99, 440.00], // D minor
            [329.63, 415.30, 493.88], // E minor
            [349.23, 440.00, 523.25]  // F major
        ];
        
        chords.forEach((chord, index) => {
            setTimeout(() => {
                if (this.backgroundMusicPlaying) {
                    this.playChord(chord, 1.5, 'sine', 0.05);
                }
            }, index * 2000);
        });
        
        // Loop
        setTimeout(() => {
            if (this.backgroundMusicPlaying) {
                this.playBackgroundLoop();
            }
        }, 8000);
    }
    
    // Utility methods
    createReverb(duration = 2, decay = 2) {
        if (!this.audioContext) return null;
        
        const convolver = this.audioContext.createConvolver();
        const bufferSize = this.audioContext.sampleRate * duration;
        const buffer = this.audioContext.createBuffer(2, bufferSize, this.audioContext.sampleRate);
        
        for (let channel = 0; channel < 2; channel++) {
            const channelData = buffer.getChannelData(channel);
            for (let i = 0; i < bufferSize; i++) {
                channelData[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, decay);
            }
        }
        
        convolver.buffer = buffer;
        return convolver;
    }
    
    // Resume audio context (required for some browsers)
    resumeAudio() {
        if (this.audioContext && this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
    }
}

// Global sound engine instance
let soundEngine = null;

// Initialize sound engine
function initializeSoundEngine() {
    if (!soundEngine) {
        soundEngine = new SoundEngine();
    }
    return soundEngine;
}

// Convenience functions
function playSound(type, ...args) {
    if (!soundEngine) {
        soundEngine = initializeSoundEngine();
    }
    
    soundEngine.resumeAudio();
    
    switch (type) {
        case 'correct':
            soundEngine.playCorrectAnswer();
            break;
        case 'wrong':
            soundEngine.playWrongAnswer();
            break;
        case 'shoot':
            soundEngine.playShoot();
            break;
        case 'explosion':
            soundEngine.playExplosion();
            break;
        case 'powerup':
            soundEngine.playPowerUp();
            break;
        case 'levelup':
            soundEngine.playLevelUp();
            break;
        case 'gameover':
            soundEngine.playGameOver();
            break;
        case 'achievement':
            soundEngine.playAchievement();
            break;
        case 'click':
            soundEngine.playButtonClick();
            break;
        case 'hover':
            soundEngine.playButtonHover();
            break;
        case 'countdown':
            soundEngine.playCountdown();
            break;
        case 'finalcountdown':
            soundEngine.playFinalCountdown();
            break;
        default:
            console.warn('Unknown sound type:', type);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SoundEngine, initializeSoundEngine, playSound };
} else if (typeof window !== 'undefined') {
    window.SoundEngine = SoundEngine;
    window.initializeSoundEngine = initializeSoundEngine;
    window.playSound = playSound;
}
