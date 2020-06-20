from minimax import find_best_move
from tictactoe import TTTBoard
from board import Move, Board

board: Board = TTTBoard()

# a functin that asks the user to input a move
def get_player_move() -> Move:
    # initialise Move to a negative number
    player_move: Move = Move(-1)
    # as for a move. condition will be satisfied as Move(-1)
    # is not a legal move
    while player_move not in board.legal_moves:
        play: int = int(input("Enter a legal square (0-8): "))
        player_move = Move(play)
    return player_move


if __name__ == "__main__":
    # main game loop
    while True:
        # human player plays first
        human_move: Move = get_player_move()
        # create a board using the move
        board = board.move(human_move)
        if board.is_win:
            print("Human wins!")
            break
        elif board.is_draw:
            print("Draw!")
            break
        # run the find_best_move function
        computer_move: Move = find_best_move(board)
        print(f"Computer move is {computer_move}")
        board = board.move(computer_move)
        print(board)
        if board.is_win:
            print("Computer wins!")
        elif board.is_draw:
            print("Draw!")
            break
