document.addEventListener('DOMContentLoaded', () => {
    const warningBackground = document.getElementById('warning-background');
    let isWarningActive = false;

    document.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            event.preventDefault(); // Prevent scrolling when space is pressed

            // 원하는 각도를 변수로 설정 (예시: 60도)
            let angle = 45;

            // warning-background 요소 선택
            let warningBackground = document.getElementById('warning-background');

            // linear-gradient의 각도를 동적으로 업데이트
            warningBackground.style.background = `linear-gradient(${angle}deg, rgba(255,0,0,0) 80%, rgba(255,0,0,0.8) 100%)`;

            isWarningActive = !isWarningActive;
            warningBackground.classList.toggle('active', isWarningActive);
        }
    });
});