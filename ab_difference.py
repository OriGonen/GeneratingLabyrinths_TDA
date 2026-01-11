import matplotlib.pyplot as plt
from generation import method_a, method_b

# to compare how method a and method b look like in constrained mode
def compare_methods(width=10, height=10, wall_nums=(20, 40, 60)):
    fig, axes = plt.subplots(
        nrows=3,
        ncols=2,
        figsize=(10, 15)
    )

    for row, wall_num in enumerate(wall_nums):
        maze_a, wa = method_a(
            width=width,
            height=height,
            constrained=True,
            wall_num=wall_num
        )

        ax = axes[row, 0]
        draw_maze_on_ax(maze_a, ax)
        ax.set_title(f"Method A: walls={wa}")

        maze_b, wb = method_b(
            width=width,
            height=height,
            constrained=True,
            wall_num=wall_num
        )

        ax = axes[row, 1]
        draw_maze_on_ax(maze_b, ax)
        ax.set_title(f"Method B: walls={wb}")

    plt.tight_layout()
    plt.savefig("ab_constrained.svg")
    plt.show()


# helper function to draw on an axes
def draw_maze_on_ax(maze, ax):
    for x in range(maze.W):
        for y in range(maze.H):
            cell = maze.grid[x][y]

            if cell.top:
                ax.plot([x, x+1], [y+1, y+1], 'k')
            if cell.bottom:
                ax.plot([x, x+1], [y, y], 'k')
            if cell.right:
                ax.plot([x+1, x+1], [y, y+1], 'k')
            if cell.left:
                ax.plot([x, x], [y, y+1], 'k')

    ax.set_aspect("equal")
    ax.set_xlim(0, maze.W)
    ax.set_ylim(0, maze.H)
    ax.set_xticks([])
    ax.set_yticks([])



if __name__ == "__main__":
    compare_methods(
        width=20,
        height=20,
        wall_nums=(40, 260, 420)
    )
