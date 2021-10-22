from board import Board
from auxiliary import Status
from prettytable import PrettyTable

class Main:

    def __init__(self):
        self.board = Board()

    def turn(self):
        """Play through a turn in the game
        """        
        self.output() ##Output current board state to users
        column = self.input() ##Accept move input from next player

        self.board.make_move(column) ##Play move in the board

        current_state = self.board.game_over() ##Determine current board state
        if current_state == Status.game_won: ##Last move won the game
            print("Game won")
            self.output()
            print("\n\n")
            self.board.reset() ##Restart game
        elif current_state == Status.game_drawn: ##Last move drew the game
            print("Game drawn")
            self.output()
            print("\n\n")
            self.board.reset() ##Restart game

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

    def output(self):
        """Temporary output function for text-based prototype
        """
        board_output = self.board.output()
        table = PrettyTable()
        table.header = False
        table.hrules = True
        for row in board_output:
            table.add_row(row)
        print(table)

    def main(self):
        while True:
            self.turn()


main = Main()
main.main()

