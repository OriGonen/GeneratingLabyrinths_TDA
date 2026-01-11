import random
import time
from Maze3D import Maze3D


def method_a_3d(W=5, H=5, D=5, wall_num=-1, max_time=60):
    t0 = time.time()
    maze = Maze3D(W, H, D)
    rng = random.Random()

    # get all possible internal wall locations
    candidates = maze.non_existing_walls()

    # shuffle for random picking
    rng.shuffle(candidates)

    current_wall_count = 0

    for x, y, z, direction in candidates:
        if time.time() - t0 > max_time:
            break

        # Stop condition 2: Specific wall count reached (if not -1)
        if wall_num > 0 and current_wall_count >= wall_num:
            break

        # Try adding the wall
        maze.add_wall(x, y, z, direction)

        # Check constraint
        if not maze.is_fully_reachable():
            # If it creates an unreachable chamber, revert immediately
            maze.add_wall(x, y, z, direction, delete=True)
        else:
            # Wall was successfully added
            current_wall_count += 1

    return maze, current_wall_count