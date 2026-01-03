from Maze import Maze
from generation import method_a


maze, num = method_a(20, 20, constrained=True, wall_num=300)
print(num)
print(maze.is_fully_reachable())
print(f"unreachable chambers: {maze.count_unreachable_chambers()}")
maze.draw()






# maze = Maze(4, 4)
#
# maze.add_wall(1, 1, "T")
# maze.add_wall(1, 1, "L")
# maze.add_wall(1, 1, "B")
#
# print(maze.is_fully_reachable())
# maze.draw()
# # still reachable
#
# maze.add_wall(1, 1, "R")  # closes the cycle
# print(maze.is_fully_reachable())
# maze.draw()
