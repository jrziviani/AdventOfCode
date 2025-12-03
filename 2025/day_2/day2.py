from collections import defaultdict

def check_repeated_range(start: int, end: int) -> int:
    result = 0
    for num in range(start, end + 1):
        snum = str(num)
        lnum = len(snum)
        if lnum % 2 != 0:
            continue

        if snum[:lnum // 2] == snum[lnum // 2:]:
            result += num

    return result

def check_freq_range(start: int, end: int) -> int:
    result = 0
    for num in range(start, end + 1):
        snum = str(num)
        lnum = len(snum)

        for i in range(1, lnum // 2 + 1):
            if lnum % i != 0:
                continue

            prefix = snum[:i]
            repeat = lnum // i
            
            if prefix * repeat == snum:
                result += num
                break

    return result

def first_solution(filename: str) -> int:
    result = 0
    with open(filename) as file:
        for line in file:
            for ranges in line.strip().split(','):
                range = ranges.split('-')
                result += check_repeated_range(int(range[0]), int(range[1]))
    return result

def second_solution(filename: str) -> int:
    result = 0
    with open(filename) as file:
        for line in file:
            for ranges in line.strip().split(','):
                range = ranges.split('-')
                result += check_freq_range(int(range[0]), int(range[1]))
    return result

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))

