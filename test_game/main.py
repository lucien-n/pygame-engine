from scengine import *
from scengine.utils import log

import pygame as pg

from test_game.player import Player
from test_game.hud import Hud
from test_game.world.world_generator import WorldGenerator
from test_game.world.world import World

from multiprocessing import Process
from pathlib import Path
import time

path = Path(__file__).parent


class Game(engine.Engine):
    def __init__(
        self,
        title: str = "SCEngine - Game",
        size: tuple[int] = (1280, 720),
        background_color: pg.Color = (10, 10, 10, 255),
        resource_folder: str = path / "resources",
        tile_size: int = 16,
        chunk_size: int = 16,
        world_size: int = 4_192,
        world_generator: WorldGenerator = None,
        world_pipe=None,
        world_process: Process = None,
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

        self.CAMERA = camera.Camera(self)

        self.PLAYER = Player(self)
        self.CAMERA.follow(self.PLAYER)

        self.HUD = Hud(self)

        # World - Separate process
        self.WORLD_GENERATOR = world_generator
        self.WORLD_PIPE = world_pipe
        self.WORLD_PROCESS = world_process
        self.WORLD_DATA = None

        # World - Main process
        self.WORLD = World(self, tile_size, chunk_size, world_size)

        # Queues
        self.OVERLAY_DRAW_Q = queue.Queue()

        self.EVENT_HANDLER_Q.add(self.PLAYER)

        self.UPDATE_Q.add(self.PLAYER)
        self.UPDATE_Q.add(self.HUD)
        self.UPDATE_Q.add(self.CAMERA)

        self.DRAW_Q.add(self.WORLD)
        self.DRAW_Q.add(self.PLAYER)

        self.OVERLAY_DRAW_Q.add(self.HUD)

    def event_handler(self) -> None:
        """Main event_handler method"""
        super().event_handler()

    def update(self) -> None:
        """Main update method"""
        self.HUD.debug_lines.clear()
        super().update()

        self.WORLD_PIPE.send(self.generate_world_pipe_data())
        log("Main | Sent data to World")
        self.WORLD_DATA = self.WORLD_PIPE.recv()
        log("Main | Received data from World")

        self.WORLD.update()

    def draw(self):
        """Main draw method"""
        self.DRAWING_SURFACE.fill(self.BACKGROUND_COLOR)

        super().draw()

        self.WINDOW.blit(pg.transform.scale(self.DRAWING_SURFACE, self.SIZE), (0, 0))

        [overlay.draw() for overlay in self.OVERLAY_DRAW_Q]

        pg.display.update()
        self.CLOCK.tick(self.SETTINGS["video"]["framerate"])

    def run(self):
        log("Main | Starting game")
        super().run()
        if self.RUNNING:
            self.WORLD_GENERATOR.join()

    def generate_world_pipe_data(self) -> dict:
        """Generates data sent to the WORLD_PIPE

        Returns:
            dict: running and waiting to be generated chunks
        """
        data = {"running": self.RUNNING}

        if not self.WORLD.CHUNK_GENERATION_QUEUE.isEmpty():
            data["chunk"] = self.WORLD.CHUNK_GENERATION_QUEUE.ITEMS[0]
            log(
                "Main | Requested generation of ",
                self.WORLD.CHUNK_GENERATION_QUEUE.ITEMS[0],
            )
            self.WORLD.CHUNK_GENERATION_QUEUE.pop(0)

        return data
