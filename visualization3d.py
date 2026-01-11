import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def draw_maze_3d(maze):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for x, y, z, d in maze.existing_walls():
        verts = get_face_vertices(x, y, z, d)
        ax.add_collection3d(Poly3DCollection([verts], alpha=0.6, edgecolor='k'))

    ax.set_xlim(0, maze.W)
    ax.set_ylim(0, maze.H)
    ax.set_zlim(0, maze.D)
    plt.show()


def get_face_vertices(x, y, z, d):
    if d == "xp":
        return [(x + 1, y, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x + 1, y, z + 1)]
    if d == "yp":
        return [(x, y + 1, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]
    if d == "zp":
        return [(x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1), (x, y + 1, z + 1)]