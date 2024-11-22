export function updateVehicleStatus(status) {
    const statusElement = document.getElementById("vehicle-status");
    statusElement.textContent = status;
}

export function updateBatteryLevel(level) {
    const batteryElement = document.getElementById("battery-level");
    batteryElement.textContent = `${level}%`;
}

export function updateEstimatedRange(range) {
    const rangeElement = document.getElementById("estimated-range");
    const numericRange = Number(range);
    rangeElement.textContent = `${numericRange.toFixed(2)} km`;
}

export function updateOutsideTemp(temp) {
    const tempElement = document.getElementById("outside-temp");
    const numericTemp = Number(temp);
    tempElement.textContent = `${numericTemp.toFixed(1)}°C`;
}

function updateCurrentTime(time) {
    const timeElement = document.getElementById("current-time");
    timeElement.textContent = time;
}

export function updateCurrentLocaleTime() {
    setInterval(() => {
        const now = new Date();
        updateCurrentTime(now.toLocaleTimeString());
    }, 1000);
}