import sys
from typing import Dict

from settings import DIR_ROOT, log

sys.path.append(DIR_ROOT)

from flask_socketio import Namespace
from flask import render_template, request
from user_agents import parse

from user_interface.web.interface import WebInterface
from user_interface.web.storage import UserAnswer
from math_game.user_interface.web.socket_server import app, socketio
from math_game.run import GameConstructor, GameSettings


@app.route('/')
def get_arithmetic_game_(message: str = "Разгони мозг"):
    return render_template('web.html', data=message,
                           sync_mode=socketio.async_mode)


class ClientEvents(Namespace):
    socket_id_user_answers: Dict[str, UserAnswer] = {}

    def on_connect(self):
        user_agent = parse(request.user_agent.string)
        is_mobile = user_agent.is_mobile
        is_tablet = user_agent.is_tablet
        is_ps = user_agent.is_pc
        log(f"connect {request.headers}")

    def on_disconnect(self):
        self.on_stop_game()

    def on_start_game(self, data):
        print("start_game", request.sid)
        server_event = ServerEvents(request.sid)

        answer = UserAnswer(message=None, is_game_active=True)
        self.socket_id_user_answers[request.sid] = answer

        game = GameConstructor(GameSettings(**data['data']),
                               WebInterface(server_event, answer))
        game.run()

    def on_stop_game(self):
        self.socket_id_user_answers[request.sid].is_game_active = False
        print("stop game")

    def on_user_answer(self, data):
        self.socket_id_user_answers[request.sid].message = data['data']
        print('on_user_answer', self.socket_id_user_answers[request.sid], request.sid)


class ServerEvents:
    def __init__(self, socket_id):
        self.socket_id = socket_id

    def send_message(self, message: str, show_message_time: float = None):
        print('server_message', message, self.socket_id)
        socketio.emit("server_message", {"data": message}, room=self.socket_id)
        if show_message_time is not None:
            socketio.sleep(show_message_time)
            socketio.emit("server_message", {"data": '-'}, room=self.socket_id)


socketio.on_namespace(ClientEvents())

if __name__ == '__main__':
    print("start")
    socketio.run(app, host='0.0.0.0', port=5000)
