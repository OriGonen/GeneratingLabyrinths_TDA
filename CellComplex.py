# for the 2D generalization

from collections import deque
from matplotlib import pyplot as plt


class Cell:
    def __init__(self, cid):
        self.id = cid
        self.edges = set()

class Edge:
    def __init__(self, eid, cell_a, cell_b=None):
        self.id = eid
        self.cells = {cell_a} if cell_b is None else {cell_a, cell_b}
        self.present = False


# CellComplex is generalization of Maze
class CellComplex:
    def __init__(self, cells, edges):
        self.cells = cells
        self.edges = edges

        for e in edges:
            for c in e.cells:
                c.edges.add(e)

    def wall_count(self):
        return sum(1 for e in self.edges if e.present)
    def count_unreachable_cells(self, boundary_cells):
        reachable = reachable_cells(boundary_cells)
        return len(self.cells) - len(reachable)

    def draw(self, show_wrap_edges=False, name=None):

        # get boundaries from cell ids
        xs = [c.id[0] for c in self.cells]
        ys = [c.id[1] for c in self.cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        W = max_x - min_x + 1
        H = max_y - min_y + 1
        fig, ax = plt.subplots(figsize=(W, H))

        # draw the walls
        for e in self.edges:
            if not e.present:
                continue

            c1, c2 = tuple(e.cells)
            (x1, y1), (x2, y2) = c1.id, c2.id

            dx = x2 - x1
            dy = y2 - y1

            # vertical wall (between left-right neighbors)
            if abs(dx) == 1 and dy == 0:
                x = max(x1, x2)
                y = y1
                ax.plot([x, x], [y, y + 1], color="black", linewidth=2)

            # horizontal wall (between up-down neighbors)
            elif abs(dy) == 1 and dx == 0:
                x = x1
                y = max(y1, y2)
                ax.plot([x, x + 1], [y, y], color="black", linewidth=2)

            # wrap-around
            elif show_wrap_edges:
                ax.plot(
                    [x1 + 0.5, x2 + 0.5],
                    [y1 + 0.5, y2 + 0.5],
                    color="red",
                    linestyle="dashed",
                    linewidth=2,
                )

        ax.set_xlim(min_x, max_x + 1)
        ax.set_ylim(min_y, max_y + 1)
        ax.set_aspect("equal")
        ax.axis("off")

        plt.tight_layout()

        if name is not None:
            filename = f"{name}.png"
            plt.savefig(filename)
        else:
            plt.show()

# find all cells that are reachable from the cells start_cells
def reachable_cells(start_cells):
    visited = set(start_cells)
    queue = deque(start_cells)

    while queue:
        cell = queue.popleft()
        for edge in cell.edges:
            if not edge.present:
                for other in edge.cells:
                    if other not in visited:
                        visited.add(other)
                        queue.append(other)
    return visited


# no boundary, so just pick an arbitrary cell
def torus_boundary_cells(complex):
    return {complex.cells[0]}

# no boundary, so just pick an arbitrary cell
def klein_boundary_cells(complex):
    return {complex.cells[0]}


# function to create a torus adjacency
def build_torus_complex(W, H):
    cells = {}
    edges = []
    eid = 0

    for x in range(W):
        for y in range(H):
            cells[(x, y)] = Cell((x, y))

    # creating edges. only creating right and up (not down and left) to avoid duplicates
    for x in range(W):
        for y in range(H):
            c = cells[(x, y)]

            # right (wrap around)
            c2 = cells[ ((x+1)%W,y) ]
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)
            c.edges.add(e)
            c2.edges.add(e)

            # up (wrap around)
            c2 = cells[ (x,(y+1)%H) ]
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)
            c.edges.add(e)
            c2.edges.add(e)

    return CellComplex(list(cells.values()), edges)


# function to create Klein bottle adjacency
# left <-> right (normal wrap around)
# bottom <-> top with horizontal flip
def build_klein_complex(W, H):
    cells = {}
    edges = []
    eid = 0

    for x in range(W):
        for y in range(H):
            cells[(x, y)] = Cell((x, y))

    # creating edges. only creating right and up (not down and left) to avoid duplicates
    for x in range(W):
        for y in range(H):
            c = cells[(x, y)]

            # right (normal wrap around)
            c2 = cells[((x + 1) % W, y)]
            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)
            c.edges.add(e)
            c2.edges.add(e)

            # up (twisted wrap around)
            if y < H - 1:
                c2 = cells[ (x,y+1) ]
            else:
                c2 = cells[ (W-1-x,0) ]


            e = Edge(eid, c, c2)
            eid += 1
            edges.append(e)
            c.edges.add(e)
            c2.edges.add(e)

    return CellComplex(list(cells.values()), edges)
