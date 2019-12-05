"""
https://adventofcode.com/2019/day/5
"""

from copy import deepcopy


# Constants for Intcode computer modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1


def getvalue(program, index, mode=POSITION_MODE):
    """Return a value from a program by index based on the mode.
    Parameters that instructions write to should always be IMMEDIATE_MODE.
    """
    if mode == POSITION_MODE:
        return program[program[index]]
    elif mode == IMMEDIATE_MODE:
        return program[index]
    raise Exception(f"unknown mode: {mode}")


def process(program, inputval=None):
    """Run an Intcode program. Modifiy the program in-place as needed.
    Accepts an optional `inputval` to support Opcode 3.
    Returns an `outputval` if it encounters Opcode 4.
    """
    outputval = None
    index = 0
    while index < len(program):
        # parse opcode and parameter mode(s) from instruction
        # (convert integer into 5-digit string with zeroes before parsing)
        instruction = str(program[index]).zfill(5)
        opcode = int(instruction[-2:])
        param1_mode = int(instruction[-3])
        param2_mode = int(instruction[-4])
        # Since param 3 is always a destination, which is always immediate,
        # this var is ignored at the moment but will likely be needed later
        param3_mode = int(instruction[-5])

        # opcode to exit normally
        if opcode == 99:
            return outputval

        # opcodes for addition or multiplication
        if opcode in (1, 2):
            val1 = getvalue(program, index+1, param1_mode)
            val2 = getvalue(program, index+2, param2_mode)
            dest = getvalue(program, index+3, IMMEDIATE_MODE)

            if opcode == 1:
                program[dest] = val1 + val2
            elif opcode == 2:
                program[dest] = val1 * val2

            index += 4
            continue

        # opcode for input
        if opcode == 3:
            dest = getvalue(program, index+1, IMMEDIATE_MODE)
            program[dest] = inputval
            index += 2
            continue

        # opcode for output
        if opcode == 4:
            outputval = getvalue(program, index+1, param1_mode)
            index += 2
            continue

        raise Exception("unknown opcode, something went wrong")


def test():
    testcases = [
        ([1002,4,3,4,33],[1002,4,3,4,99]),
        ([1101,100,-1,4,0],[1101,100,-1,4,99]),
    ]
    for program, expected in testcases:
        process(program)
        assert program == expected


def main():
    # Convert the text program into a list of integers (Intcode)
    with open("data/day5.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(',')]
    output = process(program, inputval=1)
    print(f"answer is: {output}")


if __name__ == "__main__":
    test()
    main()

