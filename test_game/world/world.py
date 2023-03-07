from scengine.queue import Queue
from scengine.vector2 import Vector2

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
        self.GENERATED_CHUNKS = {}
        self.LOADED_CHUNKS = []

    def update(self):
        self.CHUNK_GENERATION_Q.empty()

        # Chunk generation - Separate Process
        raw_chunks_data = []
        if "chunks" in self.GAME.WORLD_DATA.keys():
            raw_chunks_data = self.GAME.WORLD_DATA["chunks"]
            self.build_chunks(raw_chunks_data)

        # Chunk updating - Main process
        self.LOADED_CHUNKS.clear()

        for rows in render_distance_matrices["diamond"]:
            for matrice in rows:
                chunk_pos: Vector2 = self.GAME.PLAYER.current_chunk + matrice

                # Adds chunk to generation queue if it doesn't exists
                if not self.is_chunk_generated(chunk_pos):
                    self.CHUNK_GENERATION_Q.add(chunk_pos)

                # Adds chunk to the loaded chunks
                if not self.is_chunk_loaded(chunk_pos):
                    self.LOADED_CHUNKS.append(chunk_pos.totuple())

        [
            self.get_chunk(chunk).update()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.GENERATED_CHUNKS
        ]

    def draw(self):
        [
            self.get_chunk(chunk).draw()
            for chunk in self.LOADED_CHUNKS
            if chunk in self.GENERATED_CHUNKS
        ]

    def build_chunks(self, raw_chunks_data: list) -> None:
        for raw_chunk_data in raw_chunks_data:
            if raw_chunk_data == None:
                continue

            chunk_x, chunk_y = raw_chunk_data[0]
            tiles = self.generate_tiles(raw_chunk_data[1:])
            chunk = Chunk(self.GAME, chunk_x, chunk_y, tiles)

            self.GAME.HUD.debug(f"Received chunk: {raw_chunk_data[0]}")

            self.GENERATED_CHUNKS[(chunk_x, chunk_y)] = chunk

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
