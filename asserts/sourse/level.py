class Vector:
    def __init__(self, x: int, y:int):
        self.y = y
        self.x = x


class Filed:

    def __init__(self, pos: Vector, board: "Board"):
        self.board = board
        self.pos = pos


class Board:
    def __init__(self, pos: Vector):
        self.board = [[None for _ in range(pos.x)] for _ in range(pos.y)]

    def put(self, pos: Vector, filed: Filed):
        self.board[pos.x][pos.y] = filed
