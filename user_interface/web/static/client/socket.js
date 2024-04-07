const socket = io();

socket.on('connect', function() {
    socket.emit('connect_server', {data: 'I\'m connected!'});
});

socket.on('server_message', function (json) {
    console.log("server_message")
    show_server_message(json.data)

})

function send_user_answer(message) {
    console.log("socket user_answer")
    socket.emit('user_answer', {data: message});
}

function start_game(body) {
    socket.emit('start_game', {data: body})
}

function socket_stop_game(body) {
    socket.emit('stop_game', {data: body})
}