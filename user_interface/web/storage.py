from dataclasses import dataclass


@dataclass
class UserAnswer:
    message: str or None
    is_game_active: bool
