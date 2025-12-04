import heapq
from sys import stdout
from bisect import bisect_left, bisect_right
import builtins
import math
import os
import sys
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from io import BytesIO, IOBase, StringIO
 
BUFSIZE = 1 << 20  # 1 MB buffer
 
 
class FastIO(IOBase):
    def __init__(self, fd):
        self._fd = fd
        self.buffer = BytesIO()
        self.writable = fd == 1  # type: ignore
        self.ptr = 0
 
    def read(self):
        while True:
            b = os.read(self._fd, BUFSIZE)
            if not b:
                break
            self.buffer.seek(0, 2), self.buffer.write(b)
        return self.buffer.getvalue()
 
    def readline(self):  # type: ignore
        while True:
            i = self.buffer.getvalue().find(b"\n", self.ptr)
            if i >= 0:
                i += 1
                line = self.buffer.getvalue()[self.ptr : i]
                self.ptr = i
                return line
            b = os.read(self._fd, BUFSIZE)
            if not b:
                line = self.buffer.getvalue()[self.ptr :]
                self.ptr = len(self.buffer.getvalue())
                return line
            self.buffer.seek(0, 2), self.buffer.write(b)
 
    def flush(self):
        if self.writable:  # type: ignore
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
 
 
class IOWrapper(IOBase):
    def __init__(self, fd):
        self.buffer = FastIO(fd)
        self.read = lambda: self.buffer.read().decode()
        self.readline = lambda: self.buffer.readline().decode()  # type: ignore
        self.write = lambda s: self.buffer.buffer.write(s.encode())
        self.flush = self.buffer.flush  # type: ignore
 
 
sys.stdin, _ = IOWrapper(0), IOWrapper(1)
def input():
    return sys.stdin.readline().rstrip("\n")
def print(*args, sep=' ', end='\n', flush=False):
    s = sep.join(map(str, args)) + end
    sys.stdout.write(s)
    if flush:
        sys.stdout.flush()
mod = 998244353

def main():
    t = int(input())
    for testCase in range(t):
        n = int(input())
        arr = tuple(map(int,input().split()))
        mapp = defaultdict(int)
        for i in range(2*n):
            mapp[arr[i]]+=1
        count=0
        evenCount = 0
        oddCount = 0
        for key,value in mapp.items():
            if value%2==0:
                if (value//2)%2!=0:
                    count+=2
                else:
                    evenCount+=1
            else:
                oddCount+=1
                count+=1
        if evenCount>0:
            if evenCount>1:
                count+=2*evenCount
            else:
                if oddCount>0:
                    count+=2

        print(count)

        

if __name__ == "__main__":
    main()
