from board import Board
from button import Button
from auxiliary import Player_Type, Status, Save_Type, ReturnThread
from storage import save
from ai import Minimax
import tkinter as tk
import pygame
import os
from time import sleep


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
        self.players = []
        self.ai_strength = 0

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
            self.update_active_buttons()
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
            hovered_menu_surface, 'menu')
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
            button = Button(rect, default_surface, hovered_surface, code)
            button.update(self.window, self.base_theme)
            self.active_buttons.append(button)

    def game_window(self, board : Board):
        """Runs the game window, allowing a user to play a game against a human or ai
        Needs players to be set before running
        Args:
            board (Board): Current board instance

        Returns:
            str: Code for next part of the application to use
        """
        self.create_window()
        game_surface = self.game_window_setup()
        ##Initial button setup
        self.turn_setup(board)

        ##Main loop for game window
        return_code = None
        ##While turns are continuing
        while return_code == None:
            ##Human turn
            if self.players[board.get_counter() % 2] == Player_Type.human:
                return_code = self.game_loop(board, game_surface)
            ##AI turn
            else:
                ai = Minimax(board.get_move_history(), self.ai_strength)
                move = ai.search()
                self.play_move(move, board, game_surface)
                return_code = self.terminal_check(board, game_surface)


        return return_code

    def game_loop(self, board : Board, game_surface : pygame.Surface):
        """Runs the game while checking all button clicks
        Codes being returned:
        home - Return to home window
        menu options - Run selected component
        None - Run game loop for next turn

        Args:
            board (Board): Current board instance
            game_surface (pygame.Surface): Individual game surface

        Returns:
            str: Code for next part of application to use
        """
        while True:
            self.update_active_buttons()
            ##Check for mouse clicks
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ##Check if a button was clicked
                    for button in self.active_buttons:
                        code = button.check_click(event, self.window, self.base_theme)
                        ##Menu clicked - run menu options
                        if code == 'menu':
                            ##Make necessary window updates
                            button.clear(self.window, self.base_theme)
                            self.active_buttons.remove(button)
                            self.menu_options()
                            break ##Clear current event queue
                        ##Turn played
                        elif code in range(7):
                            self.play_move(code, board, game_surface)
                            state = board.game_over()
                            return self.terminal_check(board, game_surface)
                        ##Menu option selected
                        elif code != None:
                            return code

    def end_game_output(self, game_surface : pygame.Surface, message : str, board : Board):
        """Runs when a game finishes
        Saves the game if desired

        Args:
            game_surface (pygame.Surface): Separate game surface
            message (str): Game drawn or won
            board (Board): Current board instance (to save)
        """
        pygame.display.flip()
        sleep(2)
        ##Remove board display
        game_surface.fill(self.base_theme)
        self.window.blit(game_surface, (125,50))

        ##Remove turn buttons
        self.clear_turn_buttons()

        ##Remove menu buttons - no longer needed
        ##User will be returned to home window
        for button in self.active_buttons:
            button.clear(self.window, self.base_theme)
        self.active_buttons = []


        ##Add text surfaces
        message_font = pygame.font.SysFont('rockwell', 50)
        message_surface = message_font.render(message, False, BLACK)
        message_x = (self.window.get_width() / 2) - message_surface.get_width() / 2
        message_y = self.window.get_height() / 4
        self.window.blit(message_surface, (message_x, message_y))

        save_font = pygame.font.SysFont('rockwell', 40)
        save_surface = save_font.render('Save Game?', False, BLACK)
        save_x = (self.window.get_width() / 2) - save_surface.get_width() / 2
        save_y = message_y + message_surface.get_height() + 10
        self.window.blit(save_surface, (save_x, save_y))

        ##Add Yes/No buttons
        font = pygame.font.SysFont('rockwell', 30)
        yes_surface = font.render('Yes', False, BLACK)
        yes_hovered_surface = font.render('Yes', False, DEEP_RED)
        yes_x = save_x
        yes_y = save_y + yes_surface.get_height() + 10
        yes_rect = pygame.Rect(yes_x, yes_y, yes_surface.get_width(), yes_surface.get_height())
        yes_button = Button(yes_rect, yes_surface, yes_hovered_surface, 'yes')
        yes_button.update(self.window, self.base_theme)
        self.active_buttons.append(yes_button)

        no_surface = font.render('No', False, BLACK)
        no_hovered_surface = font.render('No', False, DEEP_RED)
        no_x = save_x + save_surface.get_width() - no_surface.get_width()
        no_y = yes_y
        no_rect = pygame.Rect(no_x, no_y, no_surface.get_width(), no_surface.get_height())
        no_button = Button(no_rect, no_surface, no_hovered_surface, 'no')
        no_button.update(self.window, self.base_theme)
        self.active_buttons.append(no_button)

        ##Check for event
        while True:
            self.update_active_buttons()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ##Check if a button was clicked
                    for button in self.active_buttons:
                        code = button.check_click(event, self.window, self.base_theme)
                        ##Yes - save game
                        if code == 'yes':
                            save(Save_Type.game, board, 'Connect4.db')
                            return
                        elif code == 'no':
                            return

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
        """Set up the buttons for the next turn

        Args:
            board (Board): Current board instance
        """
        self.clear_turn_buttons()
        ##Player is human so add buttons
        if self.players[board.get_counter() % 2] == Player_Type.human:
            self.add_turn_buttons(board)
        pygame.display.flip()

    def ai_player_setup(self):
        """Runs the setup window for the ai and sets necessary attributes
        """

        def tk_output():
            """Sets attributes with given values
            """
            player = radio_output.get()
            strength = strength_output.get()
            if player == 1:
                self.set_players(Player_Type.ai, Player_Type.human)
            else:
                self.set_players(Player_Type.human, Player_Type.ai)
            self.set_ai_strength(strength)
            root.destroy() ##Terminate window

        root = tk.Tk()
        root.geometry("100x235")
        root.title("Set AI")
        ##Convert base theme tuple into hex string
        col = '#' + ''.join([hex(i)[2:] for i in self.base_theme])
        root.configure(background = col)

        ##Player frame
        player_frame = tk.Frame(root)
        player_frame.grid(row = 0, column = 0, padx = 5, pady = 5)

        tk.Label(player_frame, text = "AI Player", font = ("Arial", 16))\
            .grid(row = 0, column = 0)

        ##Radio frame
        radio_frame = tk.Frame(player_frame)
        radio_frame.grid(row = 1, column = 0, padx = 5, pady = 5)

        radio_output = tk.IntVar(radio_frame, value = 1) ##default to first player
        radio_pone = tk.Radiobutton(radio_frame, text = 'Player One', variable = radio_output, value = 1)
        radio_ptwo = tk.Radiobutton(radio_frame, text = 'Player Two', variable = radio_output, value = 2)

        radio_pone.grid(row = 0, column = 0)
        radio_ptwo.grid(row = 1, column = 0)

        radio_pone.select() ##default to first player

        ##Strength frame
        strength_frame = tk.Frame(root)
        strength_frame.grid(row = 1, column = 0, padx = 5, pady = 5)

        tk.Label(strength_frame, text = "AI Strength", font = ("Arial, 16"))\
            .grid(row = 0, column = 0)
        strength_output = tk.IntVar(strength_frame, value = 4) ##default to search depth of 4-ply
        strength_scale = tk.Scale(strength_frame, variable = strength_output, from_ = 4, to = 20, orient = tk.HORIZONTAL, tickinterval = 16)
        strength_scale.grid(row = 1, column = 0)

        ##Submit frame
        submit_frame = tk.Frame(root)
        submit_frame.grid(row = 2, column = 0, padx = 5, pady = 5)

        submit_button = tk.Button(submit_frame, text = 'Submit', command = tk_output)
        submit_button.grid(row = 0, column = 0)

        root.mainloop()

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
            button = Button(rect, default_surface, hovered_surface, col)
            button.update(self.window, self.base_theme)
            self.active_buttons.append(button)

    def clear_turn_buttons(self):
        """Clear all turn buttons from the window
        """
        for button in self.active_buttons:
            if button.code in range(7):
                button.clear(self.window, self.base_theme)
        self.active_buttons = [b for b in self.active_buttons if b.code not in range(7)]

    def play_move(self, col : int, board : Board, game_surface : pygame.Surface, in_game : bool = True):
        """Plays a move in the board and then game surface
        Game window will need to be updated afterwards
        Used in isolation to create images during loading of a file

        Args:
            col (int): Column to play in
            board (Board): Current board instance
            in_game (bool): Defaults to true, game surface should be blitted to main window
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
        if in_game:
            ##Blit game surface to window
            self.window.blit(game_surface, (125,50))
            pygame.display.flip()

    def terminal_check(self, board : Board, game_surface : pygame.Surface):
        """Check if the game is finished

        Args:
            board (Board): Current board instance
            game_surface (pygame.Surface): Board surface

        Returns:
            'home' if game finished, None otherwise
        """
        state = board.game_over()
        if state == Status.game_won:
            self.end_game_output(game_surface, 'Game Won', board)
            return 'home'
        elif state == Status.game_drawn:
            self.end_game_output(game_surface, 'Game Drawn', board)
            return 'home'
        else:
            ##Terminate game loop
            self.turn_setup(board)
            return None


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

    def update_active_buttons(self):
        """Update all active buttons in the window
        """
        for button in self.active_buttons:
            button.update(self.window, self.base_theme)

    def set_players(self, player_one : Player_Type, player_two : Player_Type):
        """Sets the players for a game

        Args:
            player_one (Player_Type): Code for player one
            player_two (Player_Type): Code for player twoe
        """
        self.players = [player_one, player_two]

    def set_ai_strength(self, strength : int):
        """Sets ai strength (search depth)

        Args:
            strength (int)
        """
        self.ai_strength = strength




