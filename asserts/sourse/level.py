from typing import Union, List


class Vector2:
    __slots__ = ("x", "y")
    x: Union[float, int]
    y: Union[float, int]

    def __init__(self, x: Union[float, int], y: Union[float, int]):
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def __setattr__(self, key, value):
        raise AttributeError

    def size(self) -> float:
        return sum((self.x**2, self.y**2))**0.5

    def __mul__(self, other: Union["Vector2", float, int]):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __add__(self, other: Union["Vector2", float, int]):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other: Union["Vector2", float, int]):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x - other, self.y - other)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def normalized(self) -> "Vector2":
        return self / self.size()


class Filed:

    def __init__(self, pos: Vector2, board: "Board"):
        self.board = board
        self.pos = pos


class Board:
    def __init__(self, pos: Vector2):
        self.board: List[List] = [[None for _ in range(pos.x)] for _ in range(pos.y)]

    def put(self, pos: Vector2, filed: Filed):
        self.board[pos.x][pos.y] = filed
