from collections import defaultdict

# learned from https://observablehq.com/@jwolondon/advent-of-code-2024-day-21
numeric = ['789', '456', '123', '.0A']
directional = ['.^A', '<v>']

def getCoordinates(key, pad):
    for i, row in enumerate(pad):
        if key in row:
            return (i, row.index(key))
    return None

def shortestPath(fromKey, toKey, pad):
    r1, c1 = getCoordinates(fromKey, pad)
    r2, c2 = getCoordinates(toKey, pad)

    ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
    lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

    if c2 > c1 and pad[r2][c1] != '.':
        return ud + lr + 'A'
    
    if pad[r1][c2] != '.':
        return lr + ud + 'A'
    
    return ud + lr + 'A'
  
def generateNumericMoves(keys):
    toKeys = ""
    fromKey = 'A'
    for key in keys:
        toKeys += shortestPath(fromKey, key, numeric)
        fromKey = key
    
    return toKeys

def generateDirectionalMoves(keys):
    toKeys = ""
    fromKey = 'A'
    for key in keys:
        toKeys += shortestPath(fromKey, key, directional)
        fromKey = key

    return toKeys

def dfs(keys, iteration, memo):
    if iteration == 0: 
        return len(keys)
    
    kname = ''.join(keys) + str(iteration)
    if kname in memo:
        return memo[kname]
    
    fromKey = 'A'
    l = 0
    for key in keys:
        toKeys = shortestPath(fromKey, key, directional)
        kname = ''.join(toKeys) + str(iteration - 1)
        memo[kname] = dfs(toKeys, iteration - 1, memo)
        l += memo[kname]
        fromKey = key

    return l

def main():
    codelist = []
    file = open('input.txt', 'r')
    for line in file:
        line = line.strip()
        codelist.append(line)
    file.close()

    total = 0
    for code in codelist:
        target = generateNumericMoves(code)
        for _ in range(2):
            target = generateDirectionalMoves(target)
        
        total += len(target) * int(code[:-1])

    print(f'Part I: {total}')

    total = 0
    for code in codelist:
        memo = defaultdict(int)
        target = generateNumericMoves(code)
        total += dfs(target, 25, memo) * int(code[:-1])

    print(f'Part II: {total}')

if __name__ == '__main__':
    main()