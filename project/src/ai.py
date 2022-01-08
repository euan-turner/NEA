from math import inf
from board import Board
from auxiliary import Status, LSB1

class Minimax:

    def __init__(self, position : list, max_depth : int):
        self.board = Board()
        self.max_search_depth = max_depth
        self.initialise_position(position)

        ##Index of ai's bitboard in board._bitboards
        self.ai_board_index = self.board.get_counter() & 1


    def initialise_position(self, position : list):
        """Loads the board instance with starting position for search

        Args:
            position (list): Moves representing position
        """
        for move in position:
            self.board.make_move(move)


    def search(self) -> int:
        """Calls minimax with initial conditions

        Returns:
            int: Best move in initial position
        """
        best_move = -1 ##Will be changed
        best_eval = - inf ##lowest possible evaluation

        valid_moves = self.board.retrieve_valid_moves()
        ordered_moves = self.naive_move_sort(valid_moves)
        for move in ordered_moves:
            ##Generate and search game tree
            self.board.make_move(move)
            move_eval = self.minimax(0, -inf, inf, False)
            self.board.undo_move()

            ##Update best move and evaluation
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        return best_move

    def minimax(self, depth : int, alpha : int, beta : int, is_max : bool):
        """Minimax search of game tree

        Args:
            depth (int): Current search depth
            alpha (int): Pruning upper bound
            beta (int): Pruning lower bound
            is_max (bool): Maximiser or minimiser turn

        Returns:
            int: Best evaluated move in position
        """
        ##Check for a terminal board position
        status = self.board.game_over()
        if status == Status.game_drawn:
            ##Drawn position, so neutral evaluation
            return 0
        elif status == Status.game_won:
            ##Use depth as an offset on evaluation
            ##So long losses or quick wins will be prioritised
            if is_max:
                ##Minimiser just won, so very negative evaluation
                return -10000 + depth
            else:
                return 10000 - depth
        elif depth == self.max_search_depth:
            return self.evaluate()
        else:
            valid_moves = self.board.retrieve_valid_moves()
            ordered_moves = self.naive_move_sort(valid_moves)

            ##Maximising player - AI
            if is_max:
                best_eval = -inf
                ##Search all available moves
                for move in ordered_moves:
                    self.board.make_move(move)
                    best_eval = max(best_eval, self.minimax(depth+1, alpha, beta, False))
                    self.board.undo_move()

                    ##Prune search tree
                    if best_eval >= beta:
                        break
                    alpha = max(best_eval, alpha)
            ##Minimising player - human
            else:
                best_eval = inf
                ##Search all available moves
                for move in ordered_moves:
                    self.board.make_move(move)
                    best_eval = min(best_eval, self.minimax(depth+1, alpha, beta, True))
                    self.board.undo_move()

                    ##Prune search tree
                    if best_eval <= alpha:
                        break
                    beta = min(beta, best_eval)
            return best_eval

    def evaluate(self):
        """Calls evaluation functions

        Returns:
            int: Evaluation of position
        """
        if self.board.get_counter() > 10:
            return self.feature_evaluation()
        else:
            return self.static_evaluation()

    def static_evaluation(self) -> int:
        """Calculates static evaluation of position
        Positive is good for ai

        Returns:
            int: Static evaluation of position
        """
        ##Fixed evaluation for position
        eval_board = [
            3,4,5,5,4,3,0,
            4,6,8,8,6,4,0,
            5,8,11,11,8,5,0,
            7,10,13,13,10,7,0,
            5,8,11,11,8,5,0,
            4,6,8,8,6,4,0,
            3,4,5,5,4,3,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0
        ]
        score = 0
        for i in range(64):
            ##Move played by AI
            if (self.board.get_bitboard(self.ai_board_index) & (LSB1 << i)) != 0:
                score += eval_board[i]
            ##Move played by opponent
            elif (self.board.get_bitboard(1 - self.ai_board_index) & (LSB1 << i) != 0):
                score -= eval_board[i]
        return score

    def feature_evaluation(self) -> int:
        """Calculates feature-based evaluation of a position
        Positive is good for AI
        Currently naive to availability at ends of runs

        Features:          Scores:
        3 connected pieces 8000
        2 connected pieces 1000


        Returns:
            int: [description]
        """
        ##Will use a similar method to checking for a win (four in a row),
        ##but looking for shorter runs

        ##Identify bitboards
        ai_board = self.board.get_bitboard(self.ai_board_index)
        opp_board = self.board.get_bitboard(1 - self.ai_board_index)

        directions = [1,7,6,8] ##4 shift directions to check
        score = 0

        for d in directions:
            ai2 = ai_board & (ai_board >> d) ##run of 2
            ai3 = ai2 & (ai_board >> 2*d) ##run of 3
            opp2 = opp_board & (opp_board >> d)
            opp3 = opp2 & (opp_board >> 2*d)

            ##Count runs of 2
            ai_twos = self.count_one_bits(ai2)
            opp_twos = self.count_one_bits(opp2)

            ##Count runs of 3
            ai_threes = self.count_one_bits(ai3)
            opp_threes = self.count_one_bits(opp3)

            score += 8000*ai_threes - 8000*opp_threes \
                + 1000*ai_twos - 1000*opp_twos
        return score

    def count_one_bits(self, n : int) -> int:
        """Counts the number of positive bits in a binary integer

        Args:
            n (int): Integer to count bits in

        Returns:
            int: Number of positive bits
        """
        count = 0
        while n != 0:
            ##Check least significant bit
            if (n&1) == 1:
                count += 1
            n = n >> 1 ##Shift bits right
        return count

    def naive_move_sort(self, moves : list) -> list:
        """Sorts moves based on distance from centre

        Args:
            moves (list): Moves to sort

        Returns:
            list: Sorted moves
        """
        ##Uses lambda function calculating distance from centre column as key
        return sorted(moves, key = lambda x : abs(x-3))




