from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Cell3D:
    def __init__(self):
        # each cell contains 6 faces, represented by bools indicating if a wall exists
        # n is negative (smaller coordinate), p is positive (larger coordinate)
        self.walls = {"xp": False, "xn": False, "yp": False, "yn": False, "zp": False, "zn": False}


class Maze3D:
    OPPOSITES = {"xp": "xn", "xn": "xp", "yp": "yn", "yn": "yp", "zp": "zn", "zn": "zp"}
    DELTAS = {"xp": (1, 0, 0), "xn": (-1, 0, 0), "yp": (0, 1, 0), "yn": (0, -1, 0), "zp": (0, 0, 1), "zn": (0, 0, -1)}

    def __init__(self, W, H, D, start=None):
        # Create a grid of WxHxD cells
        self.W, self.H, self.D = W, H, D
        self.grid = [[[Cell3D() for _ in range(D)] for _ in range(H)] for _ in range(W)]
        if start is not None:
            self.start = start
        else:
            # Just choose the front bottom corner in the plotting.
            self.start = (self.W - 1, self.H - 1, self.D - 1)

    # Wrapper func. for checking if it is a valid cell
    def in_bounds(self, x, y, z):
        return 0 <= x < self.W and 0 <= y < self.H and 0 <= z < self.D

    # Detect if a cell is on the boundary of the grid
    def is_boundary(self, x, y, z):
        return x == 0 or y == 0 or z == 0 or x == self.W - 1 or y == self.H - 1 or z == self.D - 1

    def add_wall(self, x, y, z, direction, delete=False):
        dx, dy, dz = self.DELTAS[direction]
        nx, ny, nz = x + dx, y + dy, z + dz

        if not self.in_bounds(nx, ny, nz):
            return  # Out of bounds

        # Update both the current cell and the neighbor
        # Since a shared edge has a state in both of the cells
        self.grid[x][y][z].walls[direction] = not delete
        self.grid[nx][ny][nz].walls[self.OPPOSITES[direction]] = not delete

    def count_unreachable_chambers_deprecated(self):
        # NOTE: This is the deprecated way of counting unreachable chambers.
        #       This one counts unreachable chambers from all boundary cells.
        #       The reason we removed this one because the end maximal maze is always the same (at least on the bounds).
        #       => It results in a foster, where each boundary cell is its own single vertex graph.
        #           With trees that represent the internal nodes that need to be connected together.
        visited = set()
        queue = deque()

        # Start with boundary cells
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    if self.is_boundary(x, y, z):
                        visited.add((x, y, z))
                        queue.append((x, y, z))

        while queue:
            x, y, z = queue.popleft()
            cell = self.grid[x][y][z]

            # Check all 6 neighbors
            for d, (dx, dy, dz) in self.DELTAS.items():
                # If there is a wall in this direction, we cannot pass
                if cell.walls[d]:
                    continue

                nx, ny, nz = x + dx, y + dy, z + dz

                # If neighbor is valid and not visited, add to queue
                if self.in_bounds(nx, ny, nz) and (nx, ny, nz) not in visited:
                    visited.add((nx, ny, nz))
                    queue.append((nx, ny, nz))

        return (self.W * self.H * self.D) - len(visited)

    def count_unreachable_chambers(self):
        sx, sy, sz = self.start
        if not self.in_bounds(sx, sy, sz):
            raise ValueError(f"start {self.start} is out of bounds")
        visited = {(sx, sy, sz)}
        queue = deque([(sx, sy, sz)])

        while queue:
            x, y, z = queue.popleft()
            cell = self.grid[x][y][z]

            for d, (dx, dy, dz) in self.DELTAS.items():
                if cell.walls[d]:
                    continue

                nx, ny, nz = x + dx, y + dy, z + dz
                if self.in_bounds(nx, ny, nz) and (nx, ny, nz) not in visited:
                    visited.add((nx, ny, nz))
                    queue.append((nx, ny, nz))

        return (self.W * self.H * self.D) - len(visited)

    def is_fully_reachable(self):
        return self.count_unreachable_chambers() == 0

    def non_existing_walls(self):
        walls = []
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    cell = self.grid[x][y][z]
                    # We only iterate positive directions to list every internal edge exactly once
                    for d in ["xp", "yp", "zp"]:
                        dx, dy, dz = self.DELTAS[d]
                        # Check bounds to ensure we don't list grid borders as wall candidates
                        if self.in_bounds(x + dx, y + dy, z + dz) and not cell.walls[d]:
                            walls.append((x, y, z, d))
        return walls

    def existing_walls(self):
        walls = []
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    cell = self.grid[x][y][z]
                    for d in ["xp", "yp", "zp"]:
                        dx, dy, dz = self.DELTAS[d]
                        if self.in_bounds(x + dx, y + dy, z + dz) and cell.walls[d]:
                            walls.append((x, y, z, d))
        return walls

    def count_walls(self):
        return len(self.existing_walls())

    def get_face_vertices(self, x, y, z, d):
        if d == "xp":
            return [(x + 1, y, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x + 1, y, z + 1)]
        if d == "yp":
            return [(x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]
        if d == "zp":
            return [(x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]

    def draw_with_dual_graph(self, show=True, filename='maze_dual.png'):
        fig = plt.figure(figsize=(16, 7))

        # === LEFT SUBPLOT: Maze walls (3D) ===
        ax1 = fig.add_subplot(121, projection='3d')

        for x, y, z, d in self.existing_walls():
            verts = self.get_face_vertices(x, y, z, d)
            ax1.add_collection3d(Poly3DCollection([verts], alpha=0.6, edgecolor='k'))

        ax1.set_xlim(0, self.W)
        ax1.set_ylim(0, self.H)
        ax1.set_zlim(0, self.D)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title(f'Maze Walls (w={self.count_walls()})')
        ax1.view_init(elev=20, azim=45)

        # === RIGHT SUBPLOT: Dual graph (2D) ===
        ax2 = fig.add_subplot(122)

        # Build the graph
        G = nx.Graph()

        # Add nodes and edges
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    node_id = (x, y, z)
                    G.add_node(node_id)

                    cell = self.grid[x][y][z]
                    for d in ["xp", "yp", "zp"]:
                        if not cell.walls[d]:
                            dx, dy, dz = self.DELTAS[d]
                            nx_coord, ny_coord, nz_coord = x + dx, y + dy, z + dz
                            if self.in_bounds(nx_coord, ny_coord, nz_coord):
                                neighbor_id = (nx_coord, ny_coord, nz_coord)
                                if not G.has_edge(node_id, neighbor_id):
                                    G.add_edge(node_id, neighbor_id)

        # Simple 2D layout
        pos = nx.spring_layout(G, seed=42)

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='gray', alpha=0.5, width=1)

        # Draw all nodes
        nx.draw_networkx_nodes(G, pos, ax=ax2, node_color='steelblue', node_size=100, alpha=0.8)

        # Highlight start node
        start_node = self.start
        nx.draw_networkx_nodes(G, pos, nodelist=[start_node], ax=ax2,
                               node_color='red', node_size=200, edgecolors='darkred', linewidths=2)

        # Calculate stats
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        connected = nx.is_connected(G)

        ax2.set_title(f'Dual Graph\n|V|={num_nodes}, |E|={num_edges}, connected={connected}')
        ax2.axis('off')

        plt.tight_layout()

        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')

        if show:
            plt.show()

        return fig, ax1, ax2
