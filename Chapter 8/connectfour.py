from __future__ import annotations
from typing import List, Optional, Tuple
from enum import Enum

# from board.py
from board import Piece, Board, Move


class C4Piece(Piece, Enum):
    B = "B"
    R = "R"
    E = " "  # stand-in for empty

    @property
    def opposite(self) -> C4Piece:
        if self == C4Piece.B:
            return C4Piece.R
        elif self == C4Piece.R:
            return C4Piece.B
        else:
            return C4Piece.E

    def __str__(self) -> str:
        return self.value


# function that generates all the potential
# winning segments in a certain-size Connect Four grid
# You can attempt to draw to see where the numbers inside
# range() come from and how they are related to segment_length
# In Connect Four, segment length is 4
def generate_segments(
    num_columns: int, num_rows: int, segment_length: int
) -> List[List[Tuple[int, int]]]:
    segments: List[List[Tuple[int, int]]] = []

    # generate the vertical segments
    for c in range(num_columns):  # moving horizontal
        for r in range(num_rows - segment_length + 1):  # moving vertically
            segment: List[Tuple[List]] = []
            for t in range(segment_length):  # each segment
                segment.append((c, r + t))
            segments.append(segment)

    # generate the horizontal segments
    for c in range(num_columns - segment_length + 1):
        for r in range(num_rows):
            segment = []
            for t in range(segment_length):
                segment.append((c + t, r))
            segments.append(segment)

    # generate the bottom left to top right diagonal segments
    for c in range(num_rows - segment_length + 1):
        for r in range(num_columns - segment_length + 1):
            segment = []
            for t in range(segment_length):
                segment.append((c + t, r + t))
            segments.append(segment)

    # generate the top left to bottom right diagonal segments
    for c in range(num_columns - segment_length + 1):
        for r in range(segment_length - 1, num_rows):
            segment = []
            for t in range(segment_length):
                segment.append((c + t, r - t))
            segments.append(segment)
    return segments


class C4Board(Board):
    NUM_ROWS: int = 6
    NUM_COLUMNS: int = 7
    SEGMENT_LENGTH: int = 4

    # call the generate_segments function
    SEGEMENTS: List[List[Tuple[int, int]]] = generate_segments(
        NUM_COLUMNS, NUM_ROWS, SEGMENT_LENGTH
    )

    class Column:
        def __init__(self) -> None:
            self._container: List[C4Piece] = []

        @property
        def full(self) -> bool:
            return len(self._container) == C4Board.NUM_ROWS

        # adding a piece
        def push(self, item: C4Piece) -> None:
            if self.full:
                raise OverflowError("Trying to push piece to full column")
            self._container.append(item)

        # checking out a piece, allow accessing items like a list
        def __getitem__(self, index: int) -> C4Piece:
            # len(self._container) gets bigger as more C4Pieces are added
            if index > len(self._container) - 1:
                return C4Piece.E
            return self._container[index]

        def __repr__(self) -> str:
            return repr(self._container)

        def copy(self) -> C4Board.Column:
            temp: C4Board.Column = C4Board.Column()
            temp._container = self._container.copy()
            return temp

        # init for C4Board

    def __init__(
        self,
        position: Optional[List[C4Board.Column]] = None,
        turn: C4Piece = C4Piece.B,
    ) -> None:
        # Create NUM_COLUMNS of C4Board.Columns in a list to initialise
        if position is None:
            self.position: List[C4Board.Column] = [
                C4Board.Column() for _ in range(C4Board.NUM_COLUMNS)
            ]
        else:
            self.position = position
        self._turn: C4Piece = turn

    @property
    def turn(self) -> Piece:
        return self._turn

    def move(self, location: Move) -> Board:
        # copy the current C4Board
        temp_position: List[C4Board.Column] = self.position.copy()
        for c in range(C4Board.NUM_COLUMNS):
            temp_position[c] = self.position[c].copy()
        # "push" the new turn Piece to the selected location
        temp_position[location].push(self._turn)
        return C4Board(temp_position, self._turn.opposite)

    @property
    def legal_moves(self) -> List[Move]:
        # you can add to a column as long as it is not full
        return [
            Move(c) for c in range(C4Board.NUM_COLUMNS) if not self.position[c].full
        ]

    # Returns the count of black and red pieces in a segment
    def _count_segment(self, segment: List[Tuple[int, int]]) -> Tuple[int, int]:
        black_count: int = 0
        red_count: int = 0
        for column, row in segment:
            if self.position[column][row] == C4Piece.B:
                black_count += 1
            elif self.position[column][row] == C4Piece.R:
                red_count += 1
        return black_count, red_count

    @property
    def is_win(self) -> bool:
        for segment in C4Board.SEGEMENTS:
            black_count, red_count = self._count_segment(segment)
            if black_count == 4 or red_count == 4:
                return True
        return False

    # Like TTTBoard, C4Board can use the abstract base class Board’s
    # is_draw property without modification.

    def _evaluate_segment(self, segment: List[Tuple[int, int]], player: Piece) -> float:
        # use _count_segment defined above
        black_count, red_count = self._count_segment(segment)
        if red_count > 0 and black_count > 0:
            return 0  # mixed segments are neutral
        # max to determine winner
        count: int = max(red_count, black_count)
        score: float = 0
        if count == 2:
            score = 1
        elif count == 3:
            score = 100
        elif count == 4:
            score = 1000000
        color: C4Piece = C4Piece.B
        if red_count > black_count:
            color = C4Piece.R
        # if it is not the current player's turn return negative score
        if color != player:
            return -score
        return score

    def evaluate(self, player: Piece) -> float:
        total: float = 0
        # get total score from current player's perspective
        for segment in C4Board.SEGEMENTS:
            # calculate score using _evaluate_segment() defined above
            total += self._evaluate_segment(segment, player)
        return total

    def __repr__(self) -> str:
        display: str = ""
        for r in reversed(range(C4Board.NUM_ROWS)):
            display += "|"
            for c in range(C4Board.NUM_COLUMNS):
                display += f"{self.position[c][r]}" + "|"
            display += "\n"
        return display
