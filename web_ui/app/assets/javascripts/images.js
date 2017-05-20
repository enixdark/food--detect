//= require socket.io

// var socket = io.connect('{{SOCKET_SERVER_URI}}:1333');
var socket = io.connect('0.0.0.0:1333');
socket.on('answer', function(message){
  console.log(message);
});
