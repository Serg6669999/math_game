from typing import Iterable, List

from math_game.user_interface.base import Interface
from user_interface.web.flask.socket_server import socketio


class WebInterface(Interface):
    def __init__(self, server_events, user_answer):

        self.server_events = server_events
        self.user_answer = user_answer

    def choice_user_action(self, math_actions: Iterable[str]) -> List[str]:
        message = f"choice math action: {math_actions}"
        self.send_message_to_user(message)
        answer = self.get_user_answer()
        return answer.split(",")

    def send_level_to_user(self, level: int):
        self.server_events.send_level_to_user(level)

    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        self.server_events.send_message_to_user(str(message), show_message_time)

    def _await_answer_loop(self):
        answer = self.user_answer.message
        while answer is None:
            socketio.sleep(0.1)
            answer = self.user_answer.message
        else:
            self.user_answer.message = None
            return answer

    def get_user_answer(self) -> str:
        return self._await_answer_loop()
