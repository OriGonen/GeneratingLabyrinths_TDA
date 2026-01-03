from collections import deque
import matplotlib.pyplot as plt


# each cell has a boolean property for each side, whether or not it has wall
class Cell:
    def __init__(self):
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False


# class for maze
class Maze:
    def __init__(self, width, height): # creates a maze with no walls
        self.W = width
        self.H = height
        self.grid = [[Cell() for _ in range(height)] for _ in range(width)]

        # TODO: maybe remove? and if not, then do it for y as well
        # # make outter wall
        # for x in range(width):
        #     self.grid[x][0].bottom = True
        #     self.grid[x][height-1].top = True

    def is_boundary(self, x, y):
        return x == 0 or y == 0 or x == self.W - 1 or y == self.H - 1


    def add_wall(self, x, y, direction, delete=False):
        """
        (x, y) is the cell location in the maze

        direction is "Top" or "Bottom" or "Left" or "Right".
        Can also be used with "T", "B", "L", "R".
        """

        if direction.upper().startswith("T") and 0 <= y < self.H - 1:
            self.grid[x][y].top = not delete
            # to be consistent the one on top should have its bottom turned on.
            # this will be done for other checks as well, but it will not be explicitly mentioned like here
            self.grid[x][y+1].bottom = not delete
        elif direction.upper().startswith("B") and 0 < y <= self.W - 1:
            self.grid[x][y].bottom = not delete
            self.grid[x][y-1].top =not delete
        elif direction.upper().startswith("L") and 0 < x <= self.W - 1:
            self.grid[x][y].left = not delete
            self.grid[x-1][y].right = not delete
        elif direction.upper().startswith("R") and 0 <= x < self.W - 1:
            self.grid[x][y].right = not delete
            self.grid[x+1][y].left = not delete
        else:
            return

    # count unreachable chambers
    def count_unreachable_chambers(self, from_origin=None):
        visited = {(0, 0)}
        queue = deque([(0, 0)])

        if from_origin is None: # add all boundary points
            for x in range(self.W):
                for y in range(self.H):
                    if self.is_boundary(x, y):
                        visited.add((x, y))
                        queue.append((x, y))

        # go over until queue is empty
        while queue:
            x, y = queue.popleft()
            cell = self.grid[x][y]

            ### now, we check adjacent cells
            to_check = []
            # up
            if y<self.H-1 and not cell.top:
                to_check.append((x, y+1))
            # down
            if y>0 and not cell.bottom:
                to_check.append((x, y-1))
            # right
            if x<self.W-1 and not cell.right:
                to_check.append((x+1, y))
            # left
            if x>0 and not cell.left:
                to_check.append((x-1, y))

            # now check all the cells needed to check
            for (nx, ny) in to_check:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append( (nx, ny) )

        # count the unreachable chambers
        return self.W*self.H - len(visited)



    # function to check if every tile is reachable (i.e., there are no unreachable chambers)
    def is_fully_reachable(self):
        return self.count_unreachable_chambers() == 0

    # count the number of walls
    def count_walls(self):
        # since we want to avoid duplicates, we count only rights and tops (except boundaries)
        wall_count = 0

        for x in range(self.W):
            for y in range(self.H):
                cell = self.grid[x][y]

                # count top walls
                if cell.top:
                    wall_count += 1
                # count right walls
                if cell.right:
                    wall_count += 1

                # bottom row
                if y == 0 and cell.bottom:
                    wall_count += 1
                # left-most column
                if x == 0 and cell.left:
                    wall_count += 1

        return wall_count


    def draw(self):
        fig, ax = plt.subplots()

        for x in range(self.W):
            for y in range(self.H):
                cell = self.grid[x][y]

                # draw the walls that surround this cell
                if cell.top:
                    ax.plot([x,x+1],[y+1,y+1], 'k')
                if cell.bottom:
                    ax.plot([x, x + 1], [y, y], 'k')
                if cell.right:
                    ax.plot([x+1,x+1],[y+1,y], 'k')
                if cell.left:
                    ax.plot([x,x],[y+1,y], 'k')

        ax.set_aspect("equal")
        ax.set_xlim(0, self.W)
        ax.set_ylim(0, self.H)
        ax.set_xticks(range(self.W + 1))
        ax.set_yticks(range(self.H + 1))
        ax.grid(True)
        plt.show()
