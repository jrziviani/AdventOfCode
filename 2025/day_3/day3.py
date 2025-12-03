


def get_highest_joltage(batteries: list[int]) -> int:
    high_left = 0
    high_left_idx = 0
    for i in range(0, len(batteries) - 1):
        if high_left < batteries[i]:
            high_left = batteries[i]
            high_left_idx = i

    high_right = 0
    for i in range(high_left_idx + 1, len(batteries)):
        high_right = max(high_right, batteries[i])

    return high_left * 10 + high_right

def get_highest_joltage_12(batteries: list[int]) -> int:
    sum_batteries = 0
    missing_batteries = 12

    start_window = 0
    end_window = len(batteries) - missing_batteries + 1
    while missing_batteries:
        highest = 0
        new_start = 0
        
        if end_window - start_window > 1:
            while start_window < end_window:
                if batteries[start_window] > highest:
                    highest = batteries[start_window]
                    new_start = start_window

                start_window += 1
        else:
            highest = batteries[start_window]
            new_start = start_window

        missing_batteries -= 1
        sum_batteries = sum_batteries * 10 + highest
        end_window = len(batteries) - missing_batteries + 1
        start_window = new_start + 1

    return sum_batteries

def first_solution(filename: str) -> int:
    result = 0
    with open(filename) as file:
        for line in file:
            result += get_highest_joltage([int(c) for c in line.strip()])
            
    return result

def second_solution(filename: str) -> int:
    result = 0
    with open(filename) as file:
        for line in file:
            result += get_highest_joltage_12([int(c) for c in line.strip()])
            
    return result

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))