from MazeSurface import *

from GenerationSurfaces import general_method_a, general_method_b, general_method_c

W, H = 20, 20
stype = "torus"
torus_a = build_torus_complex(W, H)
force_torus_generators(torus_a, W, H)
general_method_a(torus_a, wall_num=-1, boundary_function=torus_boundary_cells)
torus_a.draw(name=f"images/{stype}_method_a",method="A")

torus_b = build_torus_complex(W, H)
force_torus_generators(torus_b, W, H)
general_method_b(torus_b, wall_num=-1, boundary_function=torus_boundary_cells)
torus_b.draw(name=f"images/{stype}_method_b", method="B")

torus_c = build_torus_complex(W, H)
force_torus_generators(torus_c, W, H)
general_method_c(torus_c, boundary_function=torus_boundary_cells)
torus_c.draw(name=f"images/{stype}_method_c",method="C")

stype = "klein"
klein_a = build_klein_complex(W, H)
force_klein_generators(klein_a, W, H)
general_method_a(klein_a, wall_num=-1, boundary_function=klein_boundary_cells)
klein_a.draw(name=f"images/{stype}_method_a",method="A")

klein_b = build_klein_complex(W, H)
force_klein_generators(klein_b, W, H)
general_method_b(klein_b, wall_num=-1, boundary_function=klein_boundary_cells)
klein_b.draw(name=f"images/{stype}_method_b", method="B")

klein_c = build_klein_complex(W, H)
force_klein_generators(klein_c, W, H)
general_method_c(klein_c, boundary_function=klein_boundary_cells)
klein_c.draw(name=f"images/{stype}_method_c",method="C")