"""
https://adventofcode.com/2019/day/7
"""

from copy import deepcopy
from itertools import permutations


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


def process(program, inputs=None):
    """Run an Intcode program. Modifiy the program in-place as needed.
    Returns an `outputval` if it encounters Opcode 4.
    Accepts an optional `inputs` list to support Opcode 3.
        - Each encounter of opcode 3 will remove an element from the inputs
    """
    program = deepcopy(program)
    inputs = deepcopy(inputs)

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
            program[dest] = inputs.pop(0)

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

            # Should jump; update instruction pointer directly
            if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                index = val2
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


def best_phase_settings(program):
    """Return the best phase settings for a 5-amp relay of a program."""
    calcs = {
        settings: thruster_signal(program, settings)
        for settings in permutations(range(5))
    }
    return max(calcs, key=calcs.get)


def thruster_signal(program, phase_settings):
    """Return total signal produced from a program run through an amp relay."""
    inputval = 0
    for setting in phase_settings:
        inputval = process(program, inputs=[setting, inputval])
    return inputval


def test():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    best = best_phase_settings(program)
    max_signal = thruster_signal(program, best)
    assert best == (4,3,2,1,0)
    assert max_signal == 43210

    program = [
        3,23,3,24,1002,24,10,24,1002,23,-1,23,
        101,5,23,23,1,24,23,23,4,23,99,0,0
    ]
    best = best_phase_settings(program)
    max_signal = thruster_signal(program, best)
    assert best == (0,1,2,3,4)
    assert max_signal == 54321

    program = [
        3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
    ]
    best = best_phase_settings(program)
    max_signal = thruster_signal(program, best)
    assert best == (1,0,4,3,2)
    assert max_signal == 65210


def main():
    # Convert the text program into a list of integers (Intcode)
    with open("data/day7.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(',')]

    # Possible sequences are [0,1,2,3,4] in any order
    best = best_phase_settings(program)
    max_signal = thruster_signal(program, best)
    print(f"highest possible signal is: {max_signal}")


if __name__ == "__main__":
    test()
    main()
