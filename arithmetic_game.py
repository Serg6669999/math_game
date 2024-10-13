import random
from re import findall
from typing import List, Tuple
from domen.business_rules import GameRule, ArithmeticRules
from domen.entity import GameName


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
        self.show_message_time = (self.level + 1) / 2.5
        self.max_steps = 7

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        true_answer = MathAction(data).get_arithmetic_actions()[math_action]
        numbers_list = findall(r"\d+", answer)
        number_answer = int(numbers_list[0]) if len(numbers_list) != 0 else ""
        return number_answer == true_answer, true_answer

    def _get_random_pairs_of_numbers(self) -> list:
        first_range_of_numbers, second_range_of_numbers = self._get_first_second_range_of_numbers(
            self.level)
        return [(random.randint(*first_range_of_numbers),
                 random.randint(*second_range_of_numbers))
                for i in range(1, self.max_steps)
                ]

    def get_random_pairs_of_numbers_with_math_action(self,
                                                     math_actions: List[str]):
        return [(data, random.choice(math_actions)) for data in
                self._get_random_pairs_of_numbers()]

    def send_level_to_user(self, level: int):
        self.interface_class_obj.send_level_to_user(level)

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

    def get_game_name(self) -> GameName:
        return GameName.arithmetic

    def _is_even_numbered(self, number):
        return number % 2 == 0

    def _get_first_second_range_of_numbers(self, level: int):

        def get_first_second_numbers(level_):
            number_1 = level_ * 5
            number_2 = number_1 + 9
            first_numbers = (1 if number_1 - 10 == 0 else number_1 - 10, number_2 - 10)
            second_numbers = (number_1, number_2)

            print(first_numbers, second_numbers, level_)

            return first_numbers, second_numbers

        if self._is_even_numbered(level):
            return get_first_second_numbers(level)
        else:
            first_numbers, _ = get_first_second_numbers(level + 1)
            return first_numbers, first_numbers

    def set_next_level(self):

        if self.incorrect_answers < 3:
            self.level += 1
            self.show_message_time = (self.level + 1) / 2.5
            self.First_range_of_numbers, self.Second_range_of_numbers = self._get_first_second_range_of_numbers(self.level)


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
            self.show_message_time = (self.level + 1) / 2.5

    def get_game_name(self) -> GameName:
        return GameName.memory_arithmetic

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        return f"{numbers_for_calculations} {math_action} {self.arithmetic_number}"


class Memory(MemoryArithmetic):
    def __init__(self, interface_class):
        super().__init__(interface_class)
        self.arithmetic_number = 1
        self.math_action = '*'

    def get_game_name(self) -> GameName:
        return GameName.memory

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str,
                      ) -> str:
        return f"{numbers_for_calculations}"

    def check_answer(self, math_action: str, answer: str,
                     data: Tuple[int, int]):
        result_numbers_list = [
            MathAction(
                (value, self.arithmetic_number)).get_arithmetic_actions()[
                math_action]
            for value in data
        ]
        answer_number_list = [int(char) for char in answer if char.isdigit()]
        return answer_number_list == result_numbers_list, result_numbers_list
