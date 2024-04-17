from dataclasses import dataclass


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
    words: str

    def __post_init__(self):
        self.delayed_response = int(self.delayed_response)
        self.max_steps_of_level = int(self.max_steps_of_level)
        self.entry_level = int(self.entry_level)
