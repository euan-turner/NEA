from prettytable import PrettyTable
from board import Board
import pygame

class Interface:

    def output_board(board : Board):

        board_output = board.output()
        table = PrettyTable()
        table.header = False
        table.hrules = True
        for row in board_output:
            table.add_row(row)
        print(table)



class Button():
    """Generic button class
    """

    def __init__(self, rect : pygame.Rect, colour : tuple,
            hoveredColour : tuple, clickedColour : tuple):
        self.rect = rect
        self.colour = colour
        self.hov_colour = hoveredColour
        self.click_colour = clickedColour
        self.hovered = False
        self.clicked = False

    def check_click(self, event : pygame.event, window : pygame.Surface) -> tuple:
        """Check if button has been clicked

        Args:
            event (pygame.event): Event instance, only passing in mousedown
                events will be more efficient
            window ([type]): Surface buttons exists on

        Returns:
            tuple: Centre co-ordinates of button, used to identify
                - may change if I find a more efficient method of identification
        """
        if self.rect.collidepoint(event.pos) and not self.clicked:
            self.clicked = True
            self.update(window)
            return self.rect.center
        else:
            return None

    def check_hover(self):
        """Checks if mouse is hovering over button
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def update(self, window : pygame.Surface):
        """Updates the buttons appearance in the window
        Should be called every frame for each button

        Args:
            window (pygame.Surface): Surface button exists on
        """
        self.check_hover()
        if self.clicked:
            window.fill(self.click_colour, self.rect)
        elif self.hovered:
            window.fill(self.hov_colour, self.rect)
        else:
            window.fill(self.colour, self.rect)
        pygame.display.flip()
