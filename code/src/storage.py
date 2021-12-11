import sqlite3
from auxiliary import Save_Type
from board import Board
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
    moves = convert(moves) ##Convert into string representation for storage
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

def convert(moves: list) -> str:
    """Converts the board's representation of the the move history into a string

    Args:
        moves (list): Integer list of moves played

    Returns:
        str: Sequence of digits representing moves
    """
    return ''.join([str(i) for i in moves])

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


        while True: ##Validate and accept confirmation
            print(f"Confirm selection: {selection}")
            confirmation = input("(Y/N): ")
            if confirmation.upper() not in {'Y', 'N'}:
                print("Invalid entry")
                continue
            elif confirmation.upper() == 'Y':
                confirmed = True
            break

    return selection


