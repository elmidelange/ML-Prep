# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


# [(col, row, val), ...]

from collections import OrderedDict

class Solution:
    def verticalTraversal(self, root: TreeNode) -> List[List[int]]:
        self.order = OrderedDict()
        self._bfs(root)
        ans = []
        for key in sorted(self.order):
            val = self.order[key]
            ans.append([v[1] for v in sorted(val)])
        return ans


    def _bfs(self, node, col=0, row=0):
        if not node:
            return
        self._bfs(node.left, col-1, row+1)
        self.order[col] = self.order.get(col,[]) + [(row, node.val)]
        self._bfs(node.right, col+1, row+1)
