(**About**)
 - **Project**: Competitive_Programming_Python — a personal collection of Python templates and optimized data structures for competitive programming.
 - **Focus**: small, fast, and contest-friendly implementations that prioritize performance and clarity when solving algorithmic problems.

(**Folder Structure**)
 - **`pypy3/`**: PyPy-compatible implementations and contest templates.
	 - **`main_template.py`**: a fast I/O template and common utilities used as a starting point for contests.
	 - **`data_structures/`**: compact implementations of useful data structures optimized for contest use:
		 - `Multiset.py` — AVL-backed multiset with counts and order operations.
		 - `SortedList.py` — block-decomposed sorted list (sqrt-decomposition) with a Fenwick tree for fast indexing.
		 - `SegmentTree.py` — classic segment tree implementation for range queries and point updates.

(**Usage & Conventions**)
 - These implementations are written to be copy-pasted into contest solutions. They have minimal external dependencies (only Python standard library).
 - Type hints are used where helpful, but implementations avoid heavy object overhead so they work well under PyPy.

(**Data Structures**)

(**Multiset** (`pypy3/data_structures/Multiset.py`))
 - **What it is**: A multiset (bag) built on an AVL tree. Stores keys with counts, supports ordered queries.
 - **Complexity**: O(log n) for add/remove/search and bound operations; O(n) to iterate or build full representation.
 - **Public methods**:
	 - `add(key)`: Insert `key` (increments count if present).
	 - `remove(key)`: Remove one occurrence of `key`. Raises `KeyError` if `key` not present.
	 - `count(key) -> int`: Return how many times `key` appears.
	 - `__contains__(key) -> bool`: Membership test (supports `in`).
	 - `min() -> key | None`: Smallest key, or `None` if empty.
	 - `max() -> key | None`: Largest key, or `None` if empty.
	 - `lower_bound(key) -> key | None`: Smallest element >= `key`, or `None`.
	 - `upper_bound(key) -> key | None`: Smallest element > `key`, or `None`.
	 - `floor_bound(key) -> key | None`: Largest element < `key`, or `None`.
	 - `__iter__()`: In-order iteration yielding every element once per count.
	 - `__len__()`: Total number of elements (counts included).
 - **Notes**: Internally uses AVL rotations to keep the tree balanced. `remove` lowers count when >1 and deletes the node only when count reaches 0.
 - **Example**:
 ```python
 from pypy3.data_structures.Multiset import Multiset

 ms = Multiset()
 ms.add(5)
 ms.add(3)
 ms.add(5)
 print(ms.count(5))   # 2
 print(3 in ms)       # True
 print(ms.lower_bound(4))  # 5
 ms.remove(5)
 print(list(ms))      # [3, 5]
 ```

(**SortedList** (`pypy3/data_structures/SortedList.py`))
 - **What it is**: A sorted sequence implemented by dividing the list into blocks (micro lists) and maintaining a Fenwick tree over block sizes for fast index lookups.
 - **Complexity**: Typical operations like `insert`, `pop`, `__getitem__`, `bisect_left/right` are amortized O(sqrt(n)) due to block management; binsearch inside a block is O(log block_size).
 - **Public methods / attributes**:
	 - `insert(x)`: Insert value `x` while keeping list sorted.
	 - `pop(k=-1)`: Remove and return element at index `k` (supports negative indices).
	 - `__getitem__(k)`: Get element at index `k`.
	 - `count(x) -> int`: Number of occurrences of `x`.
	 - `__contains__(x) -> bool`: Membership test.
	 - `bisect_left(x) -> int`: Index of first element >= `x`.
	 - `bisect_right(x) -> int`: Index of first element > `x`.
	 - `discard(x)`: Remove one occurrence of `x` if present.
	 - `remove(x)`: Alias for `discard` in this implementation.
	 - `__len__()`: Number of elements.
	 - `__iter__()`: Iterate in sorted order.
 - **Notes**: The implementation keeps `micros` (blocks) and `macro` (first element of each block) to speed locating the right block. A `FenwickTree` tracks block sizes so index-based operations can be converted to (block, offset) quickly.
 - **Example**:
 ```python
 from pypy3.data_structures.SortedList import SortedList

 sl = SortedList([5,1,3])
 sl.insert(4)
 print(sl.bisect_left(3))  # index of 3
 print(sl[2])              # 3rd smallest
 sl.discard(1)
 print(len(sl))
 ```

(**SegmentTree** (`pypy3/data_structures/SegmentTree.py`))
 - **What it is**: A standard segment tree supporting point updates and range queries. This variant builds a tree to compute sums of non-negative parts in children (useful for some DP or max-sum style problems), and also supports straightforward range sums.
 - **Complexity**: O(log n) for point updates and O(log n) per range query (worst-case O(log n) with recursion over O(log n) nodes).
 - **Public methods**:
	 - `SegmentTree(n, arr)`: Constructor — `n` is length, `arr` is initial array.
	 - `update_seg_tree(tree_index, left_index, right_index, target_index, new_value)`: Update position `target_index` to `new_value` (internal recursive API used as-is in contests).
	 - `find_range_sum(tree_index, left_index, right_index, left_query_index, right_query_index) -> int`: Query sum on interval `[left_query_index, right_query_index]`.
 - **Notes**: The implementation uses a 0-based tree array with children at `2*i+1` / `2*i+2`. Typical usage is to call the public methods starting from tree root parameters `(0, 0, n-1)` for updates and queries.
 - **Example**:
 ```python
 from pypy3.data_structures.SegmentTree import SegmentTree

 arr = [1, 2, 3, -1, 5]
 st = SegmentTree(len(arr), arr)
 print(st.find_range_sum(0, 0, st.n-1, 1, 3))  # sum of arr[1:4]
 st.update_seg_tree(0, 0, st.n-1, 3, 4)       # set arr[3] = 4
 print(st.find_range_sum(0, 0, st.n-1, 1, 3))
 ```

(**Contributing / Next steps**)
 - If you add more data structures, please add a short docblock at top of the file describing its API then update this README's Data Structures section.
 - If you'd like, I can add quick unit tests or small example scripts demonstrating these classes.

---
Generated: concise documentation for `pypy3/data_structures`.
