# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        return self._helper(root)

    def _helper(self, node):
        if node is None:
            return 0
        left_count = self._helper(node.left)
        right_count = self._helper(node.right)
        return max(left_count, right_count) + 1


if __name__ == "__main__":
    root = TreeNode(3,TreeNode(9),TreeNode(20, TreeNode(15), TreeNode(7)))
    solution = Solution()
    print(solution.maxDepth(root))
