import pygame.sprite
import pygame.surface
from test_game.world.tile import Tile


class Chunk:
    def __init__(
        self, game: object, world_x: int, world_y: int, tiles: list[Tile]
    ) -> None:
        self.GAME = game

        self.world_x = world_x
        self.world_y = world_y

        self.tiles = tiles
        self.surface = pygame.surface.Surface((256, 256))
        self.changed = True

    def update(self):
        [tile.update() for tile in self.tiles]

    def draw(self):
        if self.changed:
            self.redraw()

        self.GAME.DRAWING_SURFACE.blit(
            self.surface,
            (
                self.world_x * 256 - self.GAME.CAMERA.scroll.x,
                self.world_y * 256 - self.GAME.CAMERA.scroll.y,
            ),
        )

    def redraw(self):
        [
            self.surface.blit(tile.image, (tile.chunk_x, tile.chunk_y))
            for tile in self.tiles
        ]
