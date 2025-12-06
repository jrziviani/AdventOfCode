import re
from functools import reduce
from operator import mul

def first_solution(filename: str) -> int:
    problems = []

    with open(filename) as file:
        problems = [re.findall(r'\d+|[+*]', line.strip()) for line in file]

    result = 0
    for problem in zip(*problems):
        problemlst = list(problem)
        numbers = [int(n) for n in problemlst[:-1]]

        if problemlst[-1] == '+':
            result += sum(numbers)
        else:
            result += reduce(mul, numbers, 1)

    return result

def second_solution(filename: str) -> int:
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
    
    operator_line = lines[-1]
    data_lines = lines[:-1]
    
    max_len = max(len(line) for line in lines)
    has_data = [False] * max_len
    
    for line in data_lines:
        for i, char in enumerate(line):
            if char not in (' ', '\t'):
                has_data[i] = True
    
    column_groups = []
    i = 0
    while i < len(has_data):
        if has_data[i]:
            start = i
            while i < len(has_data) and has_data[i]:
                i += 1
            end = i - 1
            
            operator = None
            for pos in range(start, end + 1):
                if pos < len(operator_line) and operator_line[pos] in ('+', '*'):
                    operator = operator_line[pos]
                    break
            
            if operator:
                column_groups.append((list(range(start, end + 1)), operator))
        else:
            i += 1

    result = 0
    for positions, operator in reversed(column_groups):
        numbers = []
        for pos in positions:
            digits = ''.join(line[pos] if pos < len(line) else ' ' for line in data_lines)
            digits = digits.strip()
            if digits:
                numbers.append(int(digits))
        
        if operator == '+':
            result += sum(numbers)
        else:
            result += reduce(mul, numbers, 1)
    
    return result

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))