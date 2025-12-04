class SegmentTree:
    def __init__(self, n: int, arr: list[int]):
        self.n = n
        self.arr = arr[:]  # copy to avoid mutating original
        self.segTree = [0] * (4 * n)
        self._build_seg_tree(0, 0, n - 1)
 
    def _build_seg_tree(self, tree_index: int, left_index: int, right_index: int):
        if left_index > right_index:
            return
        elif left_index == right_index:
            self.segTree[tree_index] = self.arr[left_index]
            return
        else:
            mid = (left_index + right_index) // 2
            self._build_seg_tree(2 * tree_index + 1, left_index, mid)
            self._build_seg_tree(2 * tree_index + 2, mid + 1, right_index)
            self.segTree[tree_index] = max(0, self.segTree[2 * tree_index + 1]) + max(0, self.segTree[2 * tree_index + 2])
 
    def update_seg_tree(self, tree_index: int, left_index: int, right_index: int, target_index: int, new_value: int):
        if left_index == right_index:
            self.segTree[tree_index] = new_value
            self.arr[target_index] = new_value
            return
        else:
            mid = (left_index + right_index) // 2
            if target_index <= mid:
                self.update_seg_tree(2 * tree_index + 1, left_index, mid, target_index, new_value)
            else:
                self.update_seg_tree(2 * tree_index + 2, mid + 1, right_index, target_index, new_value)
            self.segTree[tree_index] = self.segTree[2 * tree_index + 1] + self.segTree[2 * tree_index + 2]
 
    def find_range_sum(self, tree_index: int, left_index: int, right_index: int, left_query_index: int, right_query_index: int) -> int:
        if left_query_index > right_index or right_query_index < left_index:
            return 0
        elif left_query_index == left_index and right_query_index == right_index:
            return self.segTree[tree_index]
        else:
            mid = (left_index + right_index) // 2
            left_sum = self.find_range_sum(
                2 * tree_index + 1,
                left_index,
                mid,
                left_query_index,
                min(right_query_index, mid)
            )
            right_sum = self.find_range_sum(
                2 * tree_index + 2,
                mid + 1,
                right_index,
                max(mid + 1, left_query_index),
                right_query_index
            )
            return left_sum + right_sum

