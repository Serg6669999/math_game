function httpGet(path, body)
{

    let url = "http://localhost:5000/"

    const options = {
        headers: {"Content-Type":"application/json"},
        method: "POST",
        body: JSON.stringify( body )
        };
    fetch( url + path, options )
        .then( response => response.json() )
        .then( response => {
            // Do something with response.
        } );
}

function get_data_for_start_game(document) {

    let delayed_response = document.getElementById("delayed_response").value;
    let max_steps_of_level = document.getElementById("max_steps_of_level").value;
    let entry_level = document.getElementById("entry_level").value;
    return {
        "game_name": document.games.game.value,
        "delayed_response": delayed_response,
        "max_steps_of_level": max_steps_of_level,
        "entry_level": entry_level
    }

}

function stop_game(document) {
    document.getElementById('message_for_user').innerHTML = "finish"
    socket_stop_game()
}

function show_server_message(server_message) {
    document.getElementById('message_for_user').innerHTML = server_message

}

function sent_user_answer(document) {

    let message = document.getElementById("user_answer_").value;
    console.log("message", message)
    return send_user_answer(message)
}

document.getElementById("start").addEventListener("click", function (){
    let body = get_data_for_start_game(document)
        start_game(body)
    }
        );
document.getElementById("stop").addEventListener("click", function (){
        stop_game(document)
    }
        );

document.addEventListener("keypress", function(event) {
  if (event.keyCode === 13) {
    sent_user_answer(document);
    let input_ = document.getElementById("user_answer_")
      input_.value = ""
  }
});