function toggleTurnSignal(direction) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    signal.classList.toggle('active');
}

function blinkTurnSignal(direction) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    let isOn = false;
    
    return setInterval(() => {
        isOn = !isOn;
        signal.style.opacity = isOn ? 1 : 0.3;
    }, 500);
}

let leftInterval, rightInterval;

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        if (leftInterval) {
            clearInterval(leftInterval);
            leftInterval = null;
            toggleTurnSignal('left');
        } else {
            leftInterval = blinkTurnSignal('left');
        }
    } else if (event.key === 'ArrowRight') {
        if (rightInterval) {
            clearInterval(rightInterval);
            rightInterval = null;
            toggleTurnSignal('right');
        } else {
            rightInterval = blinkTurnSignal('right');
        }
    }
});