from Maze import Maze
from generation import method_a, method_b, method_c, general_method_a
from CellComplex import build_klein_complex, build_torus_complex, CellComplex


# complex = build_klein_complex(20,20)
#
# maze = general_method_a(complex, 260, constrained=False)
#
# maze.draw(show_wrap_edges=True, name="klein_example")

complex = build_torus_complex(20,20)

maze = general_method_a(complex, 260, constrained=False)

maze.draw(show_wrap_edges=True, name="torus_example")





# maze, num = method_a(20, 20, constrained=False, wall_num=200)
# maze, num = method_c(10, 10)
# print(num)
# print(maze.is_fully_reachable())
# print(f"unreachable chambers: {maze.count_unreachable_chambers()}")
# maze.draw()
# print(maze.count_walls()+ len(maze.non_existing_walls()) )
# print(20*20*2 + 20 + 20)







# maze = Maze(4, 4, full=True)
# maze.vertex_add_wall((1,4), (2,4))
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
