from abc import ABC, abstractmethod
from typing import Iterable, List


class Interface(ABC):

    @abstractmethod
    def choice_user_action(self, math_actions: Iterable[str]) -> List[str]:
        pass

    @abstractmethod
    def send_message_to_user(self, message: str, show_message_time: float = None):
        pass

    @abstractmethod
    def get_user_answer(self) -> str:
        pass