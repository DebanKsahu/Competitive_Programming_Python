from bisect import bisect_left, bisect_right


class FenwickTree:
    def __init__(self, x):
        bit = self.bit = list(x)
        size = self.size = len(bit)
        for i in range(size):
            j = i | (i + 1)
            if j < size:
                bit[j] += bit[i]

    def update(self, idx, x):
        while idx < self.size:
            self.bit[idx] += x
            idx |= idx + 1

    def __call__(self, end):
        s = 0
        while end:
            s += self.bit[end - 1]
            end &= end - 1
        return s

    def find_kth(self, k):
        idx = -1
        for d in reversed(range(self.size.bit_length())):
            right_idx = idx + (1 << d)
            if right_idx < self.size and self.bit[right_idx] <= k:
                idx = right_idx
                k -= self.bit[idx]
        return idx + 1, k


class SortedList:
    block_size = 700

    def __init__(self, iterable=()):
        iterable = sorted(iterable)
        self.micros = [
            iterable[i : i + self.block_size - 1]
            for i in range(0, len(iterable), self.block_size - 1)
        ] or [[]]
        self.macro = [m[0] for m in self.micros[1:] if m]
        self.micro_size = [len(m) for m in self.micros]
        self.fenwick = FenwickTree(self.micro_size)
        self.size = len(iterable)

    # ---------- helpers ----------
    def _rebuild_macro(self):
        self.macro = [m[0] for m in self.micros[1:] if m]

    def _rebuild_fenwick(self):
        self.fenwick = FenwickTree(self.micro_size)

    def _delete_block(self, i):
        self.micros.pop(i)
        self.micro_size.pop(i)

        if self.micros:
            self._rebuild_macro()
        else:
            self.micros = [[]]
            self.micro_size = [0]
            self.macro = []

        self._rebuild_fenwick()

    def _rebalance(self, i):
        if i + 1 < len(self.micros):
            self.micros[i].extend(self.micros[i + 1])
            self.micro_size[i] += self.micro_size[i + 1]
            self._delete_block(i + 1)

            if self.micro_size[i] >= self.block_size:
                mid = self.micro_size[i] >> 1
                new_block = self.micros[i][mid:]
                left_block = self.micros[i][:mid]

                self.micros[i] = left_block
                self.micros.insert(i + 1, new_block)

                self.micro_size[i] = len(left_block)
                self.micro_size.insert(i + 1, len(new_block))

                self._rebuild_macro()
                self._rebuild_fenwick()

    # ---------- core operations ----------
    def insert(self, x):
        i = bisect_left(self.macro, x)

        if i >= len(self.micros):
            i = len(self.micros) - 1

        j = bisect_right(self.micros[i], x)
        self.micros[i].insert(j, x)

        self.size += 1
        self.micro_size[i] += 1
        self.fenwick.update(i, 1)

        if len(self.micros[i]) >= self.block_size:
            mid = self.block_size >> 1
            left = self.micros[i][:mid]
            right = self.micros[i][mid:]

            self.micros[i] = left
            self.micros.insert(i + 1, right)

            self.micro_size[i] = len(left)
            self.micro_size.insert(i + 1, len(right))

            self._rebuild_macro()
            self._rebuild_fenwick()

    def pop(self, k=-1):
        i, j = self._find_kth(k)
        self.size -= 1
        self.micro_size[i] -= 1
        self.fenwick.update(i, -1)
        val = self.micros[i].pop(j)

        if self.micro_size[i] == 0:
            self._delete_block(i)
        elif self.micro_size[i] < (self.block_size >> 2):
            self._rebalance(i)

        return val

    def __getitem__(self, k):
        i, j = self._find_kth(k)
        return self.micros[i][j]

    def count(self, x):
        return self.bisect_right(x) - self.bisect_left(x)

    def __contains__(self, x):
        return self.count(x) > 0

    def bisect_left(self, x):
        i = bisect_left(self.macro, x)
        if i >= len(self.micros):
            i = len(self.micros) - 1
        return self.fenwick(i) + bisect_left(self.micros[i], x)

    def bisect_right(self, x):
        i = bisect_right(self.macro, x)
        if i >= len(self.micros):
            i = len(self.micros) - 1
        return self.fenwick(i) + bisect_right(self.micros[i], x)

    def _find_kth(self, k):
        if k < 0:
            k = k + self.size
        if not (0 <= k < self.size):
            raise IndexError("list index out of range")
        return self.fenwick.find_kth(k)

    def __len__(self):
        return self.size

    def __iter__(self):
        return (x for micro in self.micros for x in micro)

    def __repr__(self):
        return str(list(self))

    # ---------- remove / discard ----------
    def discard(self, x):
        i = bisect_left(self.macro, x)
        if i >= len(self.micros):
            i = len(self.micros) - 1

        j = bisect_left(self.micros[i], x)
        if j == len(self.micros[i]) or self.micros[i][j] != x:
            return

        self.micros[i].pop(j)
        self.size -= 1
        self.micro_size[i] -= 1
        self.fenwick.update(i, -1)

        if self.micro_size[i] == 0:
            self._delete_block(i)
        elif self.micro_size[i] < (self.block_size >> 2):
            self._rebalance(i)

    def remove(self, x):
        i = bisect_left(self.macro, x)
        if i >= len(self.micros):
            i = len(self.micros) - 1

        j = bisect_left(self.micros[i], x)
        if j == len(self.micros[i]) or self.micros[i][j] != x:
            return

        self.discard(x)
