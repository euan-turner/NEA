from typing import NewType
from threading import Thread
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
    menu = 0
    play = 1
    ai = 2
    position = 3
    game = 4
    out = 5

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

class ReturnThread(Thread):
    """Thread subclass to return the value from the target function
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        """Store result of target function
        """
        if self._target:
            self.result = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        """Return result of target function
        """
        super().join(*args, **kwargs)
        return self.result
