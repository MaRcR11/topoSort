from collections import deque

class Graph:
    def __init__(self, edges):

        self.isNotNumeric = False

        self.N = len(set(sum(edges, ())))

        if not all(isinstance(elem, int) for tup in edges for elem in tup):
            self.isNotNumeric = True

            self.node_dict = {
                node: i
                for i, node in enumerate(
                    sorted(set([node for edge in edges for node in edge]))
                )
            }

            self.result = [
                (self.node_dict[edge[0]], self.node_dict[edge[1]]) for edge in edges
            ]

            edges = self.result

        self.adjList = [set() for _ in range(self.N)]
        self.indegree = [0] * self.N

        for src, dest in edges:
            self.adjList[src].add(dest)

            self.indegree[dest] += 1

    def is_cyclic(self):

        indegree_copy = self.indegree[:]

        queue = deque([i for i in range(len(self.adjList)) if not indegree_copy[i]])

        visited_nodes = 0

        while queue:

            node = queue.popleft()
            visited_nodes += 1

            for neighbor in self.adjList[node]:

                indegree_copy[neighbor] -= 1

                if not indegree_copy[neighbor]:
                    queue.append(neighbor)

        return visited_nodes != len(self.adjList)

def find_all_topological_orders(graph, path, N, result):

    if len(path) == N:

        result.append(", ".join(str(v) for v in path))
        return

    for v in range(N):

        if graph.indegree[v] == 0 and v not in path:
            for u in graph.adjList[v]:
                graph.indegree[u] -= 1

            path.append(v)

            find_all_topological_orders(graph, path, N, result)

            path.pop()

            for u in graph.adjList[v]:

                graph.indegree[u] += 1

def print_all_topological_orders(graph):

    path = deque()

    result = []

    find_all_topological_orders(graph, path, graph.N, result)

    if graph.isNotNumeric:

        result = [list(map(int, s.split(","))) for s in result]
        result = [
            ", ".join(list(graph.node_dict.keys())[v] for v in path) for path in result
        ]

    print(
        f"All topological sorts ({len(result)}) of the acyclic graph (number of nodes N = {graph.N}, number of edges M = {len(edges)}):"
    )

    print("\n".join(result))

if __name__ == "__main__":
    # input for edges as a string or from consecutive natural numbers starting from 0

    edges = [
        ("A", "D"),
        ("B", "C"),
        ("B", "I"),
        ("E", "C"),
        ("E", "I"),
        ("E", "A"),
        ("E", "F"),
        ("F", "C"),
        ("F", "D"),
        ("F", "A"),
        ("F", "B"),
        ("H", "B"),
        ("H", "D"),
        ("H", "I"),
        ("I", "D"),
    ]

    graph = Graph(edges)

    is_cyclic = graph.is_cyclic()

    if is_cyclic:
        print(
            f"graph is cyclic (number of nodes N = {graph.N}, number of edges M = {len(edges)}).",
        )
    else:
        print_all_topological_orders(graph)
