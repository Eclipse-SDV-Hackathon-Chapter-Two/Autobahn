import * as vd from './vehicle-dynamics.js';
import * as ts from './turn-signals.js';
import * as wg from './warning-glowing.js';

// ---------- read from server-side event ----------
// vehicle-dynamics
const eventSourceVehicleDynamics = new EventSource("/vehicle-dynamics");

eventSourceVehicleDynamics.onopen = function (_event) {
    console.log("Connection to /vehicle-dynamics opened");
}

const eventSourceHiddenDangerPeople = new EventSource("/hidden_danger_people");

eventSourceHiddenDangerPeople.onopen = function (_event) {
    console.log("Connection to /hidden_danger_people opened");
}

// ---------- add event listener for the event ----------
eventSourceVehicleDynamics.addEventListener("vehicle-dynamics", function (event) {
    let raw_data = event.data;
    let vehicle_dynamics = JSON.parse(raw_data);
    console.log(vehicle_dynamics);
    let speed_km_h = parseInt(parseFloat(vehicle_dynamics.signals.speedDisplayed) * 3.6)
    console.log("Received speed_km_h: ", speed_km_h);
    vd.updateSpeedAndTorque(speed_km_h);
});

let isTurnOn = false;
let leftInterval, rightInterval;
let isTimer = false;
eventSourceHiddenDangerPeople.addEventListener("hidden_danger_people", function (event) {
    let raw_data = event.data;
    console.log("Hidden Danger People: ", raw_data);
    if (raw_data === "HiddenDangerPeople" && !isTurnOn) {
        leftInterval = ts.activateTurnSignal('left');
        rightInterval = ts.activateTurnSignal('right');
        isTurnOn = true;
        console.log("Activate Turn Signals");
    } else if (raw_data === "Safe" && isTurnOn && !isTimer) {
        isTimer = true;
        setTimeout(() => {
            ts.inactivateTurnSignal('left', leftInterval);
            ts.inactivateTurnSignal('right', rightInterval);
            isTurnOn = false;
            isTimer = false;
            console.log("Inactivate Turn Signals after 3 seconds");
        }, 3000);
    }
});

// ---------- close the connection on error ----------
eventSourceVehicleDynamics.onerror = function (event) {
    console.log("Error: " + event);
    eventSourceVehicleDynamics.close();
}

eventSourceHiddenDangerPeople.onerror = function (event) {
    console.log("Error: " + event);
    eventSourceHiddenDangerPeople.close();
}