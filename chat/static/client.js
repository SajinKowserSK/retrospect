const socket = io.connect('http://localhost:5000');
const messageForm = document.getElementById('send-container');
const messageInput = document.getElementById('message-input');
const messageContainer = document.getElementById('message-container');

function appendMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    messageContainer.append(messageElement);

}
socket.on("message",(message) => {
    appendMessage(message);
})
messageForm.addEventListener("submit", function(e) {
    e.preventDefault();
    var message = messageInput.value;
    appendMessage(message);
    socket.emit('client-message', message);

})
