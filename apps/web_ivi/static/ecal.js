import * as vd from './vehicle-dynamics.js';
import * as ts from './turn-signals.js';
import * as wg from './warning-glowing.js';
import * as is from './info-screen.js';

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

const eventSourceCalculatedAngle = new EventSource("/calculated_angle");

eventSourceCalculatedAngle.onopen = function (_event) {
    console.log("Connection to /calculated_angle opened");
}

// ---------- add event listener for the event ----------
let lastEventTime = null; // To store the timestamp of the last event
let totalDistance = 0;
let isSafe = true;
eventSourceVehicleDynamics.addEventListener("vehicle-dynamics", function (event) {
    let raw_data = event.data;
    let vehicle_dynamics = JSON.parse(raw_data);
    console.log(vehicle_dynamics);

    let speed_km_h = parseInt(parseFloat(vehicle_dynamics.signals.speedDisplayed) * 3.6)
    console.log("Received speed_km_h: ", speed_km_h);

    const currentEventTime = Date.now(); // Current timestamp in milliseconds
    if (lastEventTime !== null) {
        const timeDifferenceHours = (currentEventTime - lastEventTime) / (1000 * 60 * 60); // Convert ms to hours

        const distanceTraveled = speed_km_h * timeDifferenceHours;
        totalDistance += distanceTraveled;

        console.log(`Time difference: ${timeDifferenceHours.toFixed(6)} hours`);
        console.log(`Distance traveled in this interval: ${distanceTraveled.toFixed(2)} km`);
        console.log(`Total distance traveled: ${totalDistance.toFixed(2)} km`);
    }

    lastEventTime = currentEventTime;

    vd.updateSpeedAndTorque(speed_km_h);
    if(isSafe) is.updateVehicleStatus(vd.isDriving(speed_km_h) ? "Driving" : "Parking");
    is.updateEstimatedRange(totalDistance);
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

eventSourceCalculatedAngle.addEventListener("calculated_angle", function (event) {
    let raw_data = event.data;
    console.log(raw_data);

    if (raw_data === "Safe") {
        wg.inactivateWarningGlowing();
    } else if (true) {
        let angle = parseInt(raw_data);
        wg.activateWarningGlowing(angle);
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