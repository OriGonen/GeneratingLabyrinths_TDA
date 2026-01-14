from generation3d import *

maze = Maze3D(3,3,3)
maze,num = method_a_3d(maze,maze.W,maze.H,maze.D)
maze.draw_with_dual_graph()