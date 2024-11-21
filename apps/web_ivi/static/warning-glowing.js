// document.addEventListener('DOMContentLoaded', () => {
//     const warningBackground = document.getElementById('warning-background');
//     let isWarningActive = true;

//     document.addEventListener('keydown', (event) => {
//         event.preventDefault(); // Prevent scrolling when space is pressed
        
//         let angle = 0;
//         if (event.code === 'Digit1') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = -45;
//         }

//         if (event.code === 'Digit2') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = -35;
//         }

//         if (event.code === 'Digit3') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = -25;
//         }

//         if (event.code === 'Digit4') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = -15;
//         }

//         if (event.code === 'Digit5') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = -5;
//         }

//         if (event.code === 'Digit6') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = 5;
//         }

//         if (event.code === 'Digit7') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = 15;
//         }

//         if (event.code === 'Digit8') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = 25;
//         }

//         if (event.code === 'Digit9') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = 35;
//         }

//         if (event.code === 'Digit0') {
//             // 원하는 각도를 변수로 설정 (예시: 60도)
//             angle = 45;
//         }

//         // linear-gradient의 각도를 동적으로 업데이트
//         warningBackground.style.background = `linear-gradient(${angle}deg, rgba(255,0,0,0) 80%, rgba(255,0,0,0.8) 100%)`;

//         // isWarningActive = !isWarningActive;
//         warningBackground.classList.toggle('active', isWarningActive);
//     });
// });

export function activateWarningGlowing(angle) {
    let warningBackground = document.getElementById('warning-background');
    warningBackground.style.background = `linear-gradient(${angle}deg, rgba(255,0,0,0) 80%, rgba(255,0,0,0.8) 100%)`;
    warningBackground.classList.toggle('active', true);
}

export function inactivateWarningGlowing() {
    let warningBackground = document.getElementById('warning-background');
    warningBackground.classList.toggle('active', false);
}