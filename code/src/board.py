from auxiliary import Bitboard, LSB1, Status

class Board:

    def __init__(self):
        self._bitboards = Bitboard([0,0]) ##2 64-bit integers as the bitboards
        self._heights = [0,7,14,21,28,35,42] ##Positions of bottom row in the bitboards
        self._counter = 0
        self._move_history = []

    def reset(self):
        """Resets attributes - primarily for use in testing
        """
        self.__init__()

    def get_counter(self) -> int:
        """Get method for _counter

        Returns:
            int: Current number of moves played
        """
        return self._counter

    def get_move_history(self) -> list:
        """Get method for _move_history

        Returns:
            list: Current move history
        """
        return self._move_history

    def get_bitboard(self, index : int) -> Bitboard:
        """Get method for a bitboard

        Args:
            index (int): The bitboard to return

        Returns:
            Bitboard: The desired bitboard
        """
        return self._bitboards[index]

    def make_move(self, column : int):
        """Plays a move in the next player's bitboard

        Args:
            column (int): The column of the move
        """
        self._move_history.append(column) ##Add new move to move history
        move = self._get_move(column) ##Get bitboard representing move

        board_index = self._counter & 1 ##Determine current player
        self._bitboards[board_index] ^= move ##Play move in bitboard

        self._heights[column] += 1 ##Increment height of used column
        self._counter += 1 ##Increment counter

    def undo_move(self):
        """Removes the last move played
        """
        self._counter -= 1 ##Decrement counter to point to last move
        column = self._move_history[self._counter]
        self._heights[column] -= 1 ##Decrement height in column to point to last move

        move = self._get_move(column) ##Get bitboard representing last move
        board_index = self._counter & 1 ##Determine last player's bitboard

        self._bitboards[board_index] ^= move ##Remove move from bitboard
        self._move_history.pop() ##Remove move from move history

    def check_win(self) -> bool:
        """Checks whether the last move created a four in a row

        Returns:
            bool: Game won or not
        """
        last_move = self._counter - 1 ##Identify last move played
        board_index = last_move & 1 ##Identify last bitboard
        b0 = self._bitboards[board_index]
        directions =  [1,7,6,8] ##The 4 shift directions to check
        for d in directions:
            b1 = b0 & (b0 >> d) ##Bitboards needed to check for win condition
            b2 = b1 >> (2*d)
            if (b1 & b2) != 0: ##Win condition satisfied
                return True
        return False

    def game_over(self) -> int:
        """Return status code representing game state

        Returns:
            int: Status code
        """
        if self.check_win() == True:
            return Status.game_won
        elif self._counter == 42:
            return Status.game_drawn
        else:
            return Status.game_unfinished

    def retrieve_valid_moves(self) -> list:
        """Retrieve all valid moves in a position

        Returns:
            list: All valid moves
        """
        valid = []
        for col in range(len(self._heights)):
            if self._heights[col] < 6 + 7*col: ##If column is not full
                valid.append(col)
        return valid

    def _get_move(self, column : int) -> Bitboard:
        """Returns a bitboard representing the move currently being made

        Returns:
            Bitboard: Bitboard with applied move
        """
        bit_position = self._heights[column] ##Determine index in bitboard
        move = Bitboard(LSB1 << bit_position) ##Shift 1 bit to correct position
        return move

    def output(self) -> list:
        """Convert the bitboards into a more understandable representation of the board

        Returns:
            list: Board representation
        """
        board_arr = []
        for i in range(64):
            bit = LSB1 << i ##Shift to examine each bit individually
            if (self._bitboards[0] & bit) != 0: ##Played by first player
                board_arr.append('X')
            elif (self._bitboards[1] & bit) != 0: ##Played by second player
                board_arr.append('O')
            else: ##Played by no player
                board_arr.append('-')

        output_arr = []
        for r in range(5, -1, -1): ##Organise values into structured array
            row = []
            for c in range(7):
                row.append(board_arr[r + (c*7)])
            output_arr.append(row)
        return output_arr
