import sys

from domen.entity import GameSettings, GameName
from settings import DIR_ROOT
from user_interface.console import ConsoleInterface
from words_game import Words

sys.path.append(DIR_ROOT)

from math_game.arithmetic_game import (
    MemoryArithmetic,
    Arithmetic,
    Memory)


class GameConstructor:
    def __init__(self, settings: GameSettings, interface):
        self.interface = interface
        self.settings = settings

    def run(self):
        game_dict = {
            GameName.arithmetic: Arithmetic,
            GameName.memory_arithmetic: MemoryArithmetic,
            GameName.memory: Memory,
            GameName.words: Words
        }
        game_ = game_dict[self.settings.game_name]
        game_obj = game_(self.interface)
        game_obj.math_action = self.settings.math_action
        game_obj.max_steps = self.settings.max_steps_of_level
        game_obj.level = self.settings.entry_level
        game_obj.deferred_step = self.settings.delayed_response
        game_obj.words = self.settings.words
        game_obj.get_math_game()


if __name__ == '__main__':
    game_settings = GameSettings(
        game_name=GameName.arithmetic,
        delayed_response="1",
        max_steps_of_level="5",
        entry_level="1"
    )
    game = GameConstructor(game_settings, ConsoleInterface())
    game.run()
