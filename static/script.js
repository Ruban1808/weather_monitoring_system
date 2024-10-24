document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('#alerts li');
    if (alerts.length > 0) {
        // Automatically remove alerts after 5 seconds
        setTimeout(() => {
            alerts.forEach(alert => alert.remove());
        }, 5000);
    }
});
