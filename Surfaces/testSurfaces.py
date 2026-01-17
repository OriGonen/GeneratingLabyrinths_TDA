from MazeSurface import *

from GenerationSurfaces import general_method_a, general_method_b, general_method_c

W, H = 20, 20

# Method A
torus_a = build_torus_complex(W, H)
force_torus_generators(torus_a, W, H)
general_method_a(torus_a, wall_num=-1, boundary_function=torus_boundary_cells)
torus_a.draw(show_wrap_edges=True, name="torus_method_a")

# Method B - NEW torus
torus_b = build_torus_complex(W, H)
force_torus_generators(torus_b, W, H)
general_method_b(torus_b, wall_num=-1, boundary_function=torus_boundary_cells, constrained=True)
torus_b.draw(show_wrap_edges=True, name="torus_method_b")

# Method C - NEW torus
torus_c = build_torus_complex(W, H)
force_torus_generators(torus_c, W, H)
general_method_c(torus_c, boundary_function=torus_boundary_cells)
torus_c.draw(show_wrap_edges=True, name="torus_method_c")