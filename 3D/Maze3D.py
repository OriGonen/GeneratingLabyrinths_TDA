from collections import deque


class Cell3D:
    def __init__(self):
        # each cell contains 6 faces, represented by bools indicating if a wall exists
        # n is negative (smaller coordinate), p is positive (larger coordinate)
        self.walls = {"xp": False, "xn": False, "yp": False, "yn": False, "zp": False, "zn": False}


class Maze3D:
    OPPOSITES = {"xp": "xn", "xn": "xp", "yp": "yn", "yn": "yp", "zp": "zn", "zn": "zp"}
    DELTAS = {"xp": (1, 0, 0), "xn": (-1, 0, 0), "yp": (0, 1, 0), "yn": (0, -1, 0), "zp": (0, 0, 1), "zn": (0, 0, -1)}

    def __init__(self, W, H, D):
        # Create a grid of WxHxD cells
        self.W, self.H, self.D = W, H, D
        self.grid = [[[Cell3D() for _ in range(D)] for _ in range(H)] for _ in range(W)]

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

    def count_unreachable_chambers(self):
        # BFS to find all cells reachable from the boundary
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
                        if self.in_bounds(x+dx, y+dy, z+dz) and cell.walls[d]:
                            walls.append((x, y, z, d))
        return walls

    def count_walls(self):
        return len(self.existing_walls())