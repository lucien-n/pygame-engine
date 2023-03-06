from typing import TypeVar

TVector2 = TypeVar("TVector2", bound="Vector2")


class Vector2(object):
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def set(self, x: int | float, y: int | float) -> tuple[int, int]:
        """Set x & y

        Args:
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int, int]: tuple of x and y
        """
        self.x, self.y = x, y
        return (self.x, self.y)

    def add(self, *args) -> tuple[int, int]:
        """Adds the value of a vector to self

        Args:
            vector (Vector2): Vector2 object
            OR
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int, int]: tuple of x and y
        """
        if len(args) <= 1:
            self.x += args[0].x
            self.y += args[0].y
        else:
            self.x += args[0]
            self.y += args[1]

        return (self.x, self.y)

    def substract(self, *args) -> tuple[int, int]:
        """Substracts the value of a vector from self

        Args:
            vector (Vector2): Vector2 object
            OR
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int, int]: tuple of x and y
        """
        if len(args) <= 1:
            self.x -= args[0].x
            self.y -= args[0].y
        else:
            self.x -= args[0]
            self.y -= args[1]

        return (self.x, self.y)

    def __add__(
        self, other: TVector2 | tuple[int | float, int]
    ) -> tuple[int | float, int]:
        if type(other) == tuple:
            return (self.x + other[0], self.y + other[1])
        return (self.x + other.x, self.y + other.y)

    def __sub__(
        self, other: TVector2 | tuple[int | float, int]
    ) -> tuple[int | float, int]:
        if type(other) == tuple:
            return (self.x - other[0], self.y - other[1])
        return (self.x - other.x, self.y - other.y)

    def __mul__(
        self, other: TVector2 | tuple[int | float, int]
    ) -> tuple[int | float, int]:
        if type(other) == tuple:
            return (self.x * other[0], self.y * other[1])
        return (self.x * other.x, self.y * other.y)

    def __truediv__(
        self, other: TVector2 | tuple[int | float, int]
    ) -> tuple[int | float, int]:
        if type(other) == tuple:
            return (self.x / other[0], self.y / other[1])
        return (self.x / other.x, self.y / other.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __call__(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y
