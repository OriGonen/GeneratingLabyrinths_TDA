import random
import time

# To keep the loops, we remove them from potential candidates
# The loop-related edges are kept in the maze_surface.protected_edges set

def general_method_a(
        maze_surface, boundary_function, wall_num=-1, max_time=20
):
    # Generate all the functions
    rng = random.Random()
    t0 = time.time()

    if wall_num == -1:
        wall_num = len(maze_surface.edges) - len(maze_surface.protected_edges)

    candidate_edges = [e for e in maze_surface.edges
                       if not e.present and e not in maze_surface.protected_edges]
    rng.shuffle(candidate_edges)

    for e in candidate_edges:
        if maze_surface.wall_count() >= wall_num or time.time() - t0 > max_time:
            break

        e.present = True

        if not maze_surface.is_fully_reachable(boundary_function(maze_surface)):
            e.present = False

    return maze_surface


def general_method_b(
        maze_surface, boundary_function, constrained=True,
        wall_num=-1, max_time=20
):
    rng = random.Random()
    t0 = time.time()

    if wall_num == -1:
        wall_num = len(maze_surface.edges) - len(maze_surface.protected_edges)

    current_cell = rng.choice(maze_surface.cells)

    while maze_surface.wall_count() < wall_num and time.time() - t0 < max_time:
        available_edges = [e for e in current_cell.edges
                           if not e.present and e not in maze_surface.protected_edges]

        if not available_edges:
            current_cell = rng.choice(maze_surface.cells)
            continue

        e = rng.choice(available_edges)
        e.present = True

        if constrained and not maze_surface.is_fully_reachable(boundary_function(maze_surface)):
            e.present = False
        else:
            other_cell = next(iter(e.cells - {current_cell}))
            current_cell = other_cell

    return maze_surface


def general_method_c(maze_surface, boundary_function, max_time=20):
    UNREACHABLE_CHAMBERS_STOP = 3

    for e in maze_surface.edges:
        e.present = True

    for e in maze_surface.protected_edges:
        e.present = False

    rng = random.Random()
    t0 = time.time()

    while (
            maze_surface.count_unreachable_cells(boundary_function(maze_surface)) > UNREACHABLE_CHAMBERS_STOP
            and time.time() - t0 < max_time
    ):
        existing = [e for e in maze_surface.existing_edges()
                    if e not in maze_surface.protected_edges]
        if not existing:
            break
        rng.shuffle(existing)
        existing[0].present = False

    while (
            maze_surface.count_unreachable_cells(boundary_function(maze_surface)) > 0
            and time.time() - t0 < max_time
    ):
        prev_count = maze_surface.count_unreachable_cells(boundary_function(maze_surface))

        walls = [e for e in maze_surface.existing_edges()
                 if e not in maze_surface.protected_edges]
        rng.shuffle(walls)
        for e in walls:
            e.present = False

            if maze_surface.count_unreachable_cells(boundary_function(maze_surface)) < prev_count:
                break
            e.present = True

    return maze_surface