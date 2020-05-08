const socket = io.connect('http://localhost:5000');
const messageForm = document.getElementById('send-container');
messageForm.addEventListener("submit", function(e) {
    console.log("button pressed");
    e.preventDefault();
})
