import re
from collections import deque
import z3 # pip3 install z3-solver

def target_to_binary(code: str) -> int:
    binary_str = ''.join('1' if char == '#' else '0' for char in code)
    return int(binary_str, 2)

def switches_to_binary(switches: str, n: int) -> int:
    switch_indices = map(int, switches.split(','))
    binary_value = 0
    for index in switch_indices:
        binary_value |= (1 << (n - 1 - index))
    return binary_value

def solve_machine(target: str, switches: list[str]) -> int:
    target_binary = target_to_binary(target)
    n = len(target)
    
    switch_binaries = [switches_to_binary(switch, n) for switch in switches]
    
    queue = deque([(0, 0)])
    visited = {0}
    while queue:
        current_state, steps = queue.popleft()
        
        if current_state == target_binary:
            return steps
        
        for switch_binary in switch_binaries:
            new_state = current_state ^ switch_binary
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))
    
    return -1

def solve_joltage(target_joltages: list[int], switches: list[str]) -> int:
    n = len(target_joltages)
    m = len(switches)
    
    x = [z3.Int(f'x_{i}') for i in range(m)]
    
    solver = z3.Optimize()
    
    for i in range(m):
        solver.add(x[i] >= 0)
    
    for i in range(n):
        constraint_expr = 0
        for j, switch in enumerate(switches):
            indices = [int(idx) for idx in switch.split(',')]
            if i in indices:
                constraint_expr += x[j]
        
        solver.add(constraint_expr == target_joltages[i])
    
    total_presses = z3.Sum(x)
    solver.minimize(total_presses)
    
    if solver.check() == z3.sat:
        model = solver.model()
        result = 0
        for i in range(m):
            val = model[x[i]]
            if val is not None:
                result += val.as_long()
        return result
    
    else:
        return -1

def first_solution(filename: str) -> int:
    total_presses = 0
    
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            target_match = re.search(r'\[([#.]+)\]', line)
            if not target_match:
                continue
                
            target = target_match.group(1)
            
            switch_matches = re.findall(r'\(([0-9,]+)\)', line)
            switches = switch_matches
            
            min_presses = solve_machine(target, switches)
            if min_presses == -1:
                return -1
                
            total_presses += min_presses
    
    return total_presses

def second_solution(filename: str) -> int:
    total_presses = 0
    
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            joltage_match = re.search(r'\{([0-9,]+)\}', line)
            if not joltage_match:
                continue
                
            joltage_values = [int(x) for x in joltage_match.group(1).split(',')]
            
            switch_matches = re.findall(r'\(([0-9,]+)\)', line)
            switches = switch_matches
            
            min_presses = solve_joltage(joltage_values, switches)
            if min_presses == -1:
                return -1
                
            total_presses += min_presses
    
    return total_presses

if __name__ == "__main__":
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))