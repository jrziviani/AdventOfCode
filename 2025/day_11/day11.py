from collections import defaultdict

def dfs(circuit: dict[str, list[str]], name: str, visited: set[str], memo: dict[str, int]) -> int:
    if name == 'out':
        return 1
    
    if name in memo:
        return memo[name]
    
    if name not in circuit or not circuit[name]:
        memo[name] = 0
        return 0
    
    visited.add(name)
    
    count_paths = 0
    for neighbors in circuit[name]:
        count_paths += dfs(circuit, neighbors, visited, memo)

    visited.remove(name)
    memo[name] = count_paths
    
    return memo[name]

def first_solution(filename: str) -> int:
    circuit = defaultdict(list[str])
    with open(filename) as file:
        for line in file:
            line = line.strip()
            name = line[:3]
            for output in line[5:].split(' '):
                circuit[name].append(output)
    
    memo = {}
    visited = set()
    return dfs(circuit, 'you', visited, memo)

def dfs2(circuit: dict[str, list[str]], name: str, visited: set[str], memo: dict[tuple, int]) -> int:
    if name == 'out':
        return 1 if 'dac' in visited and 'fft' in visited else 0
    
    key = (name, 'dac' in visited, 'fft' in visited)
    if key in memo:
        return memo[key]
     
    if name not in circuit or not circuit[name]:
        memo[key] = 0
        return 0
    
    visited.add(name)
    
    count_paths = 0
    for neighbors in circuit[name]:
        count_paths += dfs2(circuit, neighbors, visited, memo)

    visited.remove(name)
    memo[key] = count_paths
        
    return count_paths

def second_solution(filename: str) -> int:
    circuit = defaultdict(list[str])
    with open(filename) as file:
        for line in file:
            line = line.strip()
            name = line[:3]
            for output in line[5:].split(' '):
                circuit[name].append(output)
    
    memo = {}
    visited = set()
    return dfs2(circuit, 'svr', visited, memo)

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))