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
        print(index, program)

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

        # opcodes for jump-if-true / jump-if-false
        if opcode in (5, 6):
            val1 = getvalue(program, index+1, param1_mode)
            val2 = getvalue(program, index+2, param2_mode)

            # Should jump; update current instruction and restart it
            if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                program[index] = val2
                continue

            # No action, continue to next instruction
            index += 3
            continue

        # opcode for less than / equal to
        if opcode in (7, 8):
            val1 = getvalue(program, index+1, param1_mode)
            val2 = getvalue(program, index+2, param2_mode)
            dest = getvalue(program, index+3, IMMEDIATE_MODE)

            # Default 0 (False), set to 1 if True
            program[dest] = 0
            if opcode == 7 and val1 < val2:
                program[dest] = 1
            elif opcode == 8 and val1 == val2:
                program[dest] = 1

            index += 4
            continue

        raise Exception("unknown opcode, something went wrong")


def test():
    # programs defined by question
    # programs that return 1 if true, 0 if false
    equal_8 = [3,9,8,9,10,9,4,9,99,-1,8]
    less_than_8 = [3,9,7,9,10,9,4,9,99,-1,8]
    equal_8_imm_mode = [3,3,1108,-1,8,3,4,3,99]
    less_than_8_imm_mode = [3,3,1107,-1,8,3,4,3,99]
    # programs that return 0 if input is 0, 1 otherwise
    nonzero = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    nonzero_imm_mode = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

    # test cases
    testcases = [
        # (equal_8, 8, 1),
        # (equal_8, 9, 0),
        # (less_than_8, 7, 1),
        # (less_than_8, 9, 0),
        # (equal_8_imm_mode, 8, 1),
        # (equal_8_imm_mode, 9, 0),
        # (less_than_8_imm_mode, 7, 1),
        # (less_than_8_imm_mode, 9, 0),
        # (nonzero, 9, 1),
        (nonzero, 0, 0),
        # (nonzero_imm_mode, 9, 1),
        # (nonzero_imm_mode, 0, 0),
    ]
    for program, inputval, expected in testcases:
        outputval = process(deepcopy(program), inputval)
        assert outputval == expected


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
