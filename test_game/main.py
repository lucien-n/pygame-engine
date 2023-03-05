from scengine import *
import pygame as pg
from pathlib import Path

from test_game.player import Player

path = Path(__file__).parent


class Game(engine.Engine):
    def __init__(
        self,
        title: str = "SCEngine - Game",
        size: tuple[int] = (1280, 720),
        background_color: pg.Color = (10, 10, 10, 255),
        resource_folder: str = path / "resources",
    ) -> None:
        super().__init__(title, size, background_color, resource_folder)

        self.CAMERA = camera.Camera(self.DISPLAY)

        self.PLAYER = Player(self)
        self.CAMERA.follow(self.PLAYER)

    def event_handler(self) -> None:
        """Main event_handler method"""
        events = super().event_handler()

        self.PLAYER.event_handler(events)

    def update(self) -> None:
        """Main update method"""
        super().update()

        self.PLAYER.update()

    def draw(self):
        """Main draw method"""
        super().draw()

        self.PLAYER.draw()

        self.WINDOW.blit(self.DISPLAY, (0, 0))
        pg.display.flip()
        self.CLOCK.tick()
