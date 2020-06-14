import unittest
from typing import List

# import our scripts
from minimax import find_best_move
from tictactoe import TTTPiece, TTTBoard
from board import Move


class TTTMinimaxTestCase(unittest.TestCase):
    # all test methods must begin with "test_"
    def test_easy_position(self):
        # win in 1 move
        to_win_easy_position: List[TTTPiece] = [
            TTTPiece.X,
            TTTPiece.O,
            TTTPiece.X,
            TTTPiece.X,
            TTTPiece.E,
            TTTPiece.O,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.O,
        ]
        # pass in the current positions and turn to the TTTBoard
        test_board1: TTTBoard = TTTBoard(to_win_easy_position, TTTPiece.X)
        # use find_best_move function to find the best move
        answer1: Move = find_best_move(test_board1)
        # the winning move should be Sq 6, the bottom left sq
        self.assertEqual(answer1, 6)

    def test_block_position(self):
        # must block O's to win
        to_block_position: List[TTTPiece] = [
            TTTPiece.X,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.O,
            TTTPiece.E,
            TTTPiece.X,
            TTTPiece.O,
        ]
        test_board2: TTTBoard = TTTBoard(to_block_position, TTTPiece.X)
        answer2: Move = find_best_move(test_board2)
        # the best move is to block at Sq 2, the top right sq
        self.assertEqual(answer2, 2)

    def test_hard_position(self):
        # find the best move to win 2 moves
        to_win_hard_position: List[TTTPiece] = [
            TTTPiece.X,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.E,
            TTTPiece.O,
            TTTPiece.O,
            TTTPiece.X,
            TTTPiece.E,
        ]
        test_board3: TTTBoard = TTTBoard(to_win_hard_position, TTTPiece.X)
        answer3: Move = find_best_move(test_board3)
        self.assertEqual(answer3, 1)


if __name__ == "__main__":
    unittest.main()
