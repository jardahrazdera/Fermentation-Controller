function updateTime() {
    const timeElement = document.getElementById('current-time');
    const now = new Date();
    timeElement.textContent = now.toLocaleString();
}

setInterval(updateTime, 1000); // Updates every second