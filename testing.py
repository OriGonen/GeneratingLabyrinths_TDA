from Maze import Maze

maze = Maze(4, 4)

maze.add_wall(1, 1, "top")
maze.add_wall(1, 1, "left")
maze.add_wall(1, 1, "bottom")

maze.draw()
# still reachable

# maze.add_wall(1, 1, "right")  # closes the cycle
# maze.draw()
