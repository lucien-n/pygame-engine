import pygame as pg
from scengine.vector2 import Vector2


class Chunk:
    def __init__(self, game: object, world_coords: Vector2, tiles: list) -> None:
        self.GAME = game

        self.world_coords = world_coords
        self.tiles = tiles
        self.image = pg.surface.Surface((256, 256))

        self.needs_redraw = True

    def update(self) -> None:
        pass

    def draw(self) -> None:
        if self.needs_redraw:
            self.redraw()

        self.GAME.DRAWING_SURFACE.blit(
            self.image,
            (
                self.world_coords[0] * 256 - self.GAME.CAMERA.scroll.x,
                self.world_coords[1] * 256 - self.GAME.CAMERA.scroll.y,
            ),
        )

    def redraw(self) -> None:
        [
            self.image.blit(
                tile.image, (tile.chunk_coords[0] * 16, tile.chunk_coords[1] * 16)
            )
            for tile in self.tiles
        ]
        self.needs_redraw = False
