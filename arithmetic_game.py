import random
from re import findall
from typing import List, Tuple
from domen.business_rules import GameRule, ArithmeticRules


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


class Arithmetic(GameRule):

    def __init__(self, interface_class):
        super().__init__()
        self.interface_class_obj = interface_class
        self.First_range_of_numbers = (1, 9)
        self.Second_range_of_numbers = (1, 9)
        self.show_message_time = 0.9
        self.max_steps = 7
        self.level = 1

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        true_answer = MathAction(data).get_arithmetic_actions()[math_action]
        return answer == str(true_answer), true_answer

    def _get_random_pairs_of_numbers(self) -> list:
        return [(random.randint(*self.First_range_of_numbers),
                 random.randint(*self.Second_range_of_numbers))
                for i in range(1, self.max_steps)
                ]

    def get_random_pairs_of_numbers_with_math_action(self,
                                                     math_actions: List[str]):
        return [(data, random.choice(math_actions)) for data in
                self._get_random_pairs_of_numbers()]

    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        return self.interface_class_obj.send_message_to_user(message,
                                                             show_message_time)

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        return f" {math_action} ".join(map(str, numbers_for_calculations))

    def get_user_answer(self) -> str:
        return self.interface_class_obj.get_user_answer()

    def _is_even_numbered(self, number):
        return number % 2 == 0

    def _get_level_ratio(self, level):
        even_numbered = self._is_even_numbered(level)
        if even_numbered:
            first_ratio, second_ratio = 1, 0
        else:
            first_ratio, second_ratio = 0, 1

        return first_ratio, second_ratio

    def set_next_level(self):

        if self.incorrect_answers < 3:
            first_ratio, second_ratio = self._get_level_ratio(self.level)
            self.level += 1
            self.First_range_of_numbers = [i + first_ratio * 10 for i in
                                           self.First_range_of_numbers]
            self.Second_range_of_numbers = [i + second_ratio * 10 for i in
                                            self.Second_range_of_numbers]


class MemoryArithmetic(Arithmetic):
    def __init__(self, interface_class):
        super().__init__(interface_class)
        self.First_range_of_numbers = (1, 9)
        self.arithmetic_number = 2

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        result_numbers_list = [
            MathAction(
                (value, self.arithmetic_number)).get_arithmetic_actions()[
                math_action]
            for value in data
        ]
        answer_number_list = list(map(int, findall(r"\d+", answer)))
        return answer_number_list == result_numbers_list, result_numbers_list

    def _get_values(self) -> List[int]:
        return [
            random.randint(*self.First_range_of_numbers)
            for i in range(self.level + 1)
        ]

    def _get_random_pairs_of_numbers(self) -> List[List[int]]:
        return [self._get_values() for i in range(1, self.max_steps)]

    def set_next_level(self):
        if self.incorrect_answers < 3:
            self.level += 1
            self.show_message_time = self.level * 0.2835

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        return f"{numbers_for_calculations} {math_action} {self.arithmetic_number}"


class Memory(MemoryArithmetic):
    def __init__(self, interface_class):
        super().__init__(interface_class)
        self.arithmetic_number = 1
        self.math_action = '*'

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        return f"{numbers_for_calculations}"
