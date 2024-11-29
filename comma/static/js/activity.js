function updateActivityCount() {
    fetch(activityCountUrl)
        .then(response => response.json())
        .then(data => {
            const countElement = document.getElementById('activityCount');
            if (data.count > 0) {
                countElement.textContent = data.count;
                countElement.style.display = 'flex';
            } else {
                countElement.style.display = 'none';
            }
        });
}

document.addEventListener('DOMContentLoaded', function() {
    setInterval(updateActivityCount, 15000);
    updateActivityCount();
});