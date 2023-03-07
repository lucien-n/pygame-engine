import pygame.sprite
import pygame.surface


class Tile:
    def __init__(
        self, chunk_x: int, chunk_y: int, sprite: pygame.surface.Surface
    ) -> None:
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.image = sprite

    def update(self):
        pass

    def draw(self):
        pass
