import re
import os

inputdata = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
inputdata2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def GetValidInstructions(input: str):
    regex = r'mul\(([0-9]{1,3},[0-9]{1,3})\)'
    matches = re.findall(regex, input)
    return matches

def GetFullValidInstructions(input: str):
    regex = r'(mul\(([0-9]{1,3},[0-9]{1,3})\)|do\(\)|don\'t\(\))'
    matches = re.findall(regex, input)
    return matches

def StackValidInstructions(input: list[tuple[str, str]]):
    stack = []
    enabled = True
    for (ins, value) in input:
        if ins == "do()":
            enabled = True
        elif ins == "don't()":
            enabled = False
        elif ins.startswith("mul") and enabled:
            stack.append(value)        
    return stack

def Multiply(a: str):
    a = a.split(",")
    return int(a[0]) * int(a[1])

if __name__ == "__main__":
    input: str = ""
    with open("input.txt", "r") as f:
        input = f.read()

    print(GetFullValidInstructions(inputdata2))

    # Part I
    # instructions = GetValidInstructions(input)
    # result = 0
    # for i in instructions:
    #     result += Multiply(i)
    # print(result)

    # Part II
    instructions = GetFullValidInstructions(input)
    stack = StackValidInstructions(instructions)
    result = 0
    for i in stack:
        result += Multiply(i)
    print(result)
