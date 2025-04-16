def is_target_possible(target, result, values):
    if result == target and len(values) == 0:
        return True
    elif result > target or len(values) == 0:
        return False
    
    a = is_target_possible(target, result + values[0], values[1:])
    if a:
        return True
    
    # c required for part II
    concated = str(result) + str(values[0])
    c = is_target_possible(target, int(concated), values[1:])
    if c:
        return True

    if result == 0:
        result = 1

    b = is_target_possible(target, result * values[0], values[1:])
    if b:
        return True

    return False

if __name__ == "__main__":
    file = open("input.txt", "r")

    sum = 0
    lines = [line.strip().split(":") for line in file.readlines()]
    for line in lines:
        print("Progress: {}/{}".format(lines.index(line), len(lines)))
        target = int(line[0])
        values = list(map(int, line[1].strip().split(" ")))
        if is_target_possible(target, 0, values):
            sum += target
    
    print(sum)