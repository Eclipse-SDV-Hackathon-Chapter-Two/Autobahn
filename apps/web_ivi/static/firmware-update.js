document.addEventListener('DOMContentLoaded', () => {
    const firmwareUpdate = document.getElementById('firmware-update');

    document.addEventListener('keydown', (event) => {
        if (event.key.toLowerCase() === 'f') {
            firmwareUpdate.classList.toggle('visible');
            console.log("visible!!!");
        }
    });

    // Add functionality to the Yes and No buttons
    const yesButton = document.querySelector('.update-button.yes');
    const noButton = document.querySelector('.update-button.no');

    yesButton.addEventListener('click', () => {
        // Add actual update logic here
    });

    noButton.addEventListener('click', () => {
        firmwareUpdate.classList.remove('visible');
    });
});