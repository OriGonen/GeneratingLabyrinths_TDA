from collections import deque

from matplotlib import pyplot as plt


# More explicit separation between cells and edges just so we can pack klein bottles and torus into one class

class Cell:
    # A chamber in the maze
    def __init__(self, cid):
        self.id = cid
        # Set since there can't be multiple edges between two cells
        self.edges = set()


class Edge:
    def __init__(self, eid, cell_a, cell_b=None):
        self.id = eid
        self.cells = {cell_a} if cell_b is None else {cell_a, cell_b}
        # Indicates if a wall is present between the two cells
        self.present = False


class MazeSurface:
    def __init__(self, cells, edges):
        self.cells = cells
        self.edges = edges
        self.protected_edges = set()
        # Provide the cells with their corresponding edges
        for e in edges:
            for c in e.cells:
                c.edges.add(e)

    def wall_count(self):
        # Counts all existing walls
        return sum(1 for e in self.edges if e.present)

    def count_unreachable_cells(self, boundary_cells):
        reachable = reachable_cells(boundary_cells)
        return len(self.cells) - len(reachable)

    def is_fully_reachable(self, boundary_cells):
        return self.count_unreachable_cells(boundary_cells) == 0

    def get_edge_between(self, cell_a, cell_b):
        for e in cell_a.edges:
            if cell_b in e.cells:
                return e
        return None

    def existing_edges(self):
        return [e for e in self.edges if e.present]

    def non_existing_edges(self):
        return [e for e in self.edges if not e.present]

    def draw(self, show_wrap_edges=False, name=None, method=None):
        xs = [c.id[0] for c in self.cells]
        ys = [c.id[1] for c in self.cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        W = max_x - min_x + 1
        H = max_y - min_y + 1
        fig, ax = plt.subplots(figsize=(W, H))

        # Draw black walls (present edges)
        for e in self.edges:
            if not e.present:
                continue

            c1, c2 = tuple(e.cells)
            (x1, y1), (x2, y2) = c1.id, c2.id

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            if dx <= 1 and dy <= 1:
                if dx == 1 and dy == 0:
                    x = max(x1, x2)
                    y = y1
                    ax.plot([x, x], [y, y + 1], color="black", linewidth=2)
                elif dy == 1 and dx == 0:
                    x = x1
                    y = max(y1, y2)
                    ax.plot([x, x + 1], [y, y], color="black", linewidth=2)
            elif show_wrap_edges:
                ax.plot(
                    [x1 + 0.5, x2 + 0.5],
                    [y1 + 0.5, y2 + 0.5],
                    color="red",
                    linestyle="dashed",
                    linewidth=2,
                )

        # Draw blue dashed loops (protected edges)
        if self.protected_edges:
            # Horizontal loops
            y_coords = set()
            for e in self.protected_edges:
                c1, c2 = tuple(e.cells)
                y1, y2 = c1.id[1], c2.id[1]
                if y1 == y2:
                    y_coords.add(y1)

            for y in y_coords:
                ax.plot([min_x, max_x + 1], [y + 0.5, y + 0.5],
                        color="blue", linewidth=2.5, linestyle="dashed", alpha=0.7)

            # Vertical loops
            x_coords = set()
            for e in self.protected_edges:
                c1, c2 = tuple(e.cells)
                x1, x2 = c1.id[0], c2.id[0]
                if x1 == x2:
                    x_coords.add(x1)

            for x in x_coords:
                ax.plot([x + 0.5, x + 0.5], [min_y, max_y + 1],
                        color="blue", linewidth=2.5, linestyle="dashed", alpha=0.7)

        # Draw grey border around the square
        ax.plot([min_x, max_x + 1, max_x + 1, min_x, min_x],
                [min_y, min_y, max_y + 1, max_y + 1, min_y],
                color="grey", linewidth=3)

        # Add method text above
        if method:
            ax.text(0.5 * (min_x + max_x + 1), max_y + 1.3, f"Method: {method}",
                    fontsize=14, fontweight='bold', ha='center')

        ax.set_xlim(min_x - 0.2, max_x + 1.2)
        ax.set_ylim(min_y - 0.2, max_y + 1.4)
        ax.set_aspect("equal")
        ax.axis("off")

        plt.tight_layout()

        if name is not None:
            filename = f"{name}.png"
            plt.savefig(filename)
        else:
            plt.show()


def reachable_cells(start_cells):
    # Returns all reachable cells
    visited = set(start_cells)
    queue = deque(start_cells)

    # Run BFS to find all reachable cells
    while queue:
        cell = queue.popleft()
        for edge in cell.edges:
            # Open edges only
            if not edge.present:
                for other in edge.cells:
                    if other not in visited:
                        visited.add(other)
                        queue.append(other)
    return visited


# No actual boundary, so just pick an arbitrary cell
def torus_boundary_cells(maze_surface):
    return {maze_surface.cells[0]}


# No actual boundary, so just pick an arbitrary cell
def klein_boundary_cells(maze_surface):
    return {maze_surface.cells[0]}

# Torus complex/grid containing W x H cells, with periodic boundary conditions
# Torus wraps: up/down, left/right.
def build_torus_complex(W, H):
    cells = {}
    edges = []
    eid = 0

    for x in range(W):
        for y in range(H):
            cells[(x, y)] = Cell((x, y))

    for x in range(W):
        for y in range(H):
            c = cells[(x, y)]

            # Horizontal wrap
            c2 = cells[((x + 1) % W, y)]
            # Create edge
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)

            # Vertical wrap
            c2 = cells[(x, (y + 1) % H)]
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)

    return MazeSurface(list(cells.values()), edges)


