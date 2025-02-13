// Form submission handling
document.querySelector('form').addEventListener('submit', function(e) {
    const username = document.querySelector('input[name="username"]').value.trim();
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingStatus = document.getElementById('loading-status');
    const errorMessage = document.getElementById('error-message');
    
    if (username) {
        loadingOverlay.style.display = 'flex';
        errorMessage.style.display = 'none';
        
        // Loading states animation
        const loadingStates = [
            'Connecting to LeetCode...',
            'Fetching profile data...',
            'Running AI analysis...',
            'Generating insights...',
            'Preparing your personalized report...'
        ];

        let currentState = 0;
        const updateStatus = () => {
            if (currentState < loadingStates.length) {
                loadingStatus.textContent = loadingStates[currentState];
                currentState++;
            }
        };

        updateStatus();
        const interval = setInterval(updateStatus, 1500);

        // Clear interval after form submission
        setTimeout(() => clearInterval(interval), 8000);
    }
});

// Particle animation
class ParticleAnimation {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.classList.add('particles-background');
        document.querySelector('.hero').appendChild(this.canvas);
        
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        
        this.resizeCanvas();
        this.initParticles();
        this.animate();
        
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.initParticles();
        });
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: Math.random() * 2 + 1,
            speedX: Math.random() * 2 - 1,
            speedY: Math.random() * 2 - 1,
            opacity: Math.random() * 0.5 + 0.2
        };
    }
    
    initParticles() {
        this.particles = [];
        const particleCount = Math.min(
            Math.floor((this.canvas.width * this.canvas.height) / 10000),
            100
        );
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push(this.createParticle());
        }
    }
    
    animate = () => {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;
            
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
            this.ctx.fill();
        });
        
        requestAnimationFrame(this.animate);
    }
}

// Initialize particle animation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ParticleAnimation();
    
    // Display error message if provided by Flask
    const errorMessage = document.getElementById('error-message');
    if (errorMessage && errorMessage.dataset.error) {
        errorMessage.textContent = errorMessage.dataset.error;
        errorMessage.style.display = 'block';
    }
});