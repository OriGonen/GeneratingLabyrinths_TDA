# import matplotlib
# matplotlib.use("TkAgg")
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

    def add_wall(self, x, y, direction):
        """
        (x, y) is the cell location in the maze

        direction is "Top" or "Bottom" or "Left" or "Right".
        Can also be used with "T", "B", "L", "R".
        """

        if direction.upper().startswith("T") and 0 <= y < self.H - 1:
            self.grid[x][y].top = True
            # to be consistent the one on top should have its bottom turned on.
            # this will be done for other checks as well, but it will not be explicitly mentioned like here
            self.grid[x][y+1].bottom = True
        elif direction.upper().startswith("B") and 0 < y <= self.W - 1:
            self.grid[x][y].bottom = True
            self.grid[x][y-1].top =True
        elif direction.upper().startswith("L") and 0 < x <= self.W - 1:
            self.grid[x][y].left = True
            self.grid[x-1][y].right = True
        elif direction.upper().startswith("R") and 0 <= x < self.W - 1:
            self.grid[x][y].right = True
            self.grid[x+1][y].left = True
        else:
            raise Exception("Invalid direction")


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
