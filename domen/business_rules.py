import datetime
from abc import ABC, abstractmethod
from typing import List, Tuple
import math

from settings import log


def mark_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        delta_time = (end_time - start_time).seconds
        return delta_time, end_time

    return wrapper


class GameRule(ABC):
    def __init__(self):
        self.incorrect_answers = 0
        self.show_message_time = None
        self.deferred_step = 1
        self.__math_action = ""

    @property
    def math_action(self):
        return self.__math_action

    @math_action.setter
    def math_action(self, text: str):
        if self.__math_action == "":
            self.__math_action = text

    @abstractmethod
    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        pass

    @abstractmethod
    def get_user_answer(self) -> str:
        pass

    @abstractmethod
    def get_random_pairs_of_numbers_with_math_action(
            self, math_actions: List[str]) -> List[Tuple]:
        pass

    @abstractmethod
    def check_answer(self, action: str, answer: str, data: any) -> Tuple[bool, str]:
        # return (is_answer_true, true_answer)
        pass

    @abstractmethod
    def set_next_level(self):
        pass

    @abstractmethod
    def get_user_task(self,
                      numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        pass

    @mark_time
    def _action_sequence_of_numbers(self, user_action):

        sequence_of_numbers = self.get_random_pairs_of_numbers_with_math_action(
            user_action)

        deferred_numbers_for_calculations = []
        for i, (numbers_for_calculations_, math_action_) in enumerate(
                sequence_of_numbers, start=1):

            user_task = self.get_user_task(numbers_for_calculations_, math_action_)

            self.send_message_to_user(user_task, self.show_message_time)
            user_answer = self.get_user_answer()

            deferred_numbers_for_calculations.append(numbers_for_calculations_)
            if i % self.deferred_step == 0 or len(
                    deferred_numbers_for_calculations) == self.deferred_step:
                numbers_for_calculations = deferred_numbers_for_calculations.pop(0)
            else:
                continue

            maybe_answer_true, true_answer = self.check_answer(
                math_action_, user_answer, numbers_for_calculations)

            if maybe_answer_true:
                self.send_message_to_user("ok")
            else:
                self.incorrect_answers += 1
                self.send_message_to_user(
                    f"{user_answer} is false, true= {true_answer}")
                sequence_of_numbers.append((numbers_for_calculations, math_action_))
                self.get_user_answer()

    @mark_time
    def get_math_game(self, game_class):
        # TODO remove game_class
        log(f"{vars(game_class)}")
        is_game_active = game_class.interface_class_obj.user_answer.is_game_active
        while is_game_active:
            self.incorrect_answers = 0
            delta_time, end_time = self._action_sequence_of_numbers(self.math_action)
            message = f"wrongs = {self.incorrect_answers}; " \
                      f"{delta_time}sec; " \
                      f"Is next level? (yes/no)"
            self.send_message_to_user(message)
            user_answer = self.get_user_answer()
            if user_answer.lower() == 'yes':
                self.set_next_level()


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
