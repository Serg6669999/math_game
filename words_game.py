import re
from typing import List

from math_game.storage.Storage import File
from domen.business_rules import GameRule
from settings import DIR_ROOT, log


class Action:
    translate_type = {'Ru-En', 'En-Ru'}

    def __init__(self, action_object: object, action_type: str):
        self.action_object = action_object
        self.action_type = action_type

    def get(self):
        return self.action_object.get(self.action_type)


class Translate:
    def __init__(self, words_list: List[dict]):
        self.words_list = words_list

    def ru_en(self, ru_words: str) -> List[str]:
        def without_none(l: list):
            return [v for v in l if v != None]

        return [word for words in self.words_list for word in
                without_none(list(words.values()))[1:]
                if list(words.values())[0] == ru_words][:3]

    def en_ru(self, word: str) -> str:
        pass


class Words(GameRule):
    def __init__(self, interface_class):
        super().__init__()
        self.interface_class_obj = interface_class
        self.level = 1
        self.max_steps = 10
        self.__file_path = f"{DIR_ROOT}/math_game/storage/english_words/"
        self._words = ""
        self._words_list = list

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, text: str):
        self._words = text

    def set_level(self, level):
        self.level = level

    def _get_words_list(self) -> list[dict]:
        file_name = f"{self.words}.csv"
        file = File(self.__file_path, file_name)
        file.open()
        result = file.read()[:]
        file.close()
        return result

    def get_user_answer(self) -> str:
        return self.interface_class_obj.get_user_answer()

    def get_user_task(self, numbers_for_calculations: List[int],
                      math_action: str) -> str:
        return f"{numbers_for_calculations}"

    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        return self.interface_class_obj.send_message_to_user( message,
                                                             show_message_time)

    def check_answer(self, action: str, answer: str, ru_word: str):
        _answer = (re.findall(r"\w+", answer))
        true_answer = Translate(self._words_list).ru_en(ru_word)
        log(_answer, type(_answer), true_answer, type(true_answer))
        return _answer == true_answer, true_answer

    def get_random_pairs_of_numbers_with_math_action(self, action):
        self._words_list = self._get_words_list()
        first_index = self.max_steps * (self.level - 1)
        second_index = self.max_steps * self.level
        level_words_list = self._words_list[first_index:second_index]
        return [(list(word.values())[0], action) for word in level_words_list]

    def set_next_level(self):
        self.level += 1
