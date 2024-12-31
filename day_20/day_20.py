
from heapq import heappop, heappush

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def djikstra(grid, row, col, nrows, ncols):
    queue = []
    visited = {}
    parents = {}
    heappush(queue, (0, row, col))
    total_cost = 0
    end_rc = None

    while queue:
        cost, r, c = heappop(queue)

        if grid[r][c] == 'E':
            end_rc = (r, c)
            total_cost = cost
            break

        for d in directions:
            dr = r + d[0]
            dc = c + d[1]

            if dr < 0 or dr >= nrows or dc < 0 or dc >= ncols:
                continue

            if grid[dr][dc] == '#':
                continue

            if (dr, dc) in visited and visited[(dr, dc)] < cost + 1:
                continue

            visited[(dr, dc)] = cost + 1
            parents[(dr, dc)] = (r, c)
            heappush(queue, (cost + 1, dr, dc))

    print('Total cost:', total_cost)

    total = 0
    memo = set()
    while end_rc != (row, col):
        r, c = end_rc
        memo.add((r, c))

        for d in directions:
            dr = r + d[0]
            dc = c + d[1]
            dnr = dr + d[0]
            dnc = dc + d[1]
            if (dr, dc) not in parents and (dnr, dnc) in parents and (dnr, dnc) not in memo:
                savings = visited[(r, c)] - visited[(dnr, dnc)] - 2
                if savings >= 100:
                    total += 1

        end_rc = parents[(r, c)]


    print('Part I:', total)

    total = 0
    memo = set()
    for path in parents.keys():
        pr, pc = path

        memo.add(path)

        for r in range(-20, 21):
            for c in range(-20, 21):
                dr = r + pr
                dc = c + pc

                distance = abs(pr - dr) + abs(pc - dc)
                if distance > 20:
                    continue

                if (dr, dc) in visited and (dr, dc) not in memo:
                    cost1 = visited[(dr, dc)]
                    cost2 = visited[path]
                    if abs(cost2 - cost1) - distance >= 100:
                        total += 1

    print(f"Part II: {total + 1}")


def printer(grid, nrows):
    for r in range(nrows):
        print(grid[r])

def main():
    grid = []
    file = open('input.txt', 'r')
    for line in file:
        grid.append(list(line.strip()))
    file.close()

    nrows = len(grid)
    ncols = len(grid[0])

    for r in  range(nrows):
        for c in range(ncols):
            if grid[r][c] == 'S':
                djikstra(grid, r, c, nrows, ncols)


if __name__ == '__main__':
    main()