from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, node1, node2):
        self.graph[node1].append(node2)

    def dfs(self, root):
        self.visited = [False] * len(self.graph)
        self.visited[root] = True
        self._helper(root)
        print('end')

    def _helper(self, node):
        print(node, end=' -> ')
        self.visited[node] = True
        for i in self.graph[node]:
            if not self.visited[i]:
                self._helper(i)


if __name__ == '__main__':
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)

    print ("Following is Depth First Traversal"
                  " (starting from vertex 2)")
    g.dfs(2)
