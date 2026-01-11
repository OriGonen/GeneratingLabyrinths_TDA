import random
import time
from Maze3D import Maze3D

def method_a_3d(W=5, H=5, D=5, wall_num=-1, max_time=60):
    t0 = time.time()
    maze = Maze3D(W, H, D)
    rng = random.Random()

    while True:
        if wall_num > 0 and maze.count_walls() >= wall_num:
            break
        if time.time() - t0 > max_time:
            break

        candidates = maze.non_existing_walls()
        if not candidates:
            break

        x, y, z, d = rng.choice(candidates)
        maze.add_wall(x, y, z, d)

        if not maze.is_fully_reachable():
            maze.add_wall(x, y, z, d, delete=True)

    return maze, maze.count_walls()