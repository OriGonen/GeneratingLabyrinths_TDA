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


        not_walls = maze.non_existing_walls()

        x,y,direction = rng.choice(not_walls)

        # try adding wall
        maze.add_wall(x, y, direction)

        # if we are constrained, we must check and reject if an unreachable chamber appears
        if (constrained and not maze.is_fully_reachable()):
            maze.add_wall(x, y, direction, delete=True)

    return maze, maze.count_walls()

# (b) randomly walking along the 1-skeleton and adding the visited edges
def method_b(width=10, height=10, constrained=True, wall_num=50, max_time=20):
    maze = Maze(width, height)
    rng = random.Random()

    # we will pick a starting point from the boundary
    # the boundary are (0,y), (width, y), (x,0), (x,height)
    # note that the vertexes live on (width+1)x(height+1) grid
    boundary_vertex = [ (x,y) for x in range(width+1) for y in range(height+1) if x==0 or y==0 or x==width or y==height ]

    # initial point
    vx, vy = rng.choice(boundary_vertex)
    t0 = time.time()
    while maze.count_walls() < wall_num and time.time() - t0 < max_time:
        # we now need to check which moves are possible
        possible_moves = []
        if vx > 0:
            possible_moves.append( (vx-1, vy) )
        if vx < width:
            possible_moves.append( (vx+1, vy) )
        if vy > 0:
            possible_moves.append( (vx, vy-1) )
        if vy < height:
            possible_moves.append( (vx, vy+1) )

        # we should have at least one move at all times
        assert len(possible_moves) > 0

        # pick one move
        next_v = rng.choice(possible_moves)

        maze.vertex_add_wall( (vx, vy), next_v )
        # if we are constrained, we must check and reject if an unreachable chamber appears
        if (constrained and not maze.is_fully_reachable()):
            maze.vertex_add_wall( (vx, vy), next_v, delete=True )
            # we delete the wall and don't move the vertex
        else:
            vx, vy = next_v

    return maze, maze.count_walls()


# (c) starting with the 1-skeleton of a full triangulation and randomly erasing edges
def method_c(width=10, height=10, max_time=20):
    # that's not really needed but I prefer to use it like this with a constant in case we will want to check later with different values
    UNREACHABLE_CHAMBERS_STOP = 3

    # start with a full maze
    maze = Maze(width, height, full=True)

    rng = random.Random()
    directions = ["Top", "Bottom", "Left", "Right"]
    t0=time.time()

    # remove edges by random until we are left with 3 (UNREACHABLE_CHAMBERS_STOP constant) unreachable chambers
    while maze.count_unreachable_chambers() > UNREACHABLE_CHAMBERS_STOP and time.time() - t0 < max_time:
        # pick random existing wall, and remove it
        x,y,direction = rng.choice(maze.existing_walls())
        maze.add_wall(x, y, direction, delete=True)

    # now, we should erase only 3 (UNREACHABLE_CHAMBERS_STOP constant) more edges to eliminate all unreachable chambers
    while maze.count_unreachable_chambers() > 0 and time.time() - t0 < max_time:
        prev_count = maze.count_unreachable_chambers()

        # for all walls: remove it, and see if it decreased the number of unreachable chambers
        walls=maze.existing_walls()
        for wall in walls:
            x,y, direction = wall
            maze.add_wall(x, y, direction, delete=True)

            if maze.count_unreachable_chambers() < prev_count:
                break
            maze.add_wall(x, y, direction)

    return maze, maze.count_unreachable_chambers()


