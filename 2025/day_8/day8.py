import heapq
from math import sqrt
from collections import defaultdict

class UnionFind:
    def __init__(self, capacity: int):
        self.parent = list(range(capacity))
        self.count = 0
        self.count_all = capacity

    def find(self, a) -> int:
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])

        return self.parent[a]

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            self.parent[root_b] = root_a
            self.count_all -= 1

        self.count += 1

    def get_count(self) -> int:
        return self.count
    
    def is_everything_connected(self):
        return self.count_all == 1

    def get_total(self):
        groups = defaultdict(int)
        for component in range(len(self.parent)):
            groups[self.find(component)] += 1

        values = sorted(groups.values())
        total = 1
        for value in values[-3:]:
            total *= value
        return total

def euclidean_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    ax, ay, az = a
    bx, by, bz = b

    d1 = (ax - bx) ** 2
    d2 = (ay - by) ** 2
    d3 = (az - bz) ** 2

    return int(sqrt(d1 + d2 + d3))

def first_solution(filename: str) -> int:
    junctions = []
    with open(filename) as file:
        for line in file:
            junctions.append(tuple([int(v) for v in line.strip().split(',')]))

    n = len(junctions)
    pq = []
    for i in range(n):
        for j in range(i + 1, n):
            heapq.heappush(pq, (euclidean_distance(junctions[i], junctions[j]), i, j))

    uf = UnionFind(n)
    while uf.get_count() != 1000:
        _, a, b = heapq.heappop(pq)
        uf.union(a, b)

    return uf.get_total()

def second_solution(filename: str) -> int:
    junctions = []
    with open(filename) as file:
        for line in file:
            junctions.append(tuple([int(v) for v in line.strip().split(',')]))

    n = len(junctions)
    pq = []
    for i in range(n):
        for j in range(i + 1, n):
            heapq.heappush(pq, (euclidean_distance(junctions[i], junctions[j]), i, j))

    uf = UnionFind(n)
    a = 0
    b = 0
    while uf.is_everything_connected() is False:
        _, a, b = heapq.heappop(pq)
        uf.union(a, b)

    return junctions[a][0] * junctions[b][0]


if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))