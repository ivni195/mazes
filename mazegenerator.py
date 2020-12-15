import numpy as np
from graph import Graph


class Maze:
    WALL = [0, 0, 0]
    PATH = [255, 255, 255]

    def __init__(self, size, auto_init=True):
        self.size = size
        self.doors = [[0, 1], [size - 1, size - 2]]

        self.start = (0, 1)
        self.destination = (size - 1, size - 2)

        self.maze = np.empty(size * size * 3, dtype=int).reshape(size, size, 3)
        self.maze[:] = Maze.PATH
        self.maze[0, :] = self.maze[size - 1, :] = self.maze[:, 0] = self.maze[:, size - 1] = Maze.WALL
        self.maze[0, 1] = self.maze[size - 1, size - 2] = Maze.PATH

        if auto_init:
            self.fill_maze((0, 0), (size - 1, size - 1))

        self.graph = Graph()

    def fill_maze(self, upper_left, lower_right):
        y1, x1 = upper_left
        y2, x2 = lower_right

        if x2 - x1 <= 2 or y2 - y1 <= 2:
            # grubość lub długość korytarza = 1 lub mniej; nic tu nie zdziałamy
            return

        # jeżeli jest szerszy niż grubszy to podziel pionowo i na odwrót
        if x2 - x1 < y2 - y1:
            if y1 + 2 <= y2 - 2:
                # omijamy miejsca, którymi zastawilibyśmy drzwi
                y_range = [y for y in range(y1 + 2, y2 - 1) if [y, x1] not in self.doors and [y, x2] not in self.doors]

                if y_range:
                    y_wall = np.random.choice(y_range)
                else:
                    return

                self.maze[y_wall, x1 + 1:x2] = Maze.WALL

                door = np.random.choice(range(x1 + 1, x2))
                self.maze[y_wall, door] = Maze.PATH

                self.doors.append([y_wall, door])

                self.fill_maze((y1, x1), (y_wall, x2))
                self.fill_maze((y_wall, x1), (y2, x2))

        else:
            if x1 + 2 <= x2 - 2:
                x_range = [x for x in range(x1 + 2, x2 - 1) if [y1, x] not in self.doors and [y2, x] not in self.doors]

                if x_range:
                    x_wall = np.random.choice(x_range)
                else:
                    return

                self.maze[y1 + 1:y2, x_wall] = Maze.WALL

                door = np.random.choice(range(y1 + 1, y2))
                self.maze[door, x_wall] = Maze.PATH

                self.doors.append([door, x_wall])

                self.fill_maze((y1, x1), (y2, x_wall))
                self.fill_maze((y1, x_wall), (y2, x2))

    def is_path(self, y, x):
        return (self.maze[y, x] == Maze.PATH).all()

    def is_wall(self, y, x):
        return (self.maze[y, x] == Maze.WALL).all()

    def count_neighbor_path(self, y, x):
        neighbors = 0
        if self.is_path(y + 1, x):
            neighbors += 1
        if self.is_path(y - 1, x):
            neighbors += 1
        if self.is_path(y, x + 1):
            neighbors += 1
        if self.is_path(y, x - 1):
            neighbors += 1
        return neighbors

    def is_corner(self, y, x):
        cycle = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if self.count_neighbor_path(y, x) == 2:
            for i in range(5):
                dx1, dy1 = cycle[i % 4]
                dx2, dy2 = cycle[(i + 1) % 4]
                if self.is_path(y + dy1, x + dx1) and self.is_path(y + dy2, x + dx2):
                    return True
        return False

    def is_wall_in_between(self, cell1, cell2):
        y1, x1 = cell1
        y2, x2 = cell2

        if y1 == y2:
            return bool(sum(self.is_wall(y1, x) for x in range(min(x1, x2), max(x1, x2))))

        elif x1 == x2:
            return bool(sum(self.is_wall(y, x1) for y in range(min(y1, y2), max(y1, y2))))

    def make_graph(self):
        self.graph.add_node(self.start)
        self.graph.add_node(self.destination)
        
        # ==========================================================
        # ZASADY WSTAWIANIA WIERZCHOŁKÓW
        # ==========================================================
        # 1. jeżeli komórka jest w narożniku
        # 2. jeżeli komórka sąsiaduje z dokładnie 1, 3 lub 4 drogami
        #   z 1 - jest to wtedy ślepy zaułek
        #   z 3 i 4 - jest to wtedy "skrzyżowanie"
        # ==========================================================
        
        for y in range(1, self.size - 1):
            for x in range(1, self.size - 1):
                if self.is_path(y, x):
                    if self.is_corner(y, x):
                        self.graph.add_node((y, x))

                    elif self.count_neighbor_path(y, x) in [1, 3, 4]:
                        self.graph.add_node((y, x))

        # listy zawierające wierzchołki posortowane względem wspólnych rzędów lub kolumn
        rows = [[(y, x) for x in range(self.size) if (y, x) in self.graph.nodes] for y in range(self.size)]
        cols = [[(y, x) for y in range(self.size) if (y, x) in self.graph.nodes] for x in range(self.size)]

        # bierzemy po dwa wierzchołki i łączymy je, jeżeli nie ma między nimi ściany
        for row in rows:
            if len(row) > 1:
                for i in range(len(row) - 1):
                    if not self.is_wall_in_between(row[i], row[i + 1]):
                        self.graph.add_edge(row[i], row[i + 1])

        for col in cols:
            if len(col) > 1:
                for i in range(len(col) - 1):
                    if not self.is_wall_in_between(col[i], col[i + 1]):
                        self.graph.add_edge(col[i], col[i + 1])

    def solve_bfs(self):
        return self.graph.shortest_path(self.start, self.destination)


if __name__ == '__main__':
    maze = Maze(10)
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 8))
    img = plt.imshow(maze.maze)
    plt.show()
