import re
from typing import Iterable, List

from math_game.storage.Storage import File
from math_game.business_rules import GameRule


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


class Verb(GameRule):
    level = 1
    words_in_level = 10
    file_path = "/media/serg/ostree/serg/Документы/книги/english/dictionary/"
    file_name = "without_transcriptions_verb.csv"
    # file_name = "body.csv"
    file_name = "duolingvo.csv"
    # file_name = "test.csv"

    def __init__(self, interface_class):
        self.interface_class_obj = interface_class
        self._words_list = self._get_words_list()
        self.__file.close()

    def set_level(self, level):
        self.level = level

    def _get_words_list(self):
        self.__file = File(self.file_path, self.file_name)
        self.__file.open()
        return self.__file.read()

    def choice_user_action(self, actions: Iterable[str]) -> List[str]:
        return self.interface_class_obj.choice_user_action(self, actions)

    def get_user_answer(self) -> str:
        return self.interface_class_obj.get_user_answer(self)

    def send_message_to_user(self, message: str,
                             show_message_time: float = None):
        return self.interface_class_obj.send_message_to_user(self, message,
                                                             show_message_time)

    def check_answer(self, action: str, answer: str, ru_word: str):
        _answer = [" ".join(re.findall(r"\w+", answer))]
        true_answer = Translate(self._words_list).ru_en(ru_word)
        return _answer == true_answer, true_answer

    def get_random_pairs_of_numbers_with_math_action(self, action):
        first_index = self.words_in_level * (self.level - 1)
        second_index = self.words_in_level * self.level
        level_words_list = self._words_list[first_index:second_index]
        return [(list(word.values())[0], action) for word in level_words_list]

    def set_next_level(self):
        self.level += 1
