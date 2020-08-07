from collections import defaultdict, deque
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, node1, node2):
        self.graph[node1].append(node2)

    def bfs(self, root):
        visited = [False] * len(self.graph)
        q = deque([root])
        visited[root] = True
        while q:
            node = q.popleft()
            print(node, end=' -> ')
            for i in self.graph[node]:
                if not visited[i]:
                    q.append(i)
                    visited[i] = True
        print('end')


if __name__ == '__main__':
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)

    print ("Following is Breadth First Traversal"
                  " (starting from vertex 2)")
    g.bfs(2)
