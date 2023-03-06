from scengine import *
from scengine.queue import Queue
import pygame as pg
from pathlib import Path

from test_game.player import Player
from test_game.hud import Hud

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
        self.SIZE = self.WIDTH, self.HEIGHT = (
            self.SETTINGS["video"]["size"]["width"],
            self.SETTINGS["video"]["size"]["height"],
        )
        pg.display.set_mode(self.SIZE, vsync=self.SETTINGS["video"]["vsync"])

        self.DISPLAY = pg.surface.Surface(
            (
                self.SETTINGS["video"]["resolution"]["width"],
                self.SETTINGS["video"]["resolution"]["height"],
            )
        )
        self.DRAWING_SURFACE = self.DISPLAY

        self.OVERLAY_DRAW_Q = Queue()

        self.CAMERA = camera.Camera(self)

        self.PLAYER = Player(self)
        self.CAMERA.follow(self.PLAYER)

        self.HUD = Hud(self)

        self.EVENT_HANDLER_Q.add(self.PLAYER)
        self.UPDATE_Q.add(self.HUD)

        self.UPDATE_Q.add(self.HUD)
        self.UPDATE_Q.add(self.PLAYER)
        self.UPDATE_Q.add(self.CAMERA)

        self.DRAW_Q.add(self.PLAYER)

        self.OVERLAY_DRAW_Q.add(self.HUD)

    def event_handler(self) -> None:
        """Main event_handler method"""
        super().event_handler()

    def update(self) -> None:
        """Main update method"""
        super().update()

    def draw(self):
        """Main draw method"""
        self.DRAWING_SURFACE.fill(self.BACKGROUND_COLOR)

        super().draw()
        self.WINDOW.blit(pg.transform.scale(self.DRAWING_SURFACE, self.SIZE), (0, 0))

        [overlay.draw() for overlay in self.OVERLAY_DRAW_Q]

        pg.display.update()
        self.CLOCK.tick(self.SETTINGS["video"]["framerate"])
