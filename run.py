import sys
from dataclasses import dataclass

from settings import DIR_ROOT
from user_interface.console import ConsoleInterface
from words import Words

sys.path.append(DIR_ROOT)

from math_game.arithmetic_game import (
    MemoryArithmetic,
    Arithmetic,
    Memory)


class GameName:
    arithmetic = 'Arithmetic'
    memory_arithmetic = 'Memory+Arithmetic'
    memory = 'Memory'
    words = 'Words'


@dataclass
class GameSettings:
    game_name: str
    math_action: str
    delayed_response: str or int
    max_steps_of_level: str or int
    entry_level: str or int

    def __post_init__(self):
        self.delayed_response = int(self.delayed_response)
        self.max_steps_of_level = int(self.max_steps_of_level)
        self.entry_level = int(self.entry_level)


class Game:
    def __init__(self, game_class):
        self.game_class = game_class

    def start(self):
        delta_time, end_time = self.game_class.get_math_game(self.game_class)
        return delta_time, end_time


class GameConstructor:
    def __init__(self, settings: GameSettings, interface):
        self.interface = interface
        self.settings = settings

    def run(self):
        game_dict = {
            GameName.arithmetic: Game(Arithmetic(self.interface)),
            GameName.memory_arithmetic: Game(MemoryArithmetic(self.interface)),
            GameName.memory: Game(Memory(self.interface)),
            GameName.words: Game(Words(self.interface))
        }
        game_obj = game_dict[self.settings.game_name]
        game_obj.game_class.math_action = self.settings.math_action
        game_obj.game_class.max_steps = self.settings.max_steps_of_level
        game_obj.game_class.level = self.settings.entry_level
        game_obj.game_class.deferred_step = self.settings.delayed_response
        game_obj.start()


if __name__ == '__main__':
    game_settings = GameSettings(
        game_name=GameName.arithmetic,
        delayed_response="1",
        max_steps_of_level="5",
        entry_level="1"
    )
    game = GameConstructor(game_settings, ConsoleInterface())
    game.run()
    # storage_entities = StorageEntities(
    #     date=end_time,
    #     time=delta_time,
    #     incorrect_answers=arithmetic_game.incorrect_answers,
    #     arithmetic_data=(arithmetic_game.First_range_of_numbers,
    #                      arithmetic_game.Second_range_of_numbers)
    #    )
    # Storage(storage_entities).save_to_csv_file("stats.csv")
    # arithmetic_game.send_message_to_user(f"{storage_entities.__dict__}")
