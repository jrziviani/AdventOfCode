
from collections import defaultdict, deque


directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

def parse(file):
    file = open(file, 'r')
    grid = []
    commands = ''
    finished_grid = False
    for line in file:
        line = line.strip()
        if line == '':
            finished_grid = True
            continue

        if not finished_grid:
            grid.append(list(line))
        else:
            commands += line

    file.close()

    return (grid, commands)

def parseII(file):
    file = open(file, 'r')
    grid = []
    commands = ''
    finished_grid = False
    for line in file:
        line = line.strip()
        if line == '':
            finished_grid = True
            continue

        if not finished_grid:
            grid.append(list(line))
        else:
            commands += line

    file.close()

    newgrid = [[] for _ in range(len(grid))]

    for i in range(len(grid)):
        for col in grid[i]:
            if col == '#':
                newgrid[i].append('#')
                newgrid[i].append('#')
            elif col == '.':
                newgrid[i].append('.')
                newgrid[i].append('.')
            elif col == 'O':
                newgrid[i].append('[')
                newgrid[i].append(']')
            elif col == '@':
                newgrid[i].append('@')
                newgrid[i].append('.')

    #for i in range(len(newgrid)):
    #    newgrid[i] = ''.join(newgrid[i])

    # print_grid(newgrid)

    return (newgrid, commands)

def find_robot_position(grid, nrows, ncols):
    for i in range(nrows):
        for j in range(ncols):
            if grid[i][j] == '@':
                return (i, j)
    return None

def find_robot_positionII(grid, nrows, ncols):
    for i in range(nrows):
        for j in range(ncols):
            if grid[i][j] == '@':
                return (i, j)
    return None

def move_goodsII(grid, nrows, ncols, robot_position, direction):
    row, col, = robot_position
    dir = directions[direction]
    dr = row + dir[0]
    dc = col + dir[1]

    if grid[dr][dc] == '#':
        return (row, col)
    
    if direction == '<':
        i = dc
        while i > 0 and grid[dr][i] != '.':
            if grid[dr][i] == '#':
                return (row, col)
            
            i -= 1
        
        if i == 1 or grid[dr][i] == '#':
            return (row, col)
        
        s = ''.join(grid[dr])
        grid[dr] = list(s[:i] + s[i + 1:col + 1] + '.' + s[col + 1:])
        return (dr, dc)

    elif direction == '>':
        i = dc
        while i < ncols - 1 and grid[dr][i] != '.':
            if grid[dr][i] == '#':
                return (row, col)

            i += 1

        if i >= ncols - 1 or grid[dr][i] == '#':
            return (row, col)

        s = ''.join(grid[dr])
        grid[dr] = list(s[:col] + '.' + s[col:i] + s[i + 1:])
        return (dr, dc)
        
    elif direction == '^':
        if grid[dr][dc] == '#':
            return (row, col)

        box_pos = None
        if grid[dr][dc] == '[':
            box_pos = (dr, dc, dc + 1)
        elif grid[dr][dc] == ']':
            box_pos = (dr, dc - 1, dc)

        box_to_move = defaultdict(set)
        last_row = dr
        if box_pos is not None:
            queue = deque([box_pos])
            while queue:
                r, ca, cc = queue.popleft()
                box_to_move[r].add((ca, cc))
                last_row = r
                # print(f"r: {r}, ca: {ca}, cc: {cc}")

                if grid[r - 1][ca] == '#' or grid[r - 1][cc] == '#':
                    return (row, col)

                if grid[r - 1][ca] == '[':
                    queue.append((r - 1, ca, cc))
                    continue

                if grid[r - 1][ca] == ']':
                    queue.append((r - 1, ca - 1, ca))

                if grid[r - 1][cc] == '[':
                    queue.append((r - 1, cc, cc + 1))

        for r in range(last_row - 1, row):
            for box in box_to_move[r]:
                a, c = box
                tmp = grid[r - 1][a]
                grid[r - 1][a] = grid[r][a]
                grid[r][a] = tmp

                tmp = grid[r - 1][c]
                grid[r - 1][c] = grid[r][c]
                grid[r][c] = tmp

        grid[dr][dc] = '@'
        grid[row][col] = '.'

        return (dr, dc)

    else:
        if grid[dr][dc] == '#':
            return (row, col)

        box_pos = None
        if grid[dr][dc] == '[':
            box_pos = (dr, dc, dc + 1)
        elif grid[dr][dc] == ']':
            box_pos = (dr, dc - 1, dc)

        box_to_move = defaultdict(set)
        last_row = dr
        if box_pos is not None:
            queue = deque([box_pos])
            while queue:
                r, ca, cc = queue.popleft()
                box_to_move[r].add((ca, cc))
                last_row = r
                # print(f"r: {r}, ca: {ca}, cc: {cc}")

                if grid[r + 1][ca] == '#' or grid[r + 1][cc] == '#':
                    return (row, col)

                if grid[r + 1][ca] == '[':
                    queue.append((r + 1, ca, cc))
                    continue

                if grid[r + 1][ca] == ']':
                    queue.append((r + 1, ca - 1, ca))

                if grid[r + 1][cc] == '[':
                    queue.append((r + 1, cc, cc + 1))

        for r in range(last_row, row, -1):
            for box in box_to_move[r]:
                a, c = box
                tmp = grid[r + 1][a]
                grid[r + 1][a] = grid[r][a]
                grid[r][a] = tmp

                tmp = grid[r + 1][c]
                grid[r + 1][c] = grid[r][c]
                grid[r][c] = tmp

        grid[dr][dc] = '@'
        grid[row][col] = '.'

        return (dr, dc)

