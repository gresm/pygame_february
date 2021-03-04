from typing import Union, List, Tuple

_OPERATOR_TYPE = Union[List[Union[int, float], Union[int, float]],
                       Tuple[Union[int, float], Union[int, float]], "Vector2", int, float]


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
        return sum((self.x ** 2, self.y ** 2)) ** 0.5

    def __mul__(self, other: _OPERATOR_TYPE):
        o = self.deserialize(other)
        return Vector2(self.x * o.x, self.y * o.y)

    def __truediv__(self, other: _OPERATOR_TYPE) -> "Vector2":
        o = self.deserialize(other)
        return Vector2(self.x / o.x, self.y / o.y)

    def __add__(self, other: _OPERATOR_TYPE):
        o = self.deserialize(other)
        return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, other: _OPERATOR_TYPE):
        o = self.deserialize(other)
        return Vector2(self.x - o.x, self.y - o.y)

    def __floordiv__(self, other: _OPERATOR_TYPE):
        o = self.deserialize(other)
        return Vector2(self.x // o.x, self.y // o.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def serialize(self):
        return self.x, self.y

    def floor(self) -> "Vector2":
        return Vector2(int(self.x), int(self.y))

    @classmethod
    def deserialize(cls, value: _OPERATOR_TYPE) -> "Vector2":
        if isinstance(value, (list, tuple)):
            return cls(value[0], value[1])
        elif isinstance(value, (int, float)):
            return cls(value, value)
        else:
            return value

    def normalized(self) -> "Vector2":
        return self / self.size()
