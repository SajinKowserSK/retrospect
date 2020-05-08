const express = require('express');
const http = require('http');
const app = express();
const server = http.Server(app);
const io = require('socket.io')(server);
app.set('views','./views'); // set html folder to views.
app.set('view engine', 'ejs'); 
app.use(express.static(__dirname + '/static')); // set static folder to ./static.

server.listen(5000);
console.log('chat server listening on PORT 5000');
app.get('/', (req, res)=>{
     res.render('index.ejs');
})

io.on('connection', (socket)=> {
    console.log('new connection');
    socket.emit("message","welcome to chat!");
})