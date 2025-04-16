import re
from collections import defaultdict

class Position:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"(row: {self.row}, col: {self.col})"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))
    
def advance(when, grid, nrows, ncols):
    grid2D = [[None for _ in range(ncols)] for _ in range(nrows)]
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] is None:
                continue

            for robot in grid[row][col]:
                next_row = (row + robot.row * when) % nrows
                next_col = (col + robot.col * when) % ncols
                if grid2D[next_row][next_col] is None:
                    grid2D[next_row][next_col] = []
                grid2D[next_row][next_col].append(robot)

    return grid2D

def printer(grid, nrows, ncols):
    for row in range(nrows):
        print(f"{row:3d} |", end="")
        for col in range(ncols):
            if grid[row][col] is None:
                print(' ', end = "")
            else:
                #print('x' * len(grid[row][col]), end = "")
                print('x', end = "")
        print("")

def has_block(grid, row, cstart, ncols, step):
    cmax = min(cstart + step, ncols)
    for c in range(cstart, cmax):
        if grid[row][c] is None:
            return False

        #c += len(grid[row][c]) - 1

    return True

def main():
    lineRE = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
    robots = defaultdict(list)
    file = open('input.txt', 'r')
    nrows = 0
    ncols = 0
    for line in file.readlines():
        line = line.strip()
        values = lineRE.match(line)
        position = Position(int(values.group(2)), int(values.group(1)))
        velocity = Position(int(values.group(4)), int(values.group(3)))
        nrows = max(nrows, position.row)
        ncols = max(ncols, position.col)
        robots[position].append(velocity)
    file.close()

    nrows += 1
    ncols += 1

    grid2D = [[None for _ in range(ncols)] for _ in range(nrows)]
    for row in range(nrows):
        for col in range(ncols):
            position = Position(row, col)
            if position in robots:
                grid2D[row][col]= robots[position]

    # printer(grid2D, nrows, ncols)
    # print("------")
    grid = advance(1000, grid2D, nrows, ncols)
    # printer(grid, nrows, ncols)

    counter_per_quad = [0] * 4
    middle_col = ncols // 2
    middle_row = nrows // 2
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] is None:
                continue

            if row < middle_row and col < middle_col:
                counter_per_quad[0] += len(grid[row][col])
            if row < middle_row and col > middle_col:
                counter_per_quad[1] += len(grid[row][col])
            elif row > middle_row and col < middle_col:
                counter_per_quad[2] += len(grid[row][col])
            elif row > middle_row and col > middle_col:
                counter_per_quad[3] += len(grid[row][col])

    safety_factor = 1
    for quad in counter_per_quad:
        safety_factor *= quad

    print(safety_factor)

    grid = advance(7709, grid2D, nrows, ncols)
    for i in range(0, 10000):
        skip = False
        grid2D = advance(1, grid2D, nrows, ncols)
        for row in range(0, nrows, 1):
            for col in range(0, ncols - 7, 1):
                if has_block(grid2D, row, col, ncols, 7):
                    printer(grid2D, nrows, ncols)
                    print(f"i: {i + 1}) row: {row}, col: {col}")
                    input("next")
                    skip = True
                    break

            if skip:
                break

    
if __name__ == '__main__':
    main()