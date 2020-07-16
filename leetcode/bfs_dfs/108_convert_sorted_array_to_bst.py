# NOTES
# An inorder traversal of BST is an array in ascending order

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sortedArrayToBST(self, nums):
        if not nums:
            return None

        def helper(nums):
            if len(nums) <= 0:
                return None
            mid = len(nums)//2
            root = TreeNode(nums[mid])
            root.left = helper(nums[:mid])
            root.right = helper(nums[mid+1:])
            return root

        return helper(nums)


if __name__ == "__main__":
    solution = Solution()
    print(solution.sortedArrayToBST([-10,-3,0,5,9]))
