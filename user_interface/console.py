import time
from typing import Iterable, List, Tuple
import re


class ConsoleInterface:
    def choice_user_action(self, math_actions: Iterable[str]) -> List[str]:
        user_math_action = input(f"choice math action: {math_actions}")
        return user_math_action.split(",")

    def send_message_to_user(self, message: str, show_message_time: float = None):

        if show_message_time:
            print(message, end='')
            time.sleep(show_message_time)
            print('\r', '')
        else:
            print(message)

    def extract_from_text_(self, regular: str, text: str):
        return re.search(f'{regular}', text).group()

    def get_user_answer(self) -> str:
        return input()
