# generation methods, as in instructions
"""
(a) by randomly adding edges one by one;
(b) by randomly walking along the 1-skeleton of the chosen triangulation and adding the visited edges.
(c) by starting with the 1-skeleton of a full triangulation and then randomly erasing edges.
"""
import random
from Maze import Maze
import time


# (a) randomly adding edges one by one
def method_a(width=10, height=10, constrained=True, wall_num=-1, max_time=20):
    # by default, the function will stop when the first unreachable chamber occurs
    # else, it will keep going until wall_num walls occur

    # if not constrained, then the desired wall_num must be entered
    assert constrained or wall_num > 0

    t0=time.time()
    maze = Maze(width, height)
    rng = random.Random()
    directions = ["Top", "Bottom", "Left", "Right"]

    # just initializing them because we'll use them later
    x = -1; y = -1; direction = ""


    while True:
        # stop conditions:
        if not constrained and maze.count_walls() >= wall_num:
            break
        if constrained and wall_num > 0 and maze.count_walls() >= wall_num:
            break
        if time.time() - t0 > max_time:
            break


        x = rng.randint(0, width-1)
        y = rng.randint(0, height-1)

        direction = str(rng.choice(directions))

        # try adding wall
        maze.add_wall(x, y, direction)

        # if we are constrained, we must check and reject if an unreachable chamber appears
        if (constrained and not maze.is_fully_reachable()):
            maze.add_wall(x, y, direction, delete=True)

    return maze, maze.count_walls()



