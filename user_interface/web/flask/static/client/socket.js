const socket = io();

socket.on('server_message', function (json) {
    console.log("server_message")
    show_server_message(json.data)
})

socket.on('service_message', function (json) {
    console.log("service_message", json.data)
    handler_service_message(json.data)
    console.log("settings", settings)
})
socket.on('level', function (json) {
    show_level(json.data)
})

socket.on('chart', function (json) {
    get_chart(json)
})

function send_user_answer(message) {
    console.log("socket user_answer")
    socket.emit('user_answer', {data: message});
}

function start_game(body) {
    socket.emit('start_game', {data: body})
}

function socket_stop_game() {
    socket.emit('stop_game')
}