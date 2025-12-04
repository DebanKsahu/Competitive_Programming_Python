class Multiset:
    class _Node:
        __slots__ = ("key", "count", "height", "left", "right")
        def __init__(self, key):
            self.key = key
            self.count = 1
            self.height = 1
            self.left = None
            self.right = None
 
    def __init__(self):
        self.root = None
 
    # ----------------------- Internal Helper Methods ----------------------- #
    def _height(self, node):
        return node.height if node else 0
 
    def _update_height(self, node):
        node.height = max(self._height(node.left), self._height(node.right)) + 1
 
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)
 
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x
 
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y
 
    def _balance(self, node):
        self._update_height(node)
        bf = self._balance_factor(node)
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node
 
    # ----------------------- Insertion ----------------------- #
    def _insert(self, node, key):
        if not node:
            return self._Node(key)
        if key == node.key:
            node.count += 1
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return self._balance(node)
 
    def add(self, key):
        self.root = self._insert(self.root, key)
 
    # ----------------------- Deletion ----------------------- #
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
 
    def _delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.count > 1:
                node.count -= 1
                return node
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            temp = self._find_min(node.right)
            node.key = temp.key
            node.count = temp.count
            temp.count = 1 
            node.right = self._delete(node.right, temp.key)
        return self._balance(node) if node else None
 
    def remove(self, key):
        if not self.__contains__(key):
            raise KeyError(f"{key} not found in multiset")
        self.root = self._delete(self.root, key)
 
    # ----------------------- Search / Count ----------------------- #
    def _search(self, node, key):
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None
 
    def count(self, key):
        node = self._search(self.root, key)
        return node.count if node else 0
 
    def __contains__(self, key):
        return self._search(self.root, key) is not None

    # ----------------------- Min/Max ----------------------- #
    def _max_node(self, node):
        while node and node.right:
            node = node.right
        return node

    def _min_node(self, node):
        while node and node.left:
            node = node.left
        return node

    def max(self):
        node = self._max_node(self.root)
        return node.key if node else None

    def min(self):
        node = self._min_node(self.root)
        return node.key if node else None
 
    # ----------------------- Lower / Upper Bound ----------------------- #
    def _lower_bound(self, node, key):
        res = None
        while node:
            if node.key >= key:
                res = node
                node = node.left
            else:
                node = node.right
        return res
 
    def lower_bound(self, key):
        node = self._lower_bound(self.root, key)
        return node.key if node else None
 
    def _upper_bound(self, node, key):
        res = None
        while node:
            if node.key > key:
                res = node
                node = node.left
            else:
                node = node.right
        return res
 
    def upper_bound(self, key):
        node = self._upper_bound(self.root, key)
        return node.key if node else None
 
    def _floor_bound(self, node, key):
        res = None
        while node:
            if node.key < key:
                res = node       # candidate
                node = node.right
            else:
                node = node.left
        return res
 
    def floor_bound(self, key):
        node = self._floor_bound(self.root, key)
        return node.key if node else None
 
    # ----------------------- Iteration / Representation ----------------------- #
    def __iter__(self):
        yield from self._inorder(self.root)
 
    def _inorder(self, node):
        if not node:
            return
        yield from self._inorder(node.left)
        for _ in range(node.count):
            yield node.key
        yield from self._inorder(node.right)
 
    def __repr__(self):
        return "Multiset([" + ", ".join(map(str, self)) + "])"

    # ----------------------- Length ----------------------- #
    def _size(self, node):
        if not node:
            return 0
        return node.count + self._size(node.left) + self._size(node.right)

    def __len__(self):
        return self._size(self.root)