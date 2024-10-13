import sys
from typing import Dict

from settings import DIR_ROOT, log, STATS_FILE
from storage.Storage import FileP
from user_interface.web.flask.save_file import save_file

sys.path.append(DIR_ROOT)

from flask_socketio import Namespace
from flask import render_template, request, Response, jsonify
from user_agents import parse

from user_interface.web.interface import WebInterface
from user_interface.web.storage import UserAnswer
from user_interface.web.flask.socket_server import app, socketio
from math_game.run import GameConstructor, GameSettings


@app.route('/')
def get_arithmetic_game_(message: str = "Разгони мозг"):
    return render_template('web.html', data=message,
                           sync_mode=socketio.async_mode)

@app.route('/test')
def test(message: str = "test"):
    return render_template('test.html', data=message,
                           sync_mode=socketio.async_mode)


@app.route('/stats')
def stats():
    file = FileP(STATS_FILE)
    file.open()
    file_data = file.read()
    file.close()
    print(type(file_data[0]))
    return render_template('chart.html', sync_mode=socketio.async_mode)


@app.route('/stats_data', methods=["POST"])
def stats_data():
    file = FileP(STATS_FILE)
    file.open()
    file_data = file.read()
    file.close()
    print(type(file_data[0]))
    return jsonify(file_data)



@app.route('/save', methods=['POST'])
def upload_file():
    response = save_file(request)
    if response is not None:
        return response
    else:
        return Response(status=400)


class ClientEvents(Namespace):
    socket_id_user_answers: Dict[str, UserAnswer] = {}

    def on_connect(self):
        user_agent = parse(request.user_agent.string)
        is_mobile = user_agent.is_mobile
        is_tablet = user_agent.is_tablet
        is_ps = user_agent.is_pc
        is_devices = {is_mobile: "mobile", is_tablet: "tablet", is_ps: "ps"}
        log(f"connect P-{is_ps} T-{is_tablet} M-{is_mobile}")
        ServerEvents(request.sid).send_service_message(
            {"device": is_devices[True]})

    def on_disconnect(self):
        self.on_stop_game()

    def on_start_game(self, data):
        log(f"start_game, {request.sid}")
        server_event = ServerEvents(request.sid)

        user_answer = UserAnswer(message=None)
        self.socket_id_user_answers[request.sid] = user_answer

        game = GameConstructor(GameSettings(**data['data']),
                               WebInterface(server_event, user_answer))
        game.run()

    def on_stop_game(self):
        pass

    def on_user_answer(self, data):
        self.socket_id_user_answers[request.sid].message = data['data']
        log(f"on_user_answer, {self.socket_id_user_answers[request.sid]}, {request.sid}")


class ServerEvents:
    def __init__(self, socket_id):
        self.socket_id = socket_id

    def send_message_to_user(self, message: str or dict,
                             show_message_time: float = None):
        log(f'server_message, {message}, {self.socket_id}')
        socketio.emit("server_message", {"data": message}, room=self.socket_id)
        if show_message_time is not None:
            socketio.sleep(show_message_time)
            socketio.emit("server_message", {"data": '-'}, room=self.socket_id)

    def send_level_to_user(self, level: int):
        socketio.emit("level", {"data": level}, room=self.socket_id)

    def send_service_message(self, message: str or dict):
        socketio.emit("service_message", {"data": message},
                      room=self.socket_id)


socketio.on_namespace(ClientEvents())

if __name__ == '__main__':
    log("start")
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
