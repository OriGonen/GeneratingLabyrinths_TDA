import time

import numpy as np
import matplotlib.pyplot as plt
from generation import method_a, method_b

# function for comparing the number of unreachable chambers in methods a/b with respect to number of walls in each
def unreachable_chambers_comparison_ab( width=20, height=20, wall_counts=range(1, 400, 5), trials=30, max_time=20):
    results_a = []
    results_b = []


    t0 = time.time(); total = len(wall_counts)
    for i, wall_num in enumerate(wall_counts, start=1):
        # progress printing:
        elapsed = time.time() - t0
        percent = i / total * 100

        print(
            f"\rProgress: {percent:6.2f}% | "
            f"{i}/{total} | "
            f"Elapsed: {elapsed:6.1f}s",
            end="",
            flush=True
        )
        ######################################


        unreachable_a = []
        unreachable_b = []

        # we will do this number of trials for the wall number and then average the results
        for _ in range(trials):
            maze_a, count = method_a(width, height, constrained=False, wall_num=wall_num, max_time=max_time)
            assert count == wall_num
            unreachable_a.append(maze_a.count_unreachable_chambers())

            maze_b, count = method_b(width, height, constrained=False, wall_num=wall_num, max_time=max_time)
            assert count == wall_num
            unreachable_b.append(maze_b.count_unreachable_chambers())

        results_a.append(np.mean(unreachable_a))
        results_b.append(np.mean(unreachable_b))

    return wall_counts, results_a, results_b

# function for plotting the results
def plot_comparison(walls, avg_a, avg_b, width=20, height=20, trials=50):
    plt.figure(figsize=(8, 5))

    plt.plot(walls, avg_a, label="method (a): random edge addition", marker="o")
    plt.plot(walls, avg_b, label="method (b): random walk on 1-skeleton", marker="s")

    plt.xlabel("walls")
    plt.ylabel("unreachable chambers")
    plt.title(
        "Unreachable chambers vs. added walls (constrained mode)\n"
        f"Maze size: {width} × {height}, trials for averaging: {trials}",
        fontsize=12
    )
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    file_name = f"{width}_{height}_constrained_analysis.svg"
    plt.savefig(file_name)



if __name__ == '__main__':
    width=20
    height=20
    trials=50
    max_walls= 760
    walls, res_a, res_b = unreachable_chambers_comparison_ab(width=width, height=height, wall_counts=range(1, max_walls, 5), trials=trials, max_time=100)
    plot_comparison(walls, res_a, res_b, width=width, height=height, trials=trials)

    width = 30
    height = 30
    trials = 50
    max_walls = 1740
    walls, res_a, res_b = unreachable_chambers_comparison_ab(width=width, height=height,
                                                             wall_counts=range(1, max_walls, 10), trials=trials,
                                                             max_time=200)
    plot_comparison(walls, res_a, res_b, width=width, height=height, trials=trials)
