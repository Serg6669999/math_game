import datetime
import time
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
    def choice_user_action(self, actions: Iterable[str]) -> List[str]:
        pass

    @abstractmethod
    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        pass

    @abstractmethod
    def get_user_answer(self) -> str:
        pass

    incorrect_answers = 0

    def _action_sequence_of_numbers(self, user_action, game_class,
                                    deferred_step: int = 1):
        self.send_message_to_user(vars(game_class))
        time.sleep(1.1)
        sequence_of_numbers = game_class.get_random_pairs_of_numbers_with_math_action(
            user_action)
        show_message_time = getattr(game_class, 'show_message_time', None)
        arithmetic_number = getattr(game_class, 'arithmetic_number', '')

        deferred_numbers_for_calculations = []
        for i, (numbers_for_calculations_, math_action_) in enumerate(
                sequence_of_numbers, start=1):

            self.send_message_to_user(
                f"{numbers_for_calculations_}, {math_action_} {arithmetic_number}",
                show_message_time)
            user_answer = self.get_user_answer()

            deferred_numbers_for_calculations.append(numbers_for_calculations_)
            if i % deferred_step == 0 or len(
                    deferred_numbers_for_calculations) == deferred_step:
                numbers_for_calculations = deferred_numbers_for_calculations.pop(
                    0)
            else:
                continue

            maybe_answer_true, true_answer = game_class.check_answer(
                math_action_, user_answer, numbers_for_calculations)

            if maybe_answer_true:
                self.send_message_to_user("ok")
            else:
                self.incorrect_answers += 1
                self.send_message_to_user(
                    f"{numbers_for_calculations} - {user_answer} is false, true= {true_answer}")
                sequence_of_numbers.append((numbers_for_calculations, math_action_))
                self.get_user_answer()

    @mark_time
    def get_math_game(self, actions: Iterable[str], game_class,
                      deferred_step: int = 1):
        user_math_action = self.choice_user_action(actions)
        while True:
            game_class.incorrect_answers = 0
            self._action_sequence_of_numbers(user_math_action, game_class,
                                             deferred_step)
            message = f"incorrect_answers = {game_class.incorrect_answers}. " \
                      f"Is next level? (yes/no)"
            self.send_message_to_user(message)
            user_answer = self.get_user_answer()
            if user_answer == 'yes':
                game_class.set_next_level()


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
