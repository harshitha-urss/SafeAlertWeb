document.getElementById("sendAlert").addEventListener("click", function() {
    fetch('/send_alert', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerText = data.message;
    });
});
