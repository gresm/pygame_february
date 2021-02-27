from typing import List
from vector2 import Vector2


class Filed:

    def __init__(self, pos: Vector2, board: "Board"):
        self.board = board
        self.pos = pos


class Board:
    def __init__(self, pos: Vector2):
        self.board: List[List] = [[None for _ in range(pos.x)] for _ in range(pos.y)]

    def put(self, pos: Vector2, filed: Filed):
        self.board[pos.x][pos.y] = filed
