import sys
from dataclasses import dataclass

from verb import Verb

sys.path.append('/media/serg/ostree/serg/Документы/расчет рациона питания/mathGame')

from math_game.arithmetic_game import FastArithmeticGame, MathAction, ArithmeticGame


class GameName:
    arithmetic = 'Arithmetic'
    memory_arithmetic = 'Memory+Arithmetic'
    memory = 'Memory'
    words = 'Words'


@dataclass
class GameSettings:
    game_name: str
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

    def start(self, deferred_step: int = 1):
        math_actions = ", ".join(MathAction((1, 1)).get_arithmetic_actions().keys())
        delta_time, end_time = self.game_class.get_math_game(
            math_actions,
            self.game_class,
            deferred_step
        )
        return delta_time, end_time


class GameConstructor:
    def __init__(self, settings: GameSettings, interface):
        self.interface = interface
        self.settings = settings

    def arithmetic(self):
        return Game(ArithmeticGame(self.interface))

    def memory_arithmetic(self):
        return Game(FastArithmeticGame(self.interface))

    def memory(self):
        game = Game(FastArithmeticGame(self.interface))
        game.game_class.arithmetic_number = 1
        game.game_class.choice_user_action = lambda action: ['*']
        return game

    def words(self):
        return Game(Verb(self.interface))

    def run(self):
        game_dict = {
            GameName.arithmetic: self.arithmetic(),
            GameName.memory_arithmetic: self.memory_arithmetic(),
            GameName.memory: self.memory(),
            GameName.words: self.words()
        }
        game_obj = game_dict[self.settings.game_name]
        game_obj.game_class.max_steps = self.settings.max_steps_of_level
        game_obj.game_class.level = self.settings.entry_level
        game_obj.start(self.settings.delayed_response)


if __name__ == '__main__':
    pass
        # storage_entities = StorageEntities(
        #     date=end_time,
        #     time=delta_time,
        #     incorrect_answers=arithmetic_game.incorrect_answers,
        #     arithmetic_data=(arithmetic_game.First_range_of_numbers,
        #                      arithmetic_game.Second_range_of_numbers)
        #    )
        # Storage(storage_entities).save_to_csv_file("stats.csv")
        # arithmetic_game.send_message_to_user(f"{storage_entities.__dict__}")

