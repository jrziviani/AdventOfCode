from collections import deque
from collections import defaultdict

def count_splits(diagram: list[list[str]]) -> int:
    rows, cols = len(diagram), len(diagram[0])
    visited = set()
    count_splits = 0
    q = deque([(1, diagram[0].index('S'))])

    while q:
        r, c = q.pop()
        if (r, c) in visited or r >= rows or c < 0 or c >= cols:
            continue

        visited.add((r, c))

        if diagram[r][c] == '^':
            for nr, nc in [(r+1, c-1), (r+1, c+1)]:
                if (nr, nc) not in visited:
                    q.appendleft((nr, nc))
            count_splits += 1
        else:
            q.appendleft((r+1, c))

    return count_splits

def count_timelines(diagram: list[list[str]]) -> int:
    rows, cols = len(diagram), len(diagram[0])
    timelines = defaultdict(int)
    timelines[(1, diagram[0].index('S'))] = 1

    q = deque([(1, diagram[0].index('S'))])
    visited = set()
 
    while q:
        r, c = q.popleft()
        if (r, c) in visited or r >= rows or c < 0 or c >= cols:
            continue
        
        visited.add((r, c))
        curr = timelines[(r, c)]
        
        for nr, nc in ([(r+1, c-1), (r+1, c+1)] if diagram[r][c] == '^' else [(r+1, c)]):
            timelines[(nr, nc)] += curr
            q.append((nr, nc))
    
    return sum(count for (r, c), count in timelines.items() if r >= rows or c < 0 or c >= cols)

def first_solution(filename: str) -> int:
    diagram = []

    with open(filename) as file:
       diagram = [list(line.strip()) for i, line in enumerate(file) if i % 2 == 0]

    return count_splits(diagram)

def second_solution(filename: str) -> int:
    diagram = []

    with open(filename) as file:
       diagram = [list(line.strip()) for i, line in enumerate(file) if i % 2 == 0]

    return count_timelines(diagram)

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))