
from collections import defaultdict
from heapq import heappop, heappush

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def printer(grid, nrows, ncols):
    for r in range(nrows):
        print(''.join(grid[r]))

def djikstra(grid, nrows, ncols):
    item = [0, (0, 0)]
    queue = []
    heappush(queue, item)
    visited = {}
    parents = defaultdict(set)

    while queue:
        cost, (r, c) = heappop(queue)

        visited[(r, c)] = cost

        if r == nrows - 1 and c == ncols - 1:
            print('Reached the end')
            break

        for d in directions:
            dr = r + d[0]
            dc = c + d[1]

            if dr < 0 or dr >= nrows or dc < 0 or dc >= ncols:
                continue

            if grid[dr][dc] == '#':
                continue

            if (dr, dc) in visited and visited[(dr, dc)] <= cost + 1:
                continue

            visited[(dr, dc)] = cost + 1
            parents[(dr, dc)].add((r, c))
            heappush(queue, [cost + 1, (dr, dc)])

    i = 0
    states = [(nrows - 1, ncols - 1)]
    while states:
        state = states.pop()
        grid[state[0]][state[1]] = 'O'
        i += 1

        for parent in parents[state]:
            states.append(parent)

    print(i - 1)

def main():
    grid = [['.' for _ in range(71)] for _ in range(71)]
    file = open('input.txt', 'r')
    i = 0
    for line in file:
        if i == 2960:
            break
        i += 1
        line = line.strip()
        lc = [int(l) for l in line.split(',')]
        grid[lc[1]][lc[0]] = '#'
    file.close()

    nrows = len(grid)
    ncols = len(grid[0])
    print(nrows, ncols)
    djikstra(grid, nrows, ncols)
    printer(grid, nrows, ncols)

if __name__ == '__main__':
    main()