import sqlite3
from auxiliary import Save_Type
from board import Board
from main import Main
from auxiliary import get_confirmation
from prettytable import PrettyTable

def save(file_type : Save_Type, board : Board, database : str):
    """Saves a position or game to the database
    Functionality will be altered when account system is added

    Args:
        file_type (Save_Type): Position or game
        board (Board): Current instance of board
        database (string): Database to use
    """
    moves = board.get_move_history() ##Extract game or position representation
    moves = convert_history(moves) ##Convert into string representation for storage
    sql_command = f"""
    INSERT INTO store (filetype, data) VALUES ({file_type}, '{moves}')
    """
    execute_sql(sql_command, database)

def load(file_type : Save_Type, database : str) -> list:
    """Loads a position or game from the database
    Functionality will be altered when the account system is added

    Args:
        file_type (Save_Type): Position or game
        database (str): Database to use

    Returns:
        list: All retrieved positions or games
    """
    sql_command = f"""
    SELECT data FROM store WHERE filetype = {file_type}
    """
    result = execute_sql(sql_command, database)
    return [file[0] for file in result]

def convert_history(moves: list) -> str:
    """Converts the board's representation of the the move history into a string

    Args:
        moves (list): Integer list of moves played

    Returns:
        str: Sequence of digits representing moves
    """
    return ''.join([str(i) for i in moves])

def revert_history(file : str) -> list:
    """Reverts a string into a list representing the move history

    Args:
        file (str): The string history

    Returns:
        list: List of integers representing history
    """
    return [int(i) for i in file]

def execute_sql(command : str, database : str) -> sqlite3.Cursor:
    """Executes an sql command using sqlite3

    Args:
        command (string): sqlite3 command
        database (string): database to use

    Returns:
        sqlite3.Cursor : Results of sql command
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    output = cursor.execute(command)
    conn.commit()
    return output

def select_file(files : list):
    """Allows the user to select a file from the database to
    load into the application

    Args:
        files (list): All files of type in the database
        extra argument to specify user will be added with account system
    Returns:
        [type]: [description]
    """
    table = PrettyTable()
    table.field_names = ["#", "File"]
    table.add_column("#", [i+1 for i in range(len(files))])
    table.add_column("File", files)
    print(table)

    confirmed = False
    while not confirmed: ##Validate and accept input
        try:
            choice = int(input("Enter file number: "))
        except:
            print("Enter an integer")
            continue

        if choice <= 0:
            print("File index not found, try again")
            continue

        try:
            selection = files[choice-1]
        except:
            print("File index not found, try again")
            continue


        confirmed = get_confirmation()

    return revert_history(selection)


def traverse_game(move_history : list) -> list:
    """Allows the user to select a position from a game to use

    Args:
        move_history (list): Entire move history of a game

    Returns:
        list: Move history up to the position selected
    """
    traverse_board = Main() ##Need main instance for output function
    selected = False
    while not selected:
        current_counter = traverse_board.board.get_counter()
        if current_counter == 0: ##On initial position
            message = "Options: N - next" ##Cannot select or go back
            allowed = {'N'}
        elif current_counter == len(move_history): ##On terminal position
            message = "Options: B - back"
            allowed = {'B'}
        else: ##On in-game position
            message = "Options: B - back, N - next, S - select"
            allowed = {"B", "N", "S"}



        traverse_board.output()
        valid = False
        while not valid:
            try:
                choice = input("\n" + message + "\n:").upper()
            except:
                print("Invalid entry, use given keys")

            if choice not in allowed:
                print("Invalid entry, use given keys")
                continue
            else:
                valid = True
                if choice == "N":
                    traverse_board.board.make_move(move_history[current_counter])
                elif choice == "B":
                    traverse_board.board.undo_move()
                elif choice == "S":
                    confirmed = get_confirmation()
                    if confirmed:
                        return traverse_board.board.get_move_history()
                    else:
                        print("Returning to game navigation\n")


