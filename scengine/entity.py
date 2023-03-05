import pygame as pg
from .vector2 import Vector2
from .colors import Colors


class Entity(pg.sprite.Sprite):
    def __init__(
        self,
        engine,
        x: int | float = 50,
        y: int | float = 50,
    ) -> None:
        self.ENGINE = engine
        self.position = Vector2(x, y)

        self.sprite = pg.surface.Surface((16, 16))
        self.sprite.fill(Colors.white)

        self.rect = self.sprite.get_rect()
        self.rect.x, self.rect.y = self.position

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.ENGINE.WINDOW.blit(
            self.sprite, self.position.subsract(self.ENGINE.CAMERA.scroll)
        )
