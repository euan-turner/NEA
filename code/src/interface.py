from prettytable import PrettyTable
from board import Board
from button import Button
from auxiliary import Player_Type
import pygame
import os


pygame.init()

##Colours
BLACK = (0,0,0)
DEEP_RED = (129,27,27)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

class Interface:

    def __init__(self, base_theme):
        self.base_theme = base_theme
        self.active_buttons = []
        self.players = [Player_Type.human, Player_Type.human]

    def create_window(self):
        """Creates the main window used by the application
        """
        self.window = pygame.display.set_mode((600,400))
        pygame.display.set_caption("Connect 4 Application")
        self.window.fill(self.base_theme)
        pygame.display.flip()

    def home_menu_window(self) -> int:
        """Runs the home menu window and gets the user's chocie

        Returns:
            int: Code representing application component choice
        """
        self.create_window()
        self.home_menu_window_setup()

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
                        if choice == 'menu':
                            ##Clear menu button
                            button.clear(self.window, self.base_theme)
                            self.active_buttons.remove(button)
                            self.menu_options()
                            break ##Clear current event queue being processed

                        elif choice != None:
                            return choice

    def home_menu_window_setup(self):
        """Sets up the initial view and buttons for the home window
        """
        self.menu_button_setup()
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

        self.window.blit(board_surface, (board_x,board_y))
        self.window.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    def menu_button_setup(self):
        """Adds the initial menu button to a window
        """
        ##Path to hamburger menu image
        menu_image_path = self.get_image_path('menu.png')

        ##Surfaces for menu button
        menu_surface = pygame.image.load(menu_image_path)
        default_menu_surface = pygame.transform.scale(menu_surface, (50, 50))
        hovered_menu_surface = pygame.transform.scale(menu_surface, (55, 55))
        ##Clicked menu surface can just be default, as it will only be visible for an instant
        menu_button = Button(pygame.Rect(5, 5, 60, 60), default_menu_surface,
            hovered_menu_surface, default_menu_surface, 'menu')
        menu_button.update(self.window, self.base_theme)
        self.active_buttons.append(menu_button)

    def menu_options(self):
        """Adds the menu option buttons once menu button clicked
        """
        ##Text button labels
        labels = ["Play a Human", "Play the AI", "Load a Position", "Load a Game", "Quit the App"]
        codes = ['play', 'ai', 'position', 'game', 'out']

        for i in range(len(labels)):
            label = labels[i]
            code = codes[i]
            ##Surfaces
            font = pygame.font.SysFont('rockwell', 10)
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

    def game_window(self, board : Board):
        """Runs the game window, allowing a user to play a game against a human or ai

        Args:
            board (Board): Current board instance

        Returns:
            [type]: [description]
        """
        self.create_window()
        game_surface = self.game_window_setup()
        ##Initial button setup
        self.turn_setup(board)

        ##Main loop for game window
        cont = True
        while cont:
            ##Update all active buttons
            for button in self.active_buttons:
                button.update(self.window, self.base_theme)
            ##Check for mouse clicks
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.active_buttons:
                        choice = button.check_click(event, self.window, self.base_theme)
                        ##Menu clicked - run menu options
                        if choice == 'menu':
                            ##Clear menu button
                            button.clear(self.window, self.base_theme)
                            self.active_buttons.remove(button)
                            self.menu_options()
                            break
                        ##Turn played
                        elif choice in range(7):
                            self.play_move(choice, board, game_surface)
                            """Need to pull across rest of turn functionality from main"""
                            ##Set up for next turn
                            self.turn_setup(board)
                            break
                        ##Menu option selected
                        elif choice != None:
                            return choice

    def game_window_setup(self) -> pygame.Surface:
        """Sets up most of the initial game window

        Returns:
            pygame.Surface: The board surface moves will be played in
        """
        self.menu_button_setup()
        game_surface = self.game_surface_setup()
        self.window.blit(game_surface, (125,50))
        ##Add save button here
        ##Add user icon here

        return game_surface

    def game_surface_setup(self) -> pygame.Surface:
        """Sets up the initial board view in a separate surface

        Returns:
            pygame.Surface: Separate game surface
        """
        game_surface = pygame.Surface((350,300))
        game_surface.fill(self.base_theme)
        ##Draw board
        for row in range(6):
            for col in range(7):
                ##Co-ordindates are the centre of the back circle
                x = 25 + col*50
                y = 25 + row*50
                pygame.draw.circle(game_surface, WHITE, (x,y), 22, width = 0)

        return game_surface

    def turn_setup(self, board : Board):
        self.clear_turn_buttons()
        ##Player is human so add buttons
        if self.players[board.get_counter() % 2] == Player_Type.human:
            self.add_turn_buttons(board)


    def add_turn_buttons(self, board : Board):
        """Add valid turn buttons to window

        Args:
            board (Board): Current board instance
        """
        valid_moves = board.retrieve_valid_moves()

        for col in valid_moves:
            label = str(col+1)
            ##Surfaces
            font = pygame.font.SysFont('rockwell', 20)
            default_surface = font.render(label, False, BLACK)
            hovered_surface = font.render(label, False, DEEP_RED)
            ##Position
            x = (150 + col*50) - (default_surface.get_width() / 2)
            y = 360
            rect = pygame.Rect(x,y, default_surface.get_width(), default_surface.get_height())
            ##Create button
            button = Button(rect, default_surface, hovered_surface, default_surface, col)
            button.update(self.window, self.base_theme)
            self.active_buttons.append(button)

    def clear_turn_buttons(self):
        """Clear all turn buttons from the window
        For use on ai turn, or when a column has been filled
        """
        for button in self.active_buttons:
            if button.code in range(7):
                button.clear(self.window, self.base_theme)
        self.active_buttons = [b for b in self.active_buttons if b.code not in range(7)]

    def play_move(self, col : int, board : Board, game_surface : pygame.Surface):
        """Plays a move in the board and then game surface
        Game window will need to be updated afterwards

        Args:
            col (int): Column to play in
            board (Board): Current board instance
        """
        ##Get token
        token = self.get_token(board)
        ##Play move in board
        board.make_move(col)

        ##Identify location from col and heights
        height = board.get_height(col) % 7
        ##Work out (top, left) of token to be played
        x = col*50
        y = 300 - 50*height

        ##Blit token to game surface
        game_surface.blit(token, (x,y))
        ##Blit game surface to window
        self.window.blit(game_surface, (125,50))


    def get_token(self, board : Board) -> pygame.Surface:
        """Creates the token to be used to play a move

        Args:
            board (Board): Current board instance

        Returns:
            pygame.Surface: Token to be played
        """
        ##Identify current player using board counter
        if board.get_counter() % 2 == 0:
            colour = RED
        else:
            colour = YELLOW
        ##Create surface
        token = pygame.Surface((50,50))
        ##Make background transparent
        token.fill(BLACK)
        token.set_colorkey(BLACK)

        ##Colour circle depending on player
        pygame.draw.circle(token, colour, (25, 25), 18, width = 0)
        return token





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




