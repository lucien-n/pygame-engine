import opensimplex
import time
from scengine.vector2 import Vector2
from scengine.utils import log


class WorldGenerator:
    def __init__(
        self,
        tile_size: int,
        chunk_size: int,
        world_size: int,
        seed: float = time.time(),
    ) -> None:
        self.RUNNING = False
        self.GAME_PIPE = None
        self.GAME_DATA = None

        self.TILE_SIZE = tile_size
        self.CHUNK_SIZE = chunk_size
        self.WORLD_SIZE = world_size

        self.SEED = seed
        self.NOISE = opensimplex.seed(int(self.SEED))

        self.GENERATED_CHUNKS: dict[
            tuple[int, int] : list[tuple[int, int], list[int, int, str]]
        ] = {}

    def update(self):
        self.GAME_DATA = self.GAME_PIPE.recv()
        log("World | Received data from Main")

        # Close WorldProcess if MainProcess is closed
        self.RUNNING = self.GAME_DATA["running"]

        data = {}
        # Check if a chunk generation has been requested
        if "chunk" in self.GAME_DATA.keys():
            log("World | Generating chunk ", self.GAME_DATA["chunk"])
            data["chunk"] = self.generate_chunk(self.GAME_DATA["chunk"])
        else:
            log("World | No chunk generation has been requested")

        self.GAME_PIPE.send(data)
        log("World | Sent data to Main")

    def run(self, pipe=None):
        self.GAME_PIPE = pipe
        self.RUNNING = True
        log("World | Starting world generator")

        while self.RUNNING:
            self.update()

        exit(0)

    def generate_chunk(
        self, chunk_coordinates: tuple[int, int]
    ) -> list[tuple[int, int], list[int, int, str]]:
        """Generates a chunk and it's tiles

        Args:
            chunk_coordinates (Vector2): coordinates of the chunk

        Returns:
            list[Vector2, list[int, int, str]]: raw chunk data
        """

        # Check if the chunk has already been generated (should never happen)
        if self.is_chunk_generated(chunk_coordinates):
            log("World | Chunk ", chunk_coordinates, " has already been generated")
            return self.get_chunk(chunk_coordinates)

        chunk = [chunk_coordinates]
        factor_x: int = chunk_coordinates[0] * self.CHUNK_SIZE
        factor_y: int = chunk_coordinates[1] * self.CHUNK_SIZE

        # Check if chunk is out of world bounds
        if (
            not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_x < self.WORLD_SIZE
            or not (-self.WORLD_SIZE + self.CHUNK_SIZE) < factor_y < self.WORLD_SIZE
        ):
            return

        # Generate the tiles
        tiles = []
        for tile_x in range(self.CHUNK_SIZE):
            for tile_y in range(self.CHUNK_SIZE):
                noise_value = int(
                    opensimplex.noise2(
                        x=(tile_x + factor_x) / self.WORLD_SIZE,
                        y=(tile_y + factor_y) / self.WORLD_SIZE,
                    )
                    * 10
                )

                tile_type = self.get_tile_type(noise_value)
                tiles.append([tile_x, tile_y, tile_type])

        chunk.append(tiles)

        # Save the chunk
        self.GENERATED_CHUNKS[chunk_coordinates] = chunk

        return chunk

    def get_tile_type(self, noise: int) -> str:
        """Get the type of the tile depending on the noise

        Args:
            noise (int): noise value of the tile

        Returns:
            str: tile type
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

    def get_chunk(self, chunk_coordinates: tuple[int, int]) -> list:
        if self.is_chunk_generated(chunk_coordinates):
            return self.GENERATED_CHUNKS[chunk_coordinates]

        return None

    def is_chunk_generated(self, chunk_coordinates: tuple[int, int]) -> bool:
        return chunk_coordinates in self.GENERATED_CHUNKS.keys()
