import logging
import sys
from typing import Dict
sys.path.append(
    '/media/serg/ostree/serg/Документы/расчет рациона питания/mathGame')

from flask_socketio import Namespace
from flask import render_template, request

from user_interface.web.interface import WebInterface
from user_interface.web.storage import UserAnswer
from math_game.user_interface.web.socket_server import app, socketio
from math_game.run import GameConstructor, GameSettings

logging.basicConfig(level="INFO", format="%(processName)s %(threadName)s %(message)s")
log = logging.info

@app.route('/')
def get_arithmetic_game_(message: str = "Разгони мозг"):
    return render_template('web.html', data=message,
                           sync_mode=socketio.async_mode)



class ClientEvents(Namespace):
    user_answers: Dict[str, UserAnswer] = {}

    def on_connect(self):
        log(f"connect {request.sid}")

    def on_disconnect(self):
        pass

    def on_start_game(self, data):
        print("start_game", request.cookies['cookie'], request.sid)
        server_event = ServerEvents(request.sid)

        answer = UserAnswer()
        self.user_answers[request.sid] = answer

        game = GameConstructor(GameSettings(**data['data']),
                               WebInterface(server_event, answer))
        game.run()

        # thread = threading.Thread(
        #     target=run_(data['data'],server_event , user_answer),
        #     name="request.sid",
        #     # daemon=True
        # )
        # log(thread)
        # log(f"thread {thread}")
        # thread.start()
        # thread.join()

    def on_stop_game(self, data):
        print("stop game", data)

    def on_user_answer(self, data):
        self.user_answers[request.sid].message = data['data']
        print('on_user_answer', self.user_answers[request.sid], request.sid)


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
