//= require socket.io

// var socket = io.connect('{{SOCKET_SERVER_URI}}:1333');
var socket = io.connect('0.0.0.0:1333');

//get answer about food from image upload
socket.on('answer', function(message){
  $.ajax({
    method: "POST",
    url: "/images/return_data",
    data: { video_data_params: message }
  })
});


// get answer about nutrition of food
socket.on('nutrition', function(message){
  console.log(message)
});