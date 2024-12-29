
memo = {}

def find_pattern(required, patterns):
    def dfs(required, patterns, made):
        if len(required) == 0:
            return 1

        if required in memo:
            return memo[required]

        count = 0
        for pattern in patterns:
            if required.startswith(pattern):
                count += dfs(required[len(pattern):], patterns, made + pattern)

        memo[required] = count
        return count

    count = dfs(required, patterns, '')
    return count

def main():
    available = set()
    required = set()
    file = open('input.txt', 'r')
    for line in file:
        line = line.strip()
        if ',' in line:
            available = [l.strip() for l in line.split(',')]

        elif len(line) > 0:
            required.add(line)

    file.close()

    count = 0
    arrangements = 0
    for towel in required:
        res = find_pattern(towel, available)
        arrangements += res
        if res > 0:
            count += 1

    print(f'Found {count} towels')
    print(f'Found {arrangements} arrangements')

if __name__ == '__main__':
    main()