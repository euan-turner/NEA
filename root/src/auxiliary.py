from typing import NewType
import numpy as np

##Custome type definitions
Bitboard = NewType('Bitboard', np.uint64())

##Variable definitions for readability
LSB1 = 1

class Status:
    game_won = 1
    game_drawn = 0
    game_unfinished = -1