
def spoiled_ingredients(ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    spoiled = set()
    for ingredient in ingredients:
        for rng in ranges:
            inRange = ingredient >= rng[0] and ingredient <= rng[1]
            if inRange:
                if ingredient in spoiled:
                    spoiled.remove(ingredient)
                break
            
            spoiled.add(ingredient)

    return len(ingredients) - len(spoiled)

START = 0
END = 1
def valid_ids(ranges: list[tuple[int, int]]) -> int:
    ranges.sort()
    new_ranges = [[ranges[0][START], ranges[0][END]]]
    merged_id = 0
    for i in range(1, len(ranges)):
        current_range = ranges[i]
        merged_range = new_ranges[merged_id]

        if current_range[START] >= merged_range[START] and current_range[START] <= merged_range[END]:
            merged_range[END] = max(merged_range[END], current_range[END])
        else:
            new_ranges.append([current_range[START], current_range[END]])
            merged_id += 1

    total_valid_ids = 0
    for rng in new_ranges:
        total_valid_ids += rng[END] - rng[START] + 1
        
    return total_valid_ids

def first_solution(filename: str) -> int:
    isRange = True
    ranges = []
    ingredients = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line == '':
                isRange = False
                continue

            if isRange:
                parts = line.split('-')
                ranges.append((int(parts[0]), int(parts[1])))
            else:
                ingredients.append(int(line))
            
    return spoiled_ingredients(ranges, ingredients)

def second_solution(filename: str) -> int:
    ranges = []
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line == '':
                break

            parts = line.split('-')
            ranges.append((int(parts[0]), int(parts[1])))

    return valid_ids(ranges)

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))