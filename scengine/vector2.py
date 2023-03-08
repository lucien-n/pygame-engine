from typing import TypeVar
import math

TVector2 = TypeVar("TVector2", bound="Vector2")


class Vector2(object):
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def set(self, *args) -> tuple[int | float, int | float]:
        """Sets self

        Args:
            vector (Vector2): Vector2 object
            OR
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int | float, int | float]: tuple of x and y
        """
        if len(args) <= 1:
            self.x = args[0].x
            self.y = args[0].y
        else:
            self.x = args[0]
            self.y = args[1]

        return (self.x, self.y)

    def add(self, *args) -> tuple[int | float, int | float]:
        """Adds the value of a vector to self

        Args:
            vector (Vector2): Vector2 object
            OR
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int | float, int | float]: tuple of x and y
        """
        if len(args) <= 1:
            self.x += args[0].x
            self.y += args[0].y
        else:
            self.x += args[0]
            self.y += args[1]

        return (self.x, self.y)

    def substract(self, *args) -> tuple[int | float, int | float]:
        """Substracts the value of a vector from self

        Args:
            vector (Vector2): Vector2 object
            OR
            x (int | float): x value
            y (int | float): y value

        Returns:
            tuple[int | float, int | float]: tuple of x and y
        """
        if len(args) <= 1:
            self.x -= args[0].x
            self.y -= args[0].y
        else:
            self.x -= args[0]
            self.y -= args[1]

        return (self.x, self.y)

    def multiply(self, multiplier) -> TVector2:
        """Multiplies the value of a vector from self

        Args:
            multiplier (int)

        Returns:
            Vector2: self
        """
        self.x *= multiplier
        self.y *= multiplier

        return Vector2(self.x, self.y)

    def divide(self, divider: int) -> TVector2:
        """Divides the value of a vector from self

        Args:
            divider (int)

        Returns:
            Vector2: self
        """
        self.x /= divider
        self.y /= divider

        return Vector2(self.x, self.y)

    def round(self, to: int) -> TVector2:
        """Returns rounded vector

        Args:
            to (int): round to number of digits

        Returns:
            Vector2: self
        """

        return Vector2(round(self.x, to), round(self.y, to))

    def floor(self, divide: int | float = 0, multiply: int | float = 0) -> TVector2:
        """Returns floored tuple of vector

        Args:
            divide (int | float): divide values by
            multiply (int | float): multiply values by

        Returns:
            Vector2: self
        """

        if divide:
            return Vector2(math.floor(self.x / divide), math.floor(self.y / divide))
        elif multiply:
            return Vector2(math.floor(self.x * multiply), math.floor(self.y * multiply))
        else:
            return Vector2(math.floor(self.x), math.floor(self.y))

    def copy(self) -> TVector2:
        """Create a new Vector2 with the values of self

        Returns:
            TVector2: Copy of self
        """
        return Vector2(self.x, self.y)

    def totuple(self) -> tuple[int | float, int | float]:
        return (self.x, self.y)

    def __add__(self, other: TVector2 | tuple[int | float, int]) -> TVector2:
        if type(other) == tuple:
            return (self.x + other[0], self.y + other[1])
        elif type(other) == Vector2:
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other: TVector2 | tuple[int | float, int]) -> TVector2:
        if type(other) == tuple:
            return (self.x - other[0], self.y - other[1])
        elif type(other) == Vector2:
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __mul__(
        self, other: TVector2 | tuple[int | float, int] | int | float
    ) -> TVector2:
        if type(other) == tuple:
            return (self.x * other[0], self.y * other[1])
        elif type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(
        self, other: TVector2 | tuple[int | float, int] | int | float
    ) -> TVector2:
        if type(other) == tuple:
            return (self.x / other[0], self.y / other[1])
        elif type(other) == tuple:
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __call__(self) -> tuple[int, int]:
        return tuple(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y