def move_goods(grid, nrows, ncols, robot_position, direction):
    row, col, = robot_position
    dr = row + directions[direction][0]
    dc = col + directions[direction][1]

    if grid[dr][dc] == '#':
        return (row, col)

    if grid[dr][dc] == '.':
        grid[row][col] = '.'
        grid[dr][dc] = '@'
        return (dr, dc)

    i = 0
    if direction == 'v':
        i = dr
        while grid[i][col][0] != '.':
            if i== nrows or grid[i][col] == '#':
                return (row, col)
            i += 1

        for j in range(i, row, -1):
            tmp = grid[j][col]
            grid[j][col] = grid[j - 1][col]
            grid[j - 1][col] = tmp

    if direction == '^':
        i = dr
        while grid[i][col] != '.':
            if i == 0 or grid[i][col] == '#':
                return (row, col)
            i -= 1

        for j in range(i, row):
            tmp = grid[j][col]
            grid[j][col] = grid[j + 1][col]
            grid[j + 1][col] = tmp

    elif direction == '>':
        i = dc
        while grid[row][i] != '.':
            if i == ncols or grid[row][i] == '#':
                return (row, col)
            i += 1

        for j in range(i, col, -1):
            tmp = grid[row][j]
            grid[row][j] = grid[row][j - 1]
            grid[row][j - 1] = tmp

    elif direction == '<':
        i = dc
        while grid[row][i] != '.':
            if i == 0 or grid[row][i] == '#':
                return (row, col)
            i -= 1

        for j in range(i, col, 1):
            tmp = grid[row][j]
            grid[row][j] = grid[row][j + 1]
            grid[row][j + 1] = tmp

    return (dr, dc)

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def mainI():
    grid, commands = parse('input.txt')
    nrows = len(grid)
    ncols = len(grid[0])
    robot_position = find_robot_position(grid, nrows, ncols)
    # print_grid(grid)
    for command in commands:
        robot_position = move_goods(grid, nrows, ncols, robot_position, command)
        # print_grid(grid)

    total_sum = 0
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] == 'O':
                total_sum += 100 * row + col

    print(total_sum)

def mainII():
    grid, commands = parseII('input.txt')
    nrows = len(grid)
    ncols = len(grid[0])
    robot_position = find_robot_positionII(grid, nrows, ncols)
    #print_grid(grid)
    for command in commands:
        robot_position = move_goodsII(grid, nrows, ncols, robot_position, command)
        #print_grid(grid)

    total_sum = 0
    for row in range(nrows):
        for col in range(ncols):
            if grid[row][col] == '[':
                total_sum += 100 * row + col

    print(total_sum)

if __name__ == '__main__':
    #mainI()
    mainII()