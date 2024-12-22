from collections import defaultdict
from collections import deque

directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
names = ["DOWN", "UP", "LEFT", "RIGHT"]


def get_direction(name):
    return directions[names.index(name)]


def mark_grid(grid, visisted):
    for r, c in visisted:
        grid[r] = grid[r][:c] + "x" + grid[r][c + 1:]


def trace_sides(grid, row, col, direction, plant, visited):
    sides = set()
    for i, (dr, dc) in enumerate(directions):
        nr = row + dr
        nc = col + dc

        if nr >= 0 and nc >= 0 and nr < len(grid) and nc < len(grid[0]) and \
                ((nr, nc) in visited or grid[nr][nc] == plant):
            continue

        sides.add(names[i])

    visited[(row, col)] = sides


def get_areas(grid, row, col, direction, plant):
    visited = {}

    area = 0
    perimiter = 0
    stack = [(direction, row, col)]
    while stack:
        d, r, c = stack.pop()

        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
            continue

        if (r, c) in visited or grid[r][c] != plant:
            continue

        area += 1
        trace_sides(grid, r, c, d, plant, visited)
        perimiter += len(visited[(r, c)])

        for i in range(len(directions)):
            idx = (d + i + 1) % 4
            dr, dc = directions[idx]
            stack.append((idx, r + dr, c + dc))

    sides = 0
    queue = deque([(0,) + list(visited.keys())[0]])
    side_visited = set()
    while queue:
        d, r, c = queue.pop()

        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
            continue

        if (r, c) in side_visited or (r, c) not in visited:
            continue

        side_visited.add((r, c))

        pr, pc = directions[d]
        pr = r - pr
        pc = c - pc

        if (pr, pc) in visited:
            tmp = visited[(r, c)] - visited[(pr, pc)]
            sides += len(tmp)
        else:
            sides += len(visited[(r, c)])

        nr, nc = directions[d]
        nr = r + nr
        nc = c + nc
        if (nr, nc) in side_visited:
            for vd in visited[(r, c)]:
                if vd in visited[(nr, nc)]:
                    sides -= 1

        elif d == 1 and pr != r and pc != c - 1 and (r, c - 1) in side_visited:
            for vd in visited[(r, c)]:
                if vd in visited[(r, c - 1)]:
                    sides -= 1

        elif d == 0 and pr != r and pc != c + 1 and (r, c + 1) in side_visited:
            for vd in visited[(r, c)]:
                if vd in visited[(r, c + 1)]:
                    sides -= 1

        for i in range(len(directions)):
            idx = (d + i + 1) % 4
            dr, dc = directions[idx]
            queue.append((idx, r + dr, c + dc))

    mark_grid(grid, visited)

    return (area, perimiter, sides)


def main():
    grid = [
        "AAAAAA",
        "AAABBA",
        "AAABBA",
        "ABBAAA",
        "ABBAAA",
        "AAAAAA",
    ]

    grid = [
        "EEEEE",
        "EXXXX",
        "EEEEE",
        "EXXXX",
        "EEEEE",
    ]

    grid = [
        "AAAA",
        "BBCD",
        "BBCC",
        "EEEC",
    ]

    grid = [
        "RRRRIICCFF",
        "RRRRIICCCF",
        "VVRRRCCFFF",
        "VVRCCCJFFF",
        "VVVVCJJCFE",
        "VVIVCCJJEE",
        "VVIIICJJEE",
        "MIIIIIJJEE",
        "MIIISIJEEE",
        "MMMISSJEEE",
    ]

    file = open("example3.txt", "r")
    grid = [line.strip() for line in file.readlines()]

    NROWS = len(grid)
    NCOLS = len(grid[0])

    pi = 0
    pii = 0
    for r in range(NROWS):
        for c in range(NCOLS):
            plant = grid[r][c]
            if plant == "x":
                continue

            area, perimiter, sides = get_areas(grid, r, c, 0, plant)
            pi += area * perimiter
            pii += area * sides

    print(f"Part I: {pi}")
    print(f"Part II: {pii}")


if __name__ == "__main__":
    main()
