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
        "game_name": document.games.game_name.value,
        "math_action": document.games.math_action.value,
        "delayed_response": delayed_response,
        "max_steps_of_level": max_steps_of_level,
        "entry_level": entry_level,
        "words": document.games.words.value
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

function set_focus_to_user_answer(){
    const textInput = document.getElementById('user_answer_');
            textInput.focus();
}


class Settings {
    constructor() {
        this._deviceType = "";
    }
    get deviceType() {
        return this._deviceType;
    }
    set deviceType(value) {
        this._deviceType = value;
    }}
let settings = new Settings()
function handler_service_message(message){
    settings.deviceType = message.device
}
class ClickElement {
  constructor(settings) {
        console.log("ClickElementSettings", settings)
      this.action = {"user_answer_focus": {"ps": set_focus_to_user_answer,
                                           "mobile": function (){},
                                            "tablet": function (){}
                     }}
  }
  get() {

        document.getElementById("start").addEventListener("click", function (){
            let body = get_data_for_start_game(document)
                start_game(body)
                console.log("click settings", settings.deviceType, this.device_type)
            this.action.user_answer_focus[settings.deviceType]()
            }.bind(this)
                );

        document.getElementById("ok").addEventListener("click", function (){
            this.action.user_answer_focus[settings.deviceType]()
            sent_user_answer(document);
            let input_ = document.getElementById("user_answer_")
              input_.value = ""
            }.bind(this)
                );
        document.getElementById("yes").addEventListener("click", function (){
                send_user_answer("yes");
                this.action.user_answer_focus[settings.deviceType]()
            let input_ = document.getElementById("user_answer_")
              input_.value = ""
            }.bind(this)
                );
        document.getElementById("del").addEventListener("click", function (){
            this.action.user_answer_focus[settings.deviceType]()
            let input_ = document.getElementById("user_answer_")
              input_.value = input_.value.substring(0, input_.value.length - 1)
            }.bind(this)
                );
}}
new ClickElement(settings).get()

document.getElementById("stop").addEventListener("click", function (){
        stop_game(document)
    }
        );
document.addEventListener("keypress", function(event) {
  if (event.keyCode === 13)  {
    sent_user_answer(document);
    let input_ = document.getElementById("user_answer_")
      input_.value = ""
  }
});

// press numbers
const keys = document.querySelectorAll('.key');

keys.forEach(key => {
    key.addEventListener('click', () => {
        const input = document.getElementById("user_answer_");
        const current_value = input.value;
        memory_game = get_data_for_start_game(document)
        let addition = ""
        if (memory_game.game_name === "Memory") {addition = "_"}
        input.value = current_value + key.textContent[0] + addition
    });
});
