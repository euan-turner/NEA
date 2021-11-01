import sqlite3
from typing_extensions import ParamSpecArgs
from auxiliary import Save_Type
from board import Board

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

def load(file_type : Save_Type, database : str):
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
    return [file for file in result]

def convert(moves: list) -> str:
    """Converts the board's representation of the the move history into a string

    Args:
        moves (list): Integer list of moves played

    Returns:
        str: Sequence of digits representing moves
    """
    return ''.join([str(i) for i in moves])

def execute_sql(command, database):
    """Executes an sql command using sqlite3

    Args:
        command (string): sqlite3 command
        database (string): Database to use

    Returns:
        sqlite3.Cursor : Results of sql command
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    output = cursor.execute(command)
    conn.commit()
    conn.close()
    return output

