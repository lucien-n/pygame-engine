class Vector2(object):
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def add(self, vector) -> tuple[int, int]:
        """Adds the value of a vector to self

        Args:
            vector (Vector2): Vector2 object

        Returns:
            Vector2: self
        """
        self.x += vector.x
        self.y += vector.y
        return (self.x, self.y)

    def subsract(self, vector) -> tuple[int, int]:
        """Substracts the value of a vector from self

        Args:
            vector (Vector2): Vector2 object

        Returns:
            Vector2: self
        """
        self.x -= vector.x
        self.y -= vector.y
        return (self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y
