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
    def __init__(self, class_interface):
        self.interface_class_obj = class_interface

    def check_answer(self, math_action: str, answer: int, data: Tuple[int, int]):
        true_answer = MathAction(data).get_arithmetic_actions()[math_action]
        return answer == true_answer, true_answer

    def _get_random_pairs_of_numbers(self) -> list:
        return [(random.randint(1, 11), random.randint(9, 20)) for i in range(1, 10)]

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

    def send_message_to_user(self, message: str):
        return self.interface_class_obj.send_message_to_user(self, message)

    def get_user_math_action(self, math_actions: Iterable[str]) -> List[str]:
        return self.interface_class_obj.get_user_math_action(self, math_actions)

    def get_user_answer(self) -> int:
        return self.interface_class_obj.get_user_answer(self)

