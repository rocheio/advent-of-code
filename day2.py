"""
https://adventofcode.com/2019/day/2
"""

def process(program):
    for index in range(0, len(program), 4):
        opcode = program[index]
        if opcode == 99:
            # opcode to exit normally
            break

        val1 = program[program[index+1]]
        val2 = program[program[index+2]]
        dest = program[index+3]

        if opcode == 1:
            program[dest] = val1 + val2
            continue

        if opcode == 2:
            program[dest] = val1 * val2
            continue

        raise Exception("unknown opcode, something went wrong")


def adjust_data(program):
    """Adjust the program to the 1202 state before running."""
    program[1] = 12
    program[2] = 2


def test():
    testcases = [
        ([1,0,0,0,99],[2,0,0,0,99]),
        ([2,3,0,3,99],[2,3,0,6,99]),
        ([2,4,4,5,99,0],[2,4,4,5,99,9801]),
        ([1,1,1,4,99,5,6,0,99],[30,1,1,4,2,5,6,0,99]),
        ([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70,2,3,11,0,99,30,40,50]),
    ]
    for program, expected in testcases:
        process(program)
        assert program == expected


def main():
    with open("data/day2.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(',')]
    adjust_data(program)
    process(program)
    print(f"value is: {program[0]}")


if __name__ == "__main__":
    test()
    main()
