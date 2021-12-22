from prettytable import PrettyTable
from board import Board
import pygame
import os

pygame.init()

##Colours
BLACK = (0,0,0)

class Interface:

    def __init__(self, back_theme):
        self.back_theme = back_theme

    def output_board(board : Board):

        board_output = board.output()
        table = PrettyTable()
        table.header = False
        table.hrules = True
        for row in board_output:
            table.add_row(row)
        print(table)

    def create_window(self):
        """Creates the main window used by the application
        """
        self.window = pygame.display.set_mode((600,400))
        pygame.display.set_caption("Connect 4 Application")
        self.window.fill(self.back_theme)
        pygame.display.flip()

    def home_window(self):
        ##Path to hamburger menu image
        menu_image_path = self.get_image_path('menu.png')
        ##Path to board image
        board_image_path = self.get_image_path('board.png')

        ##Surface for menu
        menu_surface = pygame.image.load(menu_image_path)
        menu_surface = pygame.transform.scale(menu_surface, (50, 50))

        ##Surface for board
        board_surface = pygame.image.load(board_image_path)
        board_surface = pygame.transform.scale(board_surface, (250,200))

        ##Surface for text
        font = pygame.font.SysFont('rockwell', 50)
        text_surface = font.render('Connect 4', False, BLACK)



        ##Centre board surface
        board_x = (self.window.get_width() / 2) - (board_surface.get_width() / 2)
        board_y = (self.window.get_height() / 2) - (board_surface.get_height() / 2)

        ##Centre text surface
        text_x = (self.window.get_width() / 2) - (text_surface.get_width() / 2)
        text_y = (self.window.get_height() / 4) - text_surface.get_height()

        self.window.blit(menu_surface, (5,5))
        self.window.blit(board_surface, (board_x,board_y))
        self.window.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    def get_image_path(self, filename : str) -> str:
        """Gets the path of an image in the images directory
        Assumes the following directory structure
        src - interface.py
        |
        images

        Args:
            filename (str): Filename of desired image

        Returns:
            str: Path to desired image
        """
        file_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(file_path, '..', '..', 'images', filename)
        return os.path.normpath(image_path)




class Button():
    """Redefine a generic button class, and inheriting block, text and image button classes
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
