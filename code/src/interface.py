from prettytable import PrettyTable
from board import Board
from auxiliary import Main_Menu_Choice
from time import sleep
import pygame
import os


pygame.init()

##Colours
BLACK = (0,0,0)
DEEP_RED = (129,27,27)
class Button():
    """Redefine a generic button class, and inheriting block, text and image button classes
    """

    def __init__(self, rect : pygame.Rect, default : pygame.Surface,
            hovered : pygame.Surface, clicked : pygame.Surface, code : int):
        """Constructor method for a button
        Requires default, hovered, and clicked surface to be preconstructed

        Args:
            rect (pygame.Rect): Position and dimensions of button on surface
            default (pygame.Surface): Image surface of button as default
            hovered (pygame.Surface): Image surface of button when hovered
            clicked (pygame.Surface): Image surface of button when clicked
            code (int): Code to identify button
        """
        self.rect = rect
        self.default = default
        self.hovered_surface = hovered
        self.clicked_surface = clicked
        self.hovered = False
        self.clicked = False
        self.code = code

    def check_click(self, event : pygame.event, window : pygame.Surface, background : tuple) -> tuple:
        """Check if button has been clicked

        Args:
            event (pygame.event): Event instance, only passing in mousedown
                events will be more efficient
            window (pygame.Surface): Surface buttons exists on
            background (tuple): Background colour to wipe with before blit

        Returns:
            int: Code to identify button
        """
        if self.rect.collidepoint(event.pos) and not self.clicked:
            self.clicked = True
            self.update(window, background)
            return self.code
        else:
            return None

    def check_hover(self):
        """Checks if mouse is hovering over button
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def update(self, window : pygame.Surface, background : tuple):
        """Updates the buttons appearance in the window
        Should be called every frame for each button

        Args:
            window (pygame.Surface): Surface button exists on
            background (tuple): Background colour to wipe with before blit
        """
        self.check_hover()
        if self.clicked:
            self.clear(window, background)
            window.blit(self.clicked_surface, self.rect)
        elif self.hovered:
            self.clear(window, background)
            window.blit(self.hovered_surface, self.rect)
        else:
            self.clear(window, background)
            window.blit(self.default, self.rect)
        pygame.display.flip()

    def clear(self, window : pygame.Surface, background : tuple):
        """Clears the button's pixels from the screen

        Args:
            window (pygame.Surface): Surface buttons exists on
            background (tuple): Background colour to wipe with
        """
        window.fill(background, self.rect)
class Interface:

    def __init__(self, base_theme):
        self.base_theme = base_theme
        self.active_buttons = []

    def create_window(self):
        """Creates the main window used by the application
        """
        self.window = pygame.display.set_mode((600,400))
        pygame.display.set_caption("Connect 4 Application")
        self.window.fill(self.base_theme)
        pygame.display.flip()

    def home_menu_window(self):
        self.home_menu_window_setup()

        delay = 0

        ##Main loop for home window
        while True:
            ##Update all active buttons
            for button in self.active_buttons:
                button.update(self.window, self.base_theme)
            ##Check for mouse clicks
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.active_buttons:
                        choice = button.check_click(event, self.window, self.base_theme)
                        ##Menu icon clicked - run menu options
                        if choice == Main_Menu_Choice.menu:
                            ##Clear menu button
                            button.clear(self.window, self.base_theme)
                            self.active_buttons.remove(button)
                            self.home_menu_window_options()
                            break ##Clear current event queue being processed

                        elif choice != None:
                            return choice


    def home_menu_window_setup(self):
        """Sets up the initial view and buttons for the home window
        """
        ##Path to hamburger menu image
        menu_image_path = self.get_image_path('menu.png')
        ##Path to board image
        board_image_path = self.get_image_path('board.png')

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

        ##Surfaces for menu button
        menu_surface = pygame.image.load(menu_image_path)
        default_menu_surface = pygame.transform.scale(menu_surface, (50, 50))
        hovered_menu_surface = pygame.transform.scale(menu_surface, (55, 55))
        ##Clicked menu surface can just be default, as it will only be visible for an instant

        menu_button = Button(pygame.Rect(5, 5, 60, 60), default_menu_surface,
            hovered_menu_surface, default_menu_surface, Main_Menu_Choice.menu)
        menu_button.update(self.window, self.base_theme)
        self.active_buttons.append(menu_button)
        ##self.window.blit(menu_surface, (5,5))
        self.window.blit(board_surface, (board_x,board_y))
        self.window.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    def home_menu_window_options(self):
        ##Text button labels
        labels = ["Play a Human", "Play the AI", "Load a Position", "Load a Game", "Quit the App"]
        codes = [Main_Menu_Choice.play, Main_Menu_Choice.ai, Main_Menu_Choice.position, Main_Menu_Choice.game, Main_Menu_Choice.out]
        for i in range(len(labels)):
            label = labels[i]
            code = codes[i]
            ##Surfaces
            font = pygame.font.SysFont('rockwell', 20)
            default_surface = font.render(label, False, BLACK)
            hovered_surface = font.render(label, False, DEEP_RED)
            ##Position
            x = 5
            y = 5 + i*default_surface.get_height()
            rect = pygame.Rect(x, y, default_surface.get_width(), default_surface.get_height())
            ##Create button
            button = Button(rect, default_surface, hovered_surface, default_surface, code)
            button.update(self.window, self.base_theme)
            self.active_buttons.append(button)





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

    def output_board(board : Board):

        board_output = board.output()
        table = PrettyTable()
        table.header = False
        table.hrules = True
        for row in board_output:
            table.add_row(row)
        print(table)




