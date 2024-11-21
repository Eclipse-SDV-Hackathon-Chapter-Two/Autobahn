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

export function activateTurnSignal(direction) {
    toggleTurnSignal(direction);
    blinkTurnSignal(direction);
}

export function inactivateTurnSignal(direction) {
    signal.style.opacity = 0.3;
    toggleTurnSignal(direction);
}
