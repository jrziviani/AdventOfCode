# rotate left -> toward lower numbers
# rotate right -> toward higher numbers
# distance -> how many clicks in that direction
#                V
#[0, 1, 2, ..., 50, ..., 98, 99]
# number of times the dial is left pointing a 0

def calculate_rotations(position: int, rotation: str) -> int:
    steps = -int(rotation[1:]) if rotation[0] == 'L' else int(rotation[1:])
    return (position + steps) % 100

def calculate_rotations_with_zero_passes(position: int, rotation: str) -> tuple[int, int]:
    steps = -int(rotation[1:]) if rotation[0] == 'L' else int(rotation[1:])
    next_position = (position + steps) % 100
    pointed_zero = abs((position + steps) // 100)

    if rotation[0] == 'L' and position == 0 and next_position > 0:
        pointed_zero -= 1

    if rotation[0] == 'L' and next_position == 0:
        pointed_zero += 1

    # print(f'pos: {position} + {steps} = {position+steps};\t{next_position}, {pointed_zero}')

    return (next_position, pointed_zero)

def first_solution(filename: str) -> int:
    counter = 0
    with open(filename, 'r') as file:
        current_step = 50
        for line in file:
            current_step = calculate_rotations(current_step, line.strip())
            if current_step == 0:
                counter += 1
    return counter

def second_solution(filename: str) -> int:
    counter = 0
    with open(filename, 'r') as file:
        current_step = 50
        for line in file:
            current_step, pointed_zero = calculate_rotations_with_zero_passes(current_step, line.strip())
            counter += pointed_zero
    return counter

if __name__ == '__main__':
    print(first_solution('input1.txt'))
    print(second_solution('input1.txt'))