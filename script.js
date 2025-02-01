// Animate the counters
    
    document.addEventListener('DOMContentLoaded', () => {
    const circles = document.querySelectorAll('.circle');

    circles.forEach(circle => {
        const percent = parseInt(circle.getAttribute('data-percent'), 10);
        if (isNaN(percent) || percent < 0 || percent > 100) {
            console.error('Invalid data-percent value:', circle.getAttribute('data-percent'));
            return; // Skip invalid circle
        }

        let currentPercent = 0;

        function animateCircle() {
            if (currentPercent <= percent) {
                const degrees = (360 * currentPercent) / 100;
                circle.style.backgroundImage = `conic-gradient(#ad69ca ${degrees}deg, #e8f5e9 0deg)`;
                circle.querySelector('.percent').textContent = `${currentPercent}%`;
                currentPercent++;
                requestAnimationFrame(animateCircle); // Smooth animation
            }
        }

        animateCircle();
    });
});

