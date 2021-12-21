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

class Save_Type:
    position = 1
    game = 0

class Main_Menu_Choice:
    play = 1
    load = 2
    ai = 3

class Load_Menu_Choice:
    position = 1
    game = 2
class Player_Type:
    ai = 1
    human = 2

def get_confirmation():
    """Generic method to accept confirmation of an input

    Returns:
        boolean: Confirmed - True, Not confirmed - False
    """
    while True:
        try:
            conf = input("Confirm input (Y/N): ").upper()
            if conf not in {'Y', 'N'}:
                print("Invalid input")
            elif conf == 'Y':
                return True
            else:
                return False
        except:
            print("Invalid input")
