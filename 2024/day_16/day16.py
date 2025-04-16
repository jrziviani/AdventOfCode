from collections import defaultdict
from heapq import heappush, heappop


def parse_input(filename):
    grid = []
    file = open(filename, 'r')
    for line in file:
        grid.append(list(line.strip()))
    file.close()
    return grid


def printer(grid):
    for row in grid:
        print(''.join(row))

def get_directions():
    pass

directions = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0),
}

turns_cw_ccw = {
    directions['R']: [directions['R'], directions['D'], directions['U']],
    directions['L']: [directions['L'], directions['U'], directions['D']],
    directions['D']: [directions['D'], directions['L'], directions['R']],
    directions['U']: [directions['U'], directions['R'], directions['L']],
}

def djikstra(grid, position, nrows, ncols):
    queue = []
    item = [0, directions['R'], position]
    heappush(queue, item)
    visited = {}
    parents = defaultdict(set)
    end_positions = {}

    while queue:
        cost, direction, (row, col) = heappop(queue)

        visited[(direction, row, col)] = cost

        for ndir in turns_cw_ccw[direction]:
            nr, nc = row + ndir[0], col + ndir[1]
            if nr < 0 or nc < 0 or nr >= nrows or nc >= ncols or grid[nr][nc] == '#':
                continue

            ncost = cost + (1 if ndir == direction else 1001)
            if (ndir, nr, nc) not in visited or ncost <= visited[(ndir, nr, nc)]:
                if grid[nr][nc] == 'E':
                    if (nr, nc) not in end_positions:
                        end_positions[(nr, nc)] = (ndir, ncost)
                    else:
                        _, c = end_positions[(nr, nc)]
                        if ncost < c:
                            end_positions[(nr, nc)] = (ndir, ncost)

                visited[(ndir, nr, nc)] = ncost
                parents[(ndir, nr, nc)].add((direction, row, col))
                heappush(queue, [ncost, ndir, (nr, nc)])

    path = []
    vis = defaultdict(int)
    for pos, vals in end_positions.items():
        states = [(vals[0], *pos)]
        while states:
            state = states.pop()
            _, b, c = state
            path.append(state)
            vis[(b, c)] += 1

            if state in parents:
                for parent in parents[state]:
                    states.append(parent)

        # path.reverse()
        #path.append((vals[0], *pos))

    print(f"Min cost: {end_positions}, Best seats: {len(vis)}")

    #for r in range(nrows):
    #    for c in range(ncols):
    #        if (r, c) in vis:
    #            print("o", end='')
    #        else:
    #            print(grid[r][c], end='')
    #    print()


def main():
    grid = parse_input('input.txt')
    nrows = len(grid)
    ncols = len(grid[0])
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] == 'S':
                djikstra(grid, (row, col), nrows, ncols)


if __name__ == '__main__':
    main()
