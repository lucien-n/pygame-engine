import sys
from multiprocessing import Process, Pipe

from test_game.world.world_generator import WorldGenerator

from test_game.main import Game

if __name__ == "__main__":
    TILE_SIZE = 16  # in pixels
    CHUNK_SIZE = 16  # in tiles
    WORLD_SIZE = 4_196  # in chunks

    world = WorldGenerator(TILE_SIZE, CHUNK_SIZE, WORLD_SIZE)
    parent_conn, child_conn = Pipe()
    world_process = Process(name="WorldProcess", target=world.run, args=(child_conn,))
    world_process.start()

    game = Game(
        tile_size=TILE_SIZE,
        chunk_size=CHUNK_SIZE,
        world_size=WORLD_SIZE,
        world_generator=world,
        world_pipe=parent_conn,
        world_process=world_process,
    )
    game.run()