# Klein bottle complex/grid containing W x H cells, with periodic boundary conditions
# Klein bottle wraps: up/down, left/(flipped) right
def build_klein_complex(W, H):
    cells = {}
    edges = []
    eid = 0

    for x in range(W):
        for y in range(H):
            cells[(x, y)] = Cell((x, y))

    for x in range(W):
        for y in range(H):
            c = cells[(x, y)]

            # Horizontal wrap as in torus
            c2 = cells[((x + 1) % W, y)]
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)

            # Vertical wrap is twisted
            if y < H - 1:
                c2 = cells[(x, y + 1)]
            else:
                c2 = cells[(W - 1 - x, 0)]

            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)

    return MazeSurface(list(cells.values()), edges)


# Enforces the two fundamental loops required for non-zero H_1
# The horizontal loop and the vertical loop
# I.e., one loop around the "x direction" and one loop around the "y direction"
# The loops are then "opened" and we make sure they never get closed
def force_torus_generators(maze_surface, W, H, y0=None, x0=None):
    if y0 is None:
        y0 = H // 2
    if x0 is None:
        x0 = W // 2

    cells_dict = {c.id: c for c in maze_surface.cells}

    # Horizontal generator (loop)
    # For each x is range [0,W] set the edge to true
    for x in range(W):
        c1 = cells_dict[(x, y0)]
        c2 = cells_dict[((x + 1) % W, y0)]
        e = maze_surface.get_edge_between(c1, c2)
        if e:
            e.present = False
            maze_surface.protected_edges.add(e)

    # Vertical generator (loop)
    for y in range(H):
        c1 = cells_dict[(x0, y)]
        c2 = cells_dict[(x0, (y + 1) % H)]
        e = maze_surface.get_edge_between(c1, c2)
        if e:
            e.present = False
            maze_surface.protected_edges.add(e)

# Two (loops) generators for the Klein bottle
def force_klein_generators(maze_surface, W, H, y0=None, x0=None):
    if y0 is None:
        y0 = H // 2
    if x0 is None:
        x0 = W // 2

    cells_dict = {c.id: c for c in maze_surface.cells}

    # Same horizontal generator as for Torus
    for x in range(W):
        c1 = cells_dict[(x, y0)]
        c2 = cells_dict[((x + 1) % W, y0)]
        e = maze_surface.get_edge_between(c1, c2)
        if e:
            e.present = False
            maze_surface.protected_edges.add(e)

    # Vertical generator accounts for the flip
    for y in range(H):
        c1 = cells_dict[(x0, y)]
        if y < H - 1:
            c2 = cells_dict[(x0, y + 1)]
        else:
            c2 = cells_dict[(W - 1 - x0, 0)]
        e = maze_surface.get_edge_between(c1, c2)
        if e:
            e.present = False
            maze_surface.protected_edges.add(e)