


def parse():
    locks = []
    keys = []
    counter = [0 for i in range(5)]
    file = open('input.txt', 'r')

    next_line = file.readline()
    while next_line:
        line = next_line.strip()
        next_line = file.readline()

        if line.startswith('#####') and next_line in ['\n', '']:
            keys.append(counter)
            counter = [0 for i in range(5)]
            continue
        elif line.startswith('.....') and next_line in ['\n', '']:
            locks.append(counter)
            counter = [0 for i in range(5)]
            continue

        if len(line) == 5:
            for i in range(5):
                if line[i] == '#':
                    counter[i] += 1
        
    file.close()

    for lock in locks:
        for i in range(5):
            lock[i] -= 1

    return (locks, keys)

def main():
    locks, keys = parse()

    total = 0
    matched = True
    for lock in locks:
        for key in keys:
            for i in range(5):
                if lock[i] + key[i] > 5:
                    matched = False
                    break

            if matched:
                #print(f"Lock: {lock}, Key: {key}")
                total += 1

            matched = True

    print(f"Part I: {total}")

if __name__ == '__main__':
    main()