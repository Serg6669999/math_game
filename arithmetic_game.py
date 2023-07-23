import random
from typing import List, Tuple, Iterable

from business_rules import GameRule, ArithmeticRules


class MathAction(ArithmeticRules):
    def __init__(self, data: Tuple[int, int]):
        super().__init__(data)

    def get_arithmetic_actions(self) -> dict:
        action_dict = {
            "*": self.multiplication(),
            "+": self.sum(),
            "-": self.subtraction(),
            "/": self.division(),
            "**": self.exponentiation()
        }
        return action_dict


class ArithmeticGame(GameRule):
    First_range_of_numbers = (1, 9)
    Second_range_of_numbers = (1, 9)

    def __init__(self, interface_class):
        self.interface_class_obj = interface_class

    def check_answer(self, math_action: str, answer: str, data: Tuple[int, int]):
        true_answer = MathAction(data).get_arithmetic_actions()[math_action]
        return int(answer) == true_answer, true_answer

    def _get_random_pairs_of_numbers(self) -> list:
        return [(random.randint(*self.First_range_of_numbers),
                 random.randint(*self.Second_range_of_numbers))
                for i in range(1, 10)
                ]

    def get_random_pairs_of_numbers_with_math_action(self, math_actions: List[str]):
        for data in self._get_random_pairs_of_numbers():
            math_action = random.choice(math_actions)
            yield data, math_action

    def start(self):
        math_actions = MathAction((1, 1)).get_arithmetic_actions().keys()
        delta_time, end_time = self.get_math_game(
                                    math_actions,
                                    ArithmeticGame(self.interface_class_obj)
                                    )
        return delta_time, end_time

    def send_message_to_user(self, message: str, show_message_time: float = None):
        return self.interface_class_obj.send_message_to_user(self, message,
                                                             show_message_time)

    def choice_user_math_action(self, math_actions: Iterable[str]) -> List[str]:
        return self.interface_class_obj.choice_user_math_action(self, math_actions)

    def get_user_answer(self) -> str:
        return self.interface_class_obj.get_user_answer(self)


class FastArithmeticGame(ArithmeticGame):
    First_range_of_numbers = (1, 9)
    show_message_time = 1.5
    numbers = 3
    arithmetic_number = 1

    def check_answer(self, math_action: str, answer: str, data: Tuple[int, int]):
        result_numbers_list = [
                MathAction((self.arithmetic_number, value)).get_arithmetic_actions()[math_action]
                for value in data
        ]
        result_numbers_str = ' '.join(
            list(map(str, result_numbers_list))
        )
        return answer == result_numbers_str, result_numbers_list

    def _get_values(self):
        return [
            random.randint(*self.First_range_of_numbers)
            for i in range(self.numbers)
        ]

    def _get_random_pairs_of_numbers(self) -> list:
        return [self._get_values() for i in range(1, 10)]

    def start(self):
        math_actions = MathAction((1, 1)).get_arithmetic_actions().keys()
        delta_time, end_time = self.get_math_game(
                                    math_actions,
                                    FastArithmeticGame(self.interface_class_obj)
                                    )
        return delta_time, end_time
