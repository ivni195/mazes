from collections import defaultdict


class Graph:
    def __init__(self):
        self._graph = defaultdict()

    @property
    def nodes(self):
        return self._graph.keys()

    def add_node(self, v):
        self._graph[v] = []

    def add_edge(self, v, u):
        if v in self._graph.keys():
            self._graph[v].append(u)
        else:
            self._graph[v] = [u]

        if u in self._graph.keys():
            self._graph[u].append(v)
        else:
            self._graph[u] = [v]

    def bfs(self, s):
        visited = [s]
        q = []
        q.extend(self._graph[s])

        reachable = []

        while q:
            node = q.pop()
            for neighbor in self._graph[node]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    q.append(neighbor)
                    reachable.append(neighbor)

        return reachable

    def shortest_path(self, s, d):  # start, destination
        visited = [s]
        q = []
        q.extend(self._graph[s])
        predecessors = {s: None}

        for neighbor in self._graph[s]:
            predecessors[neighbor] = s

        while q:
            node = q.pop()
            visited.append(node)

            if node == d:
                path = [node]

                while node is not None:
                    node = predecessors[node]
                    path.append(node)
                # od tyłu bez ostatniego elementu
                return path[-2::-1]

            for neighbor in self._graph[node]:
                if neighbor not in visited:
                    predecessors[neighbor] = node
                    visited.append(neighbor)
                    q.append(neighbor)


def main():
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(4, 5)
    g.add_edge(4, 6)
    print(g.shortest_path(0, 4))
    print(g._graph)


if __name__ == '__main__':
    main()
