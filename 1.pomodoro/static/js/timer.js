document.addEventListener('DOMContentLoaded', () => {
    const timeDisplay = document.getElementById('time-display');
    const phaseDisplay = document.getElementById('phase-display');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const circle = document.querySelector('.progress-ring__circle');
    const bgEffects = document.getElementById('background-effects');

    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;

    const WORK_TIME = 25 * 60; // 25 minutes in seconds
    const RESET_DELAY = 3000;
    const PARTICLE_MIN_SIZE = 5;
    const PARTICLE_SIZE_RANGE = 10;
    const PARTICLE_MIN_DURATION = 2;
    const PARTICLE_DURATION_RANGE = 3;
    const PARTICLE_LIFETIME = 5000; // Matches max duration (2+3)s
    const RIPPLE_LIFETIME = 2000; // Matches CSS animation duration
    const PARTICLE_INTERVAL = 300;
    const RIPPLE_INTERVAL = 2000;

    let timeRemaining = WORK_TIME;
    let timerInterval = null;
    let isRunning = false;
    let totalDuration = WORK_TIME;

    function setProgress(percent) {
        const offset = circumference - percent / 100 * circumference;
        circle.style.strokeDashoffset = offset;
    }

    function updateColor(percent) {
        // Color transition:
        // 100% to 50%: Blue (79, 172, 254) to Yellow (255, 255, 0)
        // 50% to 0%: Yellow (255, 255, 0) to Red (255, 0, 0)
        let r, g, b;
        if (percent > 50) {
            // Blue to Yellow
            const p = (percent - 50) / 50;
            r = Math.floor(79 + (176 * (1 - p))); // 79 to 255
            g = Math.floor(172 + (83 * (1 - p))); // 172 to 255
            b = Math.floor(254 * p);              // 254 to 0
        } else {
            // Yellow to Red
            const p = percent / 50;
            r = 255;
            g = Math.floor(255 * p); // 0 to 255
            b = 0;
        }
        circle.style.stroke = `rgb(${r}, ${g}, ${b})`;
    }

    function updateDisplay() {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const percent = (timeRemaining / totalDuration) * 100;
        setProgress(percent);
        updateColor(percent);
    }

    function createParticle() {
        if (!isRunning) return;
        
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        const size = Math.random() * PARTICLE_SIZE_RANGE + PARTICLE_MIN_SIZE;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `100%`;
        
        particle.style.animationDuration = `${Math.random() * PARTICLE_DURATION_RANGE + PARTICLE_MIN_DURATION}s`;
        
        bgEffects.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, PARTICLE_LIFETIME);
    }

    function createRipple() {
        if (!isRunning) return;
        
        const ripple = document.createElement('div');
        ripple.classList.add('ripple');
        bgEffects.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, RIPPLE_LIFETIME);
    }

    let effectInterval = null;
    let rippleInterval = null;

    function startEffects() {
        stopEffects(); // Ensure no overlapping intervals
        effectInterval = setInterval(createParticle, PARTICLE_INTERVAL);
        rippleInterval = setInterval(createRipple, RIPPLE_INTERVAL);
    }

    function stopEffects() {
        clearInterval(effectInterval);
        clearInterval(rippleInterval);
    }

    function startTimer() {
        if (isRunning) return;
        isRunning = true;
        
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        
        startEffects();
        
        timerInterval = setInterval(() => {
            timeRemaining--;
            updateDisplay();
            
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                isRunning = false;
                stopEffects();
                startBtn.disabled = false;
                pauseBtn.disabled = true;
                phaseDisplay.textContent = '完了！';
                // Reset to default after a bit
                setTimeout(() => resetTimer(), RESET_DELAY);
            }
        }, 1000);
    }

    function pauseTimer() {
        if (!isRunning) return;
        isRunning = false;
        
        clearInterval(timerInterval);
        stopEffects();
        
        startBtn.disabled = false;
        pauseBtn.disabled = true;
    }

    function resetTimer() {
        pauseTimer();
        timeRemaining = WORK_TIME;
        phaseDisplay.textContent = '作業中';
        updateDisplay();
    }

    startBtn.addEventListener('click', startTimer);
    pauseBtn.addEventListener('click', pauseTimer);
    resetBtn.addEventListener('click', resetTimer);

    // Initial setup
    setProgress(100);
    updateColor(100);
});
