from board import Board
from auxiliary import Status, Save_Type, get_confirmation, Main_Menu_Choice, Load_Menu_Choice, Player_Type
from storage import save, load, select_file, traverse_game
from interface import Interface
from ai import Minimax

class Main:

    def __init__(self):
        self.board = Board()

    def turn(self):
        """Play through a turn in the game
        """
        ##Output current board state to users
        Interface.output_board(self.board)

        if self.board.get_counter() > 0:
            #Check if user wants to save position
            valid = False
            while not valid:
                try:
                    choice = input("Do you want to save this position? (Y/N): ").upper()
                    if choice not in {'Y','N'}:
                        print("Invalid input")
                    else:
                        valid = True
                        if choice == 'Y':
                            ##Get confirmation of decision to save
                            confirmed = get_confirmation()
                            if confirmed:
                                save(Save_Type.position, self.board, "Connect4.db")
                                print("Position saved\n")
                            else:
                                print("Position not saved, continue game\n")
                except:
                    print("Invalid input")

        if self.players[self.board.get_counter()%2] == Player_Type.human:
            column = self.input() ##Accept move input from human player
        elif self.players[self.board.get_counter()%2] == Player_Type.ai:
            ##Currently working at a fixed depth of 6
            ai = Minimax(self.board.get_move_history(), 6)
            column = ai.search()

        self.board.make_move(column) ##Play move in the board

        current_state = self.board.game_over() ##Determine current board state
        if current_state == Status.game_won: ##Last move won the game
            print("Game won")
            Interface.output_board(self.board)
            print("\n\n")

            ##Check if user wants to save the game
            valid = False
            while not valid:
                try:
                    choice = input("Do you want to save this game? (Y/N): ").upper()
                    if choice not in {'Y', 'N'}:
                        print("Invalid input")
                    else:
                        valid = True
                        if choice == 'Y':
                            confirmed = get_confirmation()
                            if confirmed:
                                save(Save_Type.game, self.board, "Connect4.db")
                                print("Game saved\n")
                            else:
                                print("Game not saved")
                except:
                    print("Invalid input")

            self.reset() ##Restart game
            self.main()

        elif current_state == Status.game_drawn: ##Last move drew the game
            print("Game drawn")
            Interface.output_board(self.board)
            print("\n\n")
            self.reset() ##Restart game
            self.main()

    def input(self) -> int:
        """Temporary input function for text-based prototype

        Returns:
            int: Chosen column
        """
        valid_moves = self.board.retrieve_valid_moves() ##Identify the valid moves in the position
        valid_move = False
        while not valid_move:
            try: ##Validate the type of the input
                choice = int(input("Enter column: ")) - 1
            except:
                print("Enter an integer\n")
                continue
            if choice not in valid_moves: ##Ensure move is a valid move in the current board state
                print("Invalid choice\n")
                continue
            valid_move = True
        return choice

    def reset(self):
        """Reset method for main
        """
        self.board.reset()
        self.players = None

    def main(self):
        """Main function controlling the usage of components of the application
        """
        print("\n\nConnect 4 Application\n\n")
        choice = self.main_menu()
        if choice == Main_Menu_Choice.play:
            ##Both player 1 and player 2 are human
            self.players = [Player_Type.human,Player_Type.human]
            self.play()

        elif choice == Main_Menu_Choice.ai:
            self.ai_menu()
            self.play()


        elif choice == Main_Menu_Choice.load:
            filetype = self.load_menu()
            ##Determine the position to playout
            if filetype == Load_Menu_Choice.position:
                positions = load(Save_Type.position, "Connect4.db")
                position = select_file(positions)
                print(position)
            elif filetype == Load_Menu_Choice.game:
                games = load(Save_Type.game, "Connect4.db")
                game = select_file(games)
                position = traverse_game(game)
            ##Playout position in-game
            self.playout(position)

    def play(self):
        """Loop through turns
        """
        print("In play")
        while True:
            self.turn()

    def playout(self, position):
        """Create a board instance and playout from position

        Args:
            position (list): Move history representing position
        """
        ##Load position into board
        for move in position:
            self.board.make_move(move)
        self.ai_menu()
        self.play()

    def main_menu(self) -> int:
        """Runs the main menu

        Returns:
            int: Code representing choice
        """
        valid = False
        while not valid:
            choice = input("1 - Play a game\n2 - Play the AI\n3 - Load a file\n:")
            if choice == '1':
                return Main_Menu_Choice.play
            elif choice == '2':
                return Main_Menu_Choice.ai
            elif choice == '3':
                return Main_Menu_Choice.load
            else:
                print("Invalid entry, try again")

    def load_menu(self) -> int:
        """Runs the load menu

        Returns:
            int: Code representing choice
        """
        valid = False
        while not valid:
            choice = input("1 - Load a position\n2 - Load a game\n:")
            if choice == '1':
                return Load_Menu_Choice.position
            elif choice == '2':
                return Load_Menu_Choice.game
            else:
                print("Invalid entry, try again")

    def ai_menu(self) :
        """Runs the ai menu, assigning player one and player two
        """
        while True:
            choice = input("Who plays first?\n1 - You\n2 - AI\n:")
            if choice == '1':
                self.players = [Player_Type.human,Player_Type.ai]
                break
            elif choice == '2':
                self.players = [Player_Type.ai,Player_Type.human]
                break
            else:
                print("Invalid entry, try again")




