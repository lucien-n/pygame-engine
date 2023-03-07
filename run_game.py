import sys
from multiprocessing import Process, Pipe

from test_game.world.world_generator import WorldGenerator

sys.dont_write_bytecode = True

from test_game.main import Game

if __name__ == "__main__":
    world = WorldGenerator()
    parent_conn, child_conn = Pipe()
    world_process = Process(name="WorldProcess", target=world.run, args=(child_conn,))
    world_process.start()

    game = Game(
        world_generator=world, world_pipe=parent_conn, world_process=world_process
    )
    game.run()
