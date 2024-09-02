// Function to send a POST request to the Flask server
function sendRequest() {
    fetch('http://54.175.240.135:5000/trigger', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
        console.log('Request sent:', data);
        establishWebSocket();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to establish a WebSocket connection with the Flask server
function establishWebSocket() {
    const socket = new WebSocket('ws://54.175.240.135:5000/socket.io/?EIO=4&transport=websocket');

    socket.onopen = function(event) {
        console.log('WebSocket connection established');
    };

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'status') {
            document.getElementById('status').textContent = data.data;
        }
    };

    socket.onclose = function(event) {
        console.log('WebSocket connection closed');
        document.getElementById('status').textContent = 'Disconnected';
    };
}

// Event listener for the button click
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('triggerButton').addEventListener('click', sendRequest);
});