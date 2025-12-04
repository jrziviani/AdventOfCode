
def check_neighbors(grid: list[list[str]]) -> int:
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def counter(y: int, x: int) -> int:
        counter = 0
        for neighbor in neighbors:
            ny, nx = neighbor
            dy = y + ny
            dx = x + nx
            if dy < 0 or dy >= len(grid) or dx < 0 or dx >= len(grid[0]):
                continue

            counter += 1 if grid[dy][dx] == '@' else 0
        
        return counter
        
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                continue

            if counter(row, col) < 4:
                total += 1

    return total

def check_neighbors_and_remove(grid: list[list[str]]) -> int:
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    to_remove = []

    def counter(y: int, x: int) -> int:
        counter = 0
        for neighbor in neighbors:
            ny, nx = neighbor
            dy = y + ny
            dx = x + nx
            if dy < 0 or dy >= len(grid) or dx < 0 or dx >= len(grid[0]):
                continue

            counter += 1 if grid[dy][dx] == '@' else 0
        
        return counter
        
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                continue

            if counter(row, col) < 4:
                to_remove.append((row, col))
                total += 1

    for ry, rx in to_remove:
        grid[ry][rx] = '.'

    return total

def first_solution(filename: str) -> int:
    grid = []
    with open(filename) as file:
        for line in file:
            grid.append([c for c in line.strip()])
    
    return check_neighbors(grid)

def debug(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))
    print()

def second_solution(filename: str) -> int:
    grid = []
    with open(filename) as file:
        for line in file:
            grid.append([c for c in line.strip()])
    
    total = 0
    removed = 0
    while True:
        old_grid = [row.copy() for row in grid]
        removed = check_neighbors_and_remove(grid)
        if old_grid == grid:
            break
        total += removed
    return total

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))