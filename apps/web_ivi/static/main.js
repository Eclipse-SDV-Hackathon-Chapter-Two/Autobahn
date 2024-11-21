import * as is from './info-screen.js';

// ---------- Variables ----------
// info-screen
const APIKEY = "YOUR_API_KEY";
const lat = 49.00180539504802;
const lon = 8.365262392978693;

let range = 0;

fetch("https://api.openweathermap.org/data/2.5/weatherlat=${lat}&lon=${lon}&appid{APIKEY}&units=metric")

// ---------- Implements ----------
// ----- info-screen -----
// Temperture
fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${APIKEY}&units=metric`)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        // Extract the temperature data
        const temperature = data.main.temp;
        console.log(`Current temperature: ${temperature}°C`);

        // Update HTML content (e.g., #outside-temp element)
        is.updateOutsideTemp(temperature);
    })
    .catch(error => {
        console.error("Error occurred while fetching data from the API:", error);
    });
// Time
is.updateCurrentLocaleTime();

document.addEventListener("keydown", function(event) {
    if (event.key === "Y" || event.key === "y") {
        fetch('/execute-shell-script', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Shell script executed:', data);
        })
        .catch(error => console.error('Error:', error));
    }
});