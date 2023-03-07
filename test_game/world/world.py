from scengine.queue import Queue
from test_game.world.chunk import Chunk
from test_game.world.tile import Tile

import pygame as pg


class World:
    def __init__(self, game: object) -> None:
        self.GAME = game

        self.WORLD_SIZE = 300  # in chunks
        self.CHUNK_SIZE = 16  # in tiles
        self.TILE_SIZE = 16  # in pixels

        self.CHUNK_GENERATION_Q = Queue()
        self.CHUNKS = {}
        self.LOADED_CHUNKS = []

    def update(self):
        self.CHUNK_GENERATION_Q.empty()

        # Chunk generation - Separate Process
        raw_chunks_data = []
        if "chunks" in self.GAME.WORLD_DATA.keys():
            raw_chunks_data = self.GAME.WORLD_DATA["chunks"]

        for raw_chunk_data in raw_chunks_data:
            if raw_chunk_data == None:
                continue

            chunk_x, chunk_y = raw_chunk_data[0]
            tiles = self.generate_tiles(raw_chunk_data[1:-1])
            chunk = Chunk(self.GAME, chunk_x, chunk_y, tiles)

            self.GAME.HUD.debug(f"Received chunk: {raw_chunk_data[0]}")

            self.CHUNKS[(chunk_x, chunk_y)] = chunk

        # Chunk updating - Main process
        self.LOADED_CHUNKS.clear()

        if self.GAME.PLAYER.current_chunk not in self.CHUNKS.keys():
            self.CHUNK_GENERATION_Q.add(self.GAME.PLAYER.current_chunk)

        if self.GAME.PLAYER.current_chunk not in self.LOADED_CHUNKS:
            self.LOADED_CHUNKS.append(
                (self.GAME.PLAYER.current_chunk.x, self.GAME.PLAYER.current_chunk.y)
            )

        [
            self.CHUNKS[chunk].update()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.CHUNKS
        ]

    def draw(self):
        [
            self.CHUNKS[chunk].draw()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.CHUNKS
        ]

    def load(self, chunk_position: tuple[int, int]) -> None:
        chunk = None
        if chunk_position in self.CHUNKS.keys():
            chunk = self.CHUNKS[chunk_position]
        else:
            self.CHUNK_GENERATION_Q.add(chunk)

    def generate_tiles(self, raw_tiles_data: list[int, int, int]) -> list[Tile]:
        tiles = []
        for raw_tile_data in raw_tiles_data:
            tiles.append(
                self.generate_tile(raw_tile_data[0], raw_tile_data[1], raw_tile_data[2])
            )

        return tiles

    def generate_tile(self, x: int, y: int, noise: int) -> Tile:
        """Returns a Tile object based on coordinates and noise value

        Args:
            x (int): x coordinate
            y (int): y coordinate
            noise (int): noise value

        Returns:
            Tile: tile
        """
        if noise < -4:
            type = "deep_water"
        elif noise < -3:
            type = "shallow_water"
        elif noise < -1:
            type = "sand"
        elif noise < 2.5:
            type = "grass"
        else:
            type = "stone"

        return Tile(x * 16, y * 16, self.GAME.SPRITES[type])
