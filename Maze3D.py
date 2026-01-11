from collections import deque

class Cell3D:
    def __init__(self):
        # each cell contains 6 faces, represented by bools
        # n is negative, p is positive
        self.walls = {"xp": False, "xn": False, "yp": False, "yn": False, "zp": False, "zn": False}

class Maze3D:
    OPPOSITES = {"xp": "xn", "xn": "xp", "yp": "yn", "yn": "yp", "zp": "zn", "zn": "zp"}
    DELTAS = {"xp": (1,0,0), "xn": (-1,0,0), "yp": (0,1,0), "yn": (0,-1,0), "zp": (0,0,1), "zn": (0,0,-1)}

    def __init__(self, W, H, D):
        # Create a grid of WxHxD cells
        self.W, self.H, self.D = W, H, D
        self.grid = [[[Cell3D() for _ in range(D)] for _ in range(H)] for _ in range(W)]

    # Simple bounds checking
    def in_bounds(self, x, y, z):
        return 0 <= x < self.W and 0 <= y < self.H and 0 <= z < self.D

    # Detect if a cell is a boundary cell (any of the faces is the boundary of the grid)
    def is_boundary(self, x, y, z):
        return x == 0 or y == 0 or z == 0 or x == self.W-1 or y == self.H-1 or z == self.D-1

    def add_wall(self, x, y, z, direction, delete=False):
        dx, dy, dz = self.DELTAS[direction]
        # neighboring coordinates
        nx, ny, nz = x + dx, y + dy, z + dz
        if not self.in_bounds(nx, ny, nz): # Tying to add a wall outside the grid
            return

        # We mark both walls (since these 2 cells share a wall and each has its own state for it)
        self.grid[x][y][z].walls[direction] = not delete
        self.grid[nx][ny][nz].walls[self.OPPOSITES[direction]] = not delete

    def count_unreachable_chambers(self):
        # BFS
        visited = set()
        queue = deque()

        # Initialize: all boundary cells are outside/reachable
        # Each of these is a starting point for BFS traversal
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    if self.is_boundary(x, y, z):
                        visited.add((x, y, z))
                        queue.append((x, y, z))

        while queue:
            x, y, z = queue.popleft()
            cell = self.grid[x][y][z]
            for d, (dx, dy, dz) in self.DELTAS.items():
                if cell.walls[d]:
                    continue
                # TODO: what excatly is done here?
                nb = (x + dx, y + dy, z + dz)
                if self.in_bounds(*nb) and nb not in visited:
                    visited.add(nb)
                    queue.append(nb)

        # If a cell is never visited, it is unreachable
        return self.W * self.H * self.D - len(visited)

    def is_fully_reachable(self):
        return self.count_unreachable_chambers() == 0

    def non_existing_walls(self):
        walls = []
        for x in range(self.W):
            for y in range(self.H):
                for z in range(self.D):
                    cell = self.grid[x][y][z]
                    # only positive directions to avoid duplicates
                    for d in ["xp", "yp", "zp"]:
                        dx, dy, dz = self.DELTAS[d]
                        if self.in_bounds(x+dx, y+dy, z+dz) and not cell.walls[d]:
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
                        if self.in_bounds(x+dx, y+dy, z+dz) and cell.walls[d]:
                            walls.append((x, y, z, d))
        return walls

    def count_walls(self):
        return len(self.existing_walls())