import re


def linear_solver(a, b, prize) -> int:
    resA = b[0] * prize[1] - b[1] * prize[0]
    resB = b[0] * a[1] - b[1] * a[0]
    if resA % resB != 0:
        return float('inf')

    bestA = resA // resB
    resB = prize[0] - a[0] * bestA
    if resB % b[0] != 0:
        return float('inf')

    bestB = resB // b[0]
    return 3 * bestA + bestB


def solver(a, b, prize) -> int:
    memo = {}

    def dfs(x: int, y: int, cost: int) -> int:
        if x == prize[0] and y == prize[1]:
            return cost
        elif x > prize[0] or y > prize[1]:
            return float('inf')

        if (x, y) in memo:
            return memo[(x, y)]

        ca = dfs(x + a[0], y + a[1], cost + 3)
        cb = dfs(x + b[0], y + b[1], cost + 1)
        memo[(x, y)] = min(ca, cb)

        return memo[(x, y)]

    return dfs(0, 0, 0)


if __name__ == '__main__':
    file = open('./input.txt', 'r')

    buttonA = re.compile(r'Button A: X\+(\d+), Y\+(\d+)')
    buttonB = re.compile(r'Button B: X\+(\d+), Y\+(\d+)')
    prize = re.compile(r'Prize: X=(\d+), Y=(\d+)')

    total = 0
    for line in file.readlines():
        line = line.strip()
        if line.startswith('Button A'):
            a = buttonA.match(line)
            a = (int(a.group(1)), int(a.group(2)))
        elif line.startswith('Button B'):
            b = buttonB.match(line)
            b = (int(b.group(1)), int(b.group(2)))
        elif line.startswith('Prize'):
            p = prize.match(line)
            p = (int(p.group(1)) + 10000000000000,
                 int(p.group(2)) + 10000000000000)
            res = linear_solver(a, b, p)
            if res != float('inf'):
                total += res

    file.close()

    print(f"Total: {total}")
