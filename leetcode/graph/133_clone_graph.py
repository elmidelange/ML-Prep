"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        return self._dfs(node)

    def _dfs(self, node, visited={}):
        if node in visited:
            return visited[node]
        new_node = Node(node.val)
        visited[node] = new_node
        for n in node.neighbors:
            new_node.neighbors.append(self._dfs(n))
        return new_node


class Solution:     def cloneGraph(self, node: 'Node') -> 'Node':         if not node:             return None         queue=[node]         visited=dict()         visited[node]=Node(node.val,[])         while queue:             current=queue.pop(0)             for x in current.neighbors:                 if x not in visited:                     visited[x]=Node(x.val,[])                     queue.append(x)                 visited[current].neighbors.append(visited[x])          return visited[node]
