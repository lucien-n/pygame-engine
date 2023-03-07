from multiprocessing import Queue
from scengine.vector2 import Vector2
import opensimplex
import time


class WorldGenerator:
    def __init__(self, seed: int | float = time.time()) -> None:
        self.SEED = seed

        self.GAME_PIPE = None

        self.RUNNING = False
        self.GAME_DATA = {}

        self.WORLD_SIZE = 300  # in chunks
        self.CHUNK_SIZE = 16  # in tiles
        self.TILE_SIZE = 16  # in pixels

        self.NOISE = opensimplex.seed(int(self.SEED))

        self.GENERATED_CHUNKS = set()
        self.CHUNKS = {}

    def update(self):
        self.GAME_DATA = self.GAME_PIPE.recv()

        self.RUNNING = self.GAME_DATA["running"]

        data = {}
        if self.GAME_DATA["chunks"]:
            raw_chunks_data = self.generate_chunks(self.GAME_DATA["chunks"])
            data["chunks"] = raw_chunks_data

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

    def generate_chunk(self, coordinates: Vector2) -> list[int, int, int]:
        """Generate a chunk based on set coordinates

        Args:
            coordinates (Vector2): chunk's coordinates

        Returns:
            list: chunk[x, y, noise]
        """
        chunk = [coordinates]
        factor_x = coordinates.x * self.CHUNK_SIZE
        factor_y = coordinates.y * self.CHUNK_SIZE

        if (
            not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_x < self.WORLD_SIZE
            or not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_y < self.WORLD_SIZE
        ):
            return

        for x in range(self.CHUNK_SIZE):
            for y in range(self.CHUNK_SIZE):
                noise = int(
                    opensimplex.noise2(
                        x=(x + factor_x) / self.CHUNK_SIZE,
                        y=(y + factor_y) / self.CHUNK_SIZE,
                    )
                    * 10
                )
                chunk.append([x, y, noise])

        return chunk

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
