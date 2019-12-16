"""
https://adventofcode.com/2019/day/11
"""

from collections import defaultdict
import math

# Constants for Intcode computer modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

# Constants for input values
COLOR_BLACK = 0
COLOR_WHITE = 1

# Constants for output values
TURN_LEFT = 0
TURN_RIGHT = 1


class Computer:
    """An Intcode computer that can run a program."""

    def __init__(self, program):
        # program is converted from list of integers to a {index -> integer}
        # map to support arbitrary memory assignment
        # (e.g. writing to position 1mil without the associated 0's in memory)
        self.program = {i: v for i, v in enumerate(program)}
        self.inputs = []
        self.outputs = []
        self.index = 0
        self.halted = False
        self.relative_base = 0

    def get_address(self, index, mode):
        """Get the absolute index referenced by a relative index and a mode."""
        if mode == IMMEDIATE_MODE:
            return index
        elif mode == POSITION_MODE:
            return self.program[index]
        elif mode == RELATIVE_MODE:
            return self.program[index] + self.relative_base
        raise Exception(f"unknown mode: {mode}")

    def get_value(self, index, mode):
        """Return a value from a program by relative index and mode."""
        address = self.get_address(index, mode)
        try:
            return self.program[address]
        except KeyError:
            return 0

    def set_value(self, index, mode, value):
        """Set a value into the program by relative index and mode."""
        address = self.get_address(index, mode)
        self.program[address] = value

    def process(self):
        """Run an Intcode program. Modifiy the program in-place as needed.
        Returns an output when it encounters Opcode 4.
        Uses the `inputs` attribute to support Opcode 3.
            - Each encounter of opcode 3 will remove an element from the inputs
        """
        while not self.halted:
            self.step()
        return self.outputs

    def step(self):
        """Run a single step of the intcode program."""
        # parse opcode and parameter mode(s) from instruction
        # (convert integer into 5-digit string with zeroes before parsing)
        instruction = str(self.program[self.index]).zfill(5)
        opcode = int(instruction[-2:])
        param1_mode = int(instruction[-3])
        param2_mode = int(instruction[-4])
        param3_mode = int(instruction[-5])

        # opcode to halt program
        if opcode == 99:
            self.halted = True
            return

        # opcodes for addition or multiplication
        if opcode in (1, 2):
            val1 = self.get_value(self.index+1, param1_mode)
            val2 = self.get_value(self.index+2, param2_mode)

            if opcode == 1:
                total = val1 + val2
            elif opcode == 2:
                total = val1 * val2

            self.set_value(self.index+3, param3_mode, total)
            self.index += 4
            return

        # opcode for input
        if opcode == 3:
            try:
                inputval = self.inputs.pop(0)
            except IndexError:
                # no input available, halt program until external process
                # adds input and restarts the process
                self.halted = True
                return

            self.set_value(self.index+1, param1_mode, inputval)
            self.index += 2
            return

        # opcode for output
        if opcode == 4:
            self.outputs += [self.get_value(self.index+1, param1_mode)]
            self.index += 2
            return

        # opcodes for jump-if-true / jump-if-false
        if opcode in (5, 6):
            val1 = self.get_value(self.index+1, param1_mode)
            val2 = self.get_value(self.index+2, param2_mode)

            # Should jump; update instruction pointer directly
            if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                self.index = val2
                return

            # No action, continue to next instruction
            self.index += 3
            return

        # opcode for less than / equal to
        if opcode in (7, 8):
            val1 = self.get_value(self.index+1, param1_mode)
            val2 = self.get_value(self.index+2, param2_mode)

            # Default 0 (False), set to 1 if True
            result = 0
            if opcode == 7 and val1 < val2:
                result = 1
            elif opcode == 8 and val1 == val2:
                result = 1

            self.set_value(self.index+3, param3_mode, result)
            self.index += 4
            return

        # opcode for relative base offset
        if opcode == 9:
            self.relative_base += self.get_value(self.index+1, param1_mode)
            self.index += 2
            return

        raise Exception("unknown opcode, something went wrong")


def run_robot(program):
    # All panels start black, and robot starts at origin facing up
    grid = defaultdict(lambda: COLOR_BLACK)
    position = (0, 0)
    direction = 90
    computer = Computer(program)
    current_color = COLOR_WHITE
    while not computer.halted:
        computer.inputs += [current_color]
        # Run program until two outputs are generated
        while len(computer.outputs) != 2:
            if computer.halted:
                return grid
            computer.step()

        # Pop the outputs for processing
        color, turn = computer.outputs
        computer.outputs = []

        # Paint the current panel
        grid[position] = color

        # Move the robot
        if turn == TURN_LEFT:
            direction += 90
        elif turn == TURN_RIGHT:
            direction -= 90
        else:
            raise Exception(f"unknown direction: {direction}")

        x = round(math.cos(math.radians(direction)))
        y = round(math.sin(math.radians(direction)))
        position = (position[0]+x, position[1]+y)
        current_color = grid[position]


def print_grid(grid):
    """Print a map of (x, y) -> color to the console."""
    # Calculate offsets for printing potentially negative range
    min_x = min(grid, key=lambda item: item[0])[0]
    min_y = min(grid, key=lambda item: item[1])[1]
    max_x = max(grid, key=lambda item: item[0])[0]
    max_y = max(grid, key=lambda item: item[1])[1]

    # Loop over grid adjusting for flipped Y perspective
    for y in range(max_y, min_y-1, -1):
        row = ""
        for x in range(min_x, max_x+1):
            color = grid[(x, y)]
            if color == COLOR_BLACK:
                row += " "
            else:
                row += "X"
        print(row)


def test():
    program = [3,9,8,9,10,9,4,9,99,-1,8]
    computer = Computer(program)
    computer.inputs += [8]
    assert computer.process()[0] == 1

    program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    output = Computer(program).process()
    assert output == program

    program = [1102,34915192,34915192,7,4,7,99,0]
    output = Computer(program).process()
    assert len(str(output[0])) == 16

    program = [104,1125899906842624,99]
    output = Computer(program).process()
    assert output[0] == 1125899906842624


def main():
    # Convert the text program into a list of integers (Intcode)
    with open("data/day11.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(',')]
    grid = run_robot(program)
    print_grid(grid)


if __name__ == "__main__":
    test()
    main()
