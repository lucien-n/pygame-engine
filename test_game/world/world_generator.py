from scengine.vector2 import Vector2
from scengine.utils import log

import pygame as pg

import opensimplex
import time

from pathlib import Path

path = Path(__file__).parent


class WorldGenerator:
    def __init__(self, seed: int | float = time.time()) -> None:
        self.SEED = seed

        self.GAME_PIPE = None

        self.RUNNING = False
        self.GAME_DATA = {}

        self.WORLD_SIZE = 8192  # in chunks
        self.CHUNK_SIZE = 16  # in tiles
        self.TILE_SIZE = 16  # in pixels

        self.NOISE = opensimplex.seed(int(self.SEED))

        self.GENERATED_CHUNKS = set()
        self.CHUNKS = {}

        self.GENERATED_CHUNK_WAITING_TO_BE_SENT = []

        self.SPRITES = {}
        self.RECEIVED_SPRITES = False

    def update(self):
        self.GAME_DATA = self.GAME_PIPE.recv()

        # Only executes once
        if not self.RECEIVED_SPRITES and self.GAME_DATA["sprites"]:
            self.SPRITES = self.GAME_DATA["sprites"]
            self.RECEIVED_SPRITES = True
            log("WP | Received sprites")

        self.RUNNING = self.GAME_DATA["running"]

        data = {}
        if self.GAME_DATA["chunks"]:
            t1 = time.time()
            self.GENERATED_CHUNK_WAITING_TO_BE_SENT = self.generate_chunks(
                [self.GAME_DATA["chunks"][0]]
            )

            data["chunks"] = self.GENERATED_CHUNK_WAITING_TO_BE_SENT[0]
            self.GENERATED_CHUNK_WAITING_TO_BE_SENT.pop(0)
            log(
                "WP | Chunk generation took: ",
                round((time.time() - t1) * 1_000, 2),
                "ms",
            )

        self.GAME_PIPE.send(data)

    def run(self, pipe=None):
        self.GAME_PIPE = pipe
        self.RUNNING = True
        while self.RUNNING:
            self.update()

        exit(0)

    def generate_chunks(self, chunks_coordinates: list[tuple[int, int]]) -> list:
        """Generates chunks based on list of coordinates

        Args:
            chunks (list[tuple[int, int]]): list of chunks coordinates

        Returns:
            list: generated chunks
        """
        chunks = []
        for chunk_coordinates in chunks_coordinates:
            if chunk_coordinates in self.CHUNKS:
                chunks.append(self.CHUNKS[chunk_coordinates])
            else:
                chunks.append(self.generate_chunk(chunk_coordinates))
        return chunks

    def generate_chunk(self, coordinates: Vector2) -> dict:
        """Generate a chunk based on set coordinates

        Args:
            coordinates (Vector2): chunk's coordinates

        Returns:
            dict: chunk
        """
        factor_x = coordinates.x * self.CHUNK_SIZE
        factor_y = coordinates.y * self.CHUNK_SIZE

        # Check if chunk is out of bounds
        if (
            not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_x < self.WORLD_SIZE
            or not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_y < self.WORLD_SIZE
        ):
            return

        tiles = []
        for x in range(self.CHUNK_SIZE):
            for y in range(self.CHUNK_SIZE):
                noise = int(
                    opensimplex.noise2(
                        x=(x + factor_x) / self.CHUNK_SIZE,
                        y=(y + factor_y) / self.CHUNK_SIZE,
                    )
                    * 10
                )

                tiles.append([x, y, self.SPRITES[self.get_tile_type(noise)]])

        return [coordinates, tiles]

    def get_chunk(self, chunk_coordinates: tuple[int, int]) -> list:
        """Returns a chunk based on coordinates

        Args:
            player_chunk (tuple[int, int]): _description_

        Returns:
            list: _description_
        """
        if chunk_coordinates in self.CHUNKS:
            return self.CHUNKS[chunk_coordinates]
        else:
            chunk = self.generate_chunk(chunk_coordinates)
            self.CHUNKS[chunk[0]] = chunk
            return chunk

    def get_tile_type(self, noise: int) -> str:
        """Returns a type based on noise value

        Args:
            noise (int): noise value

        Returns:
            str: type
        """
        if noise < -4:
            tile_type = "deep_water"
        elif noise < -3:
            tile_type = "shallow_water"
        elif noise < -1:
            tile_type = "sand"
        elif noise < 2.5:
            tile_type = "grass"
        else:
            tile_type = "stone"

        return tile_type
