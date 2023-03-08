import pygame.sprite
import pygame.surface
from scengine.vector2 import Vector2


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        chunk_coords: Vector2,
        sprite: pygame.surface.Surface,
    ) -> None:
        super().__init__()

        self.chunk_coords = chunk_coords

        self.image = sprite
        self.rect = self.image.get_rect()
