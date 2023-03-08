from scengine.queue import Queue
from scengine.vector2 import Vector2
from scengine.utils import log

import pygame as pg
import time

from test_game.world.chunk import Chunk
from test_game.world.tile import Tile
from test_game.world.matrices import render_distance_matrices


class World:
    def __init__(self, game: object) -> None:
        self.GAME = game

        self.WORLD_SIZE = 300  # in chunks
        self.CHUNK_SIZE = 16  # in tiles
        self.TILE_SIZE = 16  # in pixels

        self.CHUNK_GENERATION_Q = Queue()
        self.GENERATED_CHUNKS: dict[Vector2 : pg.sprite.Sprite] = {}
        self.LOADED_CHUNKS = []

    def update(self):
        self.CHUNK_GENERATION_Q.empty()

        # Chunk generation - Separate Process
        raw_chunk_data = []
        if "chunks" in self.GAME.WORLD_DATA.keys():
            raw_chunk_data = self.GAME.WORLD_DATA["chunks"]
            log("MP | Building chunks")
            t1 = time.time()
            self.build_chunks(raw_chunk_data)
            log(
                "MP | Chunk building took: ", round((time.time() - t1) * 1_000, 2), "ms"
            )

        # Chunk updating - Main process
        self.LOADED_CHUNKS.clear()

        for rows in render_distance_matrices["diamond"]:
            for matrice in rows:
                chunk_coords: Vector2 = self.GAME.PLAYER.current_chunk + matrice

                # Adds chunk to generation queue if it doesn't exists
                if not self.is_chunk_generated(chunk_coords):
                    self.CHUNK_GENERATION_Q.add(chunk_coords)

                # Adds chunk to the loaded chunks
                if not self.is_chunk_loaded(chunk_coords):
                    self.LOADED_CHUNKS.append(chunk_coords.totuple())

        # Update loaded chunks
        [
            self.get_chunk(chunk).update()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.GENERATED_CHUNKS
        ]

    def draw(self):
        # Draw loaded chunks
        [
            self.get_chunk(chunk).draw()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.GENERATED_CHUNKS
        ]

    def build_chunks(self, raw_chunk_data: list) -> None:
        if raw_chunk_data == None:
            return

        chunk_coords: Vector2 = raw_chunk_data[0]
        tiles = self.generate_tiles(raw_chunk_data)
        chunk = Chunk(self.GAME, chunk_coords, tiles)
        chunk.redraw()

        log("MP | Received chunk:", raw_chunk_data[0])

        self.GENERATED_CHUNKS[chunk_coords.totuple()] = chunk

    def get_chunk(self, chunk_coordinates: tuple[int, int] | Vector2) -> Chunk:
        if type(chunk_coordinates) == Vector2:
            return self.GENERATED_CHUNKS[(chunk_coordinates.x, chunk_coordinates.y)]
        else:
            return self.GENERATED_CHUNKS[chunk_coordinates]

    def is_chunk_generated(self, chunk_position: Vector2) -> bool:
        """Check if chunk is in CHUNKS

        Args:
            chunk_position (Vector2): chunk position

        Returns:
            bool: is chunk in CHUNKS
        """
        return (chunk_position.x, chunk_position.y) in self.GENERATED_CHUNKS

    def is_chunk_loaded(self, chunk_position: Vector2) -> bool:
        """Check if chunk is in LOADED_CHUNKS

        Args:
            chunk_position (Vector2): chunk position

        Returns:
            bool: is chunk in LOADED_CHUNKS
        """
        return (chunk_position.x, chunk_position.y) in self.LOADED_CHUNKS

    def load(self, chunk_position: tuple[int, int]) -> None:
        chunk = None
        if chunk_position in self.GENERATED_CHUNKS.keys():
            chunk = self.GENERATED_CHUNKS[chunk_position]
        else:
            self.CHUNK_GENERATION_Q.add(chunk)

    def generate_tiles(self, raw_tiles_data: list[Vector2, int]) -> list[Tile]:
        tiles = []
        for raw_tile_data in raw_tiles_data[1]:
            tiles.append(
                Tile(
                    Vector2(raw_tile_data[0], raw_tile_data[1]),
                    self.GAME.arr2surf(raw_tile_data[2]),
                )
            )

        return tiles
