document.addEventListener('DOMContentLoaded', () => {
    // Add functionality to the Yes and No buttons
    const yesButton = document.querySelector('.update-button.yes');
    const noButton = document.querySelector('.update-button.no');

    yesButton.addEventListener('click', () => {
        // Add actual update logic here
        fetch('/yorn', {
            method: 'POST'
        })
    });

    noButton.addEventListener('click', () => {
        firmwareUpdate.classList.remove('visible');
    });
});