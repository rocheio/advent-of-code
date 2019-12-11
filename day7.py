"""
https://adventofcode.com/2019/day/7
"""

from copy import deepcopy
from itertools import permutations


# Constants for Intcode computer modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1


class Amplifier:
    """An instance of a program that can accept inputs and process many times."""
    def __init__(self, program):
        self.program = deepcopy(program)
        self.inputs = []
        self.halted = False

    def getvalue(self, index, mode=POSITION_MODE):
        """Return a value from a program by index based on the mode.
        Parameters that instructions write to should always be IMMEDIATE_MODE.
        """
        if mode == POSITION_MODE:
            return self.program[self.program[index]]
        elif mode == IMMEDIATE_MODE:
            return self.program[index]
        raise Exception(f"unknown mode: {mode}")

    def process(self):
        """Run an Intcode program. Modifiy the program in-place as needed.
        Returns an output when it encounters Opcode 4.
        Uses the `inputs` attribute to support Opcode 3.
            - Each encounter of opcode 3 will remove an element from the inputs
        """
        print(self.inputs)
        index = 0
        while index < len(self.program):
            # parse opcode and parameter mode(s) from instruction
            # (convert integer into 5-digit string with zeroes before parsing)
            instruction = str(self.program[index]).zfill(5)
            opcode = int(instruction[-2:])
            param1_mode = int(instruction[-3])
            param2_mode = int(instruction[-4])
            # Since param 3 is always a destination, which is always immediate,
            # this var is ignored at the moment but will likely be needed later
            param3_mode = int(instruction[-5])

            # opcode to halt program
            if opcode == 99:
                self.halted = True
                return outputval

            # opcodes for addition or multiplication
            if opcode in (1, 2):
                val1 = self.getvalue(index+1, param1_mode)
                val2 = self.getvalue(index+2, param2_mode)
                dest = self.getvalue(index+3, IMMEDIATE_MODE)

                if opcode == 1:
                    self.program[dest] = val1 + val2
                elif opcode == 2:
                    self.program[dest] = val1 * val2

                index += 4
                continue

            # opcode for input
            if opcode == 3:
                dest = self.getvalue(index+1, IMMEDIATE_MODE)
                self.program[dest] = self.inputs.pop(0)

                index += 2
                continue

            # opcode for output
            if opcode == 4:
                return self.getvalue(index+1, param1_mode)

            # opcodes for jump-if-true / jump-if-false
            if opcode in (5, 6):
                val1 = self.getvalue(index+1, param1_mode)
                val2 = self.getvalue(index+2, param2_mode)

                # Should jump; update instruction pointer directly
                if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                    index = val2
                    continue

                # No action, continue to next instruction
                index += 3
                continue

            # opcode for less than / equal to
            if opcode in (7, 8):
                val1 = self.getvalue(index+1, param1_mode)
                val2 = self.getvalue(index+2, param2_mode)
                dest = self.getvalue(index+3, IMMEDIATE_MODE)

                # Default 0 (False), set to 1 if True
                self.program[dest] = 0
                if opcode == 7 and val1 < val2:
                    self.program[dest] = 1
                elif opcode == 8 and val1 == val2:
                    self.program[dest] = 1

                index += 4
                continue

            raise Exception("unknown opcode, something went wrong")


def best_phase_settings(program):
    """Return the best phase settings for a 5-amp relay of a program."""
    calcs = {
        settings: thruster_signal(program, settings)
        for settings in permutations(range(5,10))
    }
    return max(calcs, key=calcs.get)


def thruster_signal(program, phase_settings):
    """Return total signal produced from a program run through an amp relay."""
    # Create a relay of 5 Amplifiers with their phase settings as first input
    relay = []
    for init_value in phase_settings:
        amp = Amplifier(program)
        amp.inputs += [init_value]
        relay += [amp]

    # Run the relay until all amps have halted
    value = 0
    while True:
        if all(amp.halted for amp in relay):
            break
        for amp in relay:
            # Pass over any amps that have halted
            if amp.halted:
                continue
            amp.inputs += [value]
            value = amp.process()
    return inputval


def test():
    program = [
        3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
    ]
    best = best_phase_settings(program)
    max_signal = thruster_signal(program, best)
    assert best == (9,8,7,6,5)
    assert max_signal == 139629729


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
