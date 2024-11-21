const speedTorqueRelation = [{
    speed: 0,
    torque: "D1"
}, {
    speed: 20,
    torque: "D2"
}, {
    speed: 30,
    torque: "D3"
}, {
    speed: 40,
    torque: "D4"
}, {
    speed: 70,
    torque: "D5"
}, {
    speed: 80,
    torque: "D6"
}, {
    speed: 100,
    torque: "D7"
}];

/* update the speed-value */
export function updateSpeedAndTorque(speed_km_h) {
    // update the speed value fluently by a number
    let speedValue = document.getElementById("speed-value");
    let torqueValue = document.getElementById("torque-value");

    // check if the speed_km_h is greater or equal the last speed in the speedTorqueRelation
    if (speedTorqueRelation.length > 0 && speed_km_h >= speedTorqueRelation[speedTorqueRelation.length - 1].speed) {
        torqueValue.textContent = speedTorqueRelation[speedTorqueRelation.length - 1].torque;
    } else if (speed_km_h < 0) {
        torqueValue.textContent = "R"; // speed negative driving backwards
    } else {
        let torque_out = speedTorqueRelation.find((element) => {
            return speed_km_h <= element.speed;
        });

        if (torque_out) {
            torqueValue.textContent = torque_out.torque;
        }
    }

    speedValue.textContent = speed_km_h;
}
