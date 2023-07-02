import datetime
from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple
import math


def mark_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        delta_time = (end_time - start_time).total_seconds()
        return delta_time, end_time
    return wrapper


class GameRule(ABC):

    @abstractmethod
    def get_user_math_action(self, math_actions: Iterable[str]) -> List[str]:
        pass

    @abstractmethod
    def send_message_to_user(self, message: str):
        pass

    @abstractmethod
    def get_user_answer(self) -> int:
        pass
    incorrect_answers = 0

    @mark_time
    def get_math_game(self, math_actions: Iterable[str], game_class):
        user_math_action = self.get_user_math_action(math_actions)
        sequence_of_numbers = game_class.get_random_pairs_of_numbers_with_math_action(user_math_action)
        for data, math_action_ in sequence_of_numbers:
            self.send_message_to_user(f"{data}, {math_action_}")
            user_answer = self.get_user_answer()

            maybe_answer_true, true_answer = game_class.check_answer(
                math_action_, user_answer, data)

            if maybe_answer_true:
                self.send_message_to_user("ok")
            else:
                self.incorrect_answers += 1
                self.send_message_to_user(f"{user_answer} false, true= {true_answer}")


class ArithmeticRules:
    def __init__(self, data: Tuple[int, int]):
        self.x, self.y = data

    def multiplication(self) -> int:
        return self.x * self.y

    def sum(self) -> int:
        return self.x + self.y

    def subtraction(self) -> int:
        return self.x - self.y

    def division(self) -> float:
        return self.x / self.y

    def exponentiation(self) -> int:
        return self.x ** self.y


class TrigonometricFunctions:
    def __init__(self, value: float):
        self.value = value

    def sin(self):
        return math.sin(self.value)

    def cos(self):
        return math.cos(self.value)

    def tan(self):
        return math.tan(self.value)

    def atan(self):
        return math.atan(self.value)