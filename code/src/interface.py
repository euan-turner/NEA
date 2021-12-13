from prettytable import PrettyTable
from board import Board

class Interface:

    def output_board(board : Board):

        board_output = board.output()
        table = PrettyTable()
        table.header = False
        table.hrules = True
        for row in board_output:
            table.add_row(row)
        print(table)
