from mazegenerator import Maze
import matplotlib.pyplot as plt

m = Maze(30)
m.make_graph()

fig, ax = plt.subplots(ncols=2, figsize=(14, 7))

maze_copy = m.maze.copy()
ax[0].imshow(maze_copy)

nodes = m.solve_bfs()

for i in range(len(nodes) - 1):
    y1, x1 = nodes[i]
    y2, x2 = nodes[i + 1]
    for y in range(min(y1, y2), max(y1, y2) + 1):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            maze_copy[y, x] = [0, 255, 0]

for node in nodes:
    maze_copy[node] = [255, 0, 0]

ax[1].imshow(maze_copy)

for a in ax:
    a.grid(False)
    a.axis(False)

plt.show()
