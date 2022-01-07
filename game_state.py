from enum import Enum, auto
class Game_state(Enum):
    DECIDE_TURNS = auto()
    SELECT_ORIGIN = auto()
    SELECT_DEST = auto()
    MOVE = auto()
    PIECE_ON_BAR = auto()
    