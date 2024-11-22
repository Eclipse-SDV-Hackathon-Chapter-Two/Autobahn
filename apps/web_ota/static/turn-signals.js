function toggleTurnSignal(direction) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    signal.classList.toggle('active', true);
}

function blinkTurnSignal(direction) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    let isOn = false;
    
    return setInterval(() => {
        isOn = !isOn;
        signal.style.opacity = isOn ? 1 : 0.3;
    }, 500);
}

export function activateTurnSignal(direction) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    signal.classList.toggle('active', true);
    return blinkTurnSignal(direction);
}

export function inactivateTurnSignal(direction, interval) {
    const signal = document.querySelector(`.turn-signal.${direction}`);
    signal.style.opacity = 0.3;
    signal.classList.toggle('active', false);
    clearInterval(interval);
}
