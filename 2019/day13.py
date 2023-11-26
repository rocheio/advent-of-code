"""
https://adventofcode.com/2019/day/13
"""

from collections import defaultdict
import math

# Constants for Intcode computer modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

# Constants for game objects
EMPTY = 0  # No game object appears in this tile
WALL = 1  # Walls are indestructible barriers
BLOCK = 2  # Blocks can be broken by the ball
PADDLE = 3  # The paddle is indestructible
BALL = 4  # ball moves diagonally and bounces off objects

# Constants for joystick positions
J_LEFT = -1
J_MIDDLE = 0
J_RIGHT = 1


class Halt(Exception):
    """Signal to raise when computer exits operation normally."""

    pass


class NeedInput(Exception):
    """Signal to raise when computer requires input."""

    pass


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
        while True:
            try:
                self.step()
            except Halt:
                break
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
            raise Halt()

        # opcodes for addition or multiplication
        if opcode in (1, 2):
            val1 = self.get_value(self.index + 1, param1_mode)
            val2 = self.get_value(self.index + 2, param2_mode)

            if opcode == 1:
                total = val1 + val2
            elif opcode == 2:
                total = val1 * val2

            self.set_value(self.index + 3, param3_mode, total)
            self.index += 4
            return

        # opcode for input
        if opcode == 3:
            try:
                inputval = self.inputs.pop(0)
            except IndexError:
                raise NeedInput()

            self.set_value(self.index + 1, param1_mode, inputval)
            self.index += 2
            return

        # opcode for output
        if opcode == 4:
            self.outputs += [self.get_value(self.index + 1, param1_mode)]
            self.index += 2
            return

        # opcodes for jump-if-true / jump-if-false
        if opcode in (5, 6):
            val1 = self.get_value(self.index + 1, param1_mode)
            val2 = self.get_value(self.index + 2, param2_mode)

            # Should jump; update instruction pointer directly
            if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                self.index = val2
                return

            # No action, continue to next instruction
            self.index += 3
            return

        # opcode for less than / equal to
        if opcode in (7, 8):
            val1 = self.get_value(self.index + 1, param1_mode)
            val2 = self.get_value(self.index + 2, param2_mode)

            # Default 0 (False), set to 1 if True
            result = 0
            if opcode == 7 and val1 < val2:
                result = 1
            elif opcode == 8 and val1 == val2:
                result = 1

            self.set_value(self.index + 3, param3_mode, result)
            self.index += 4
            return

        # opcode for relative base offset
        if opcode == 9:
            self.relative_base += self.get_value(self.index + 1, param1_mode)
            self.index += 2
            return

        raise Exception("unknown opcode, something went wrong")

    def step_until(self, limit):
        """Run program until two outputs are generated"""
        while len(self.outputs) != 3:
            self.step()

        # Pop the outputs for processing
        outputs = self.outputs
        self.outputs = []
        return outputs


class Game:
    """A game played from an Intcode program."""

    def __init__(self, program):
        self.computer = Computer(program)
        self.grid = defaultdict(lambda: EMPTY)
        # Track (x, y) ball and paddle positions for "AI"
        self.ball_pos = (0, 0)
        self.paddle_pos = (0, 0)

    def play_to_win(self):
        """Return the score achieved after winning the game."""
        score = 0

        # first two inputs are to just stay still before AI can kick in
        self.computer.inputs += [J_MIDDLE, J_MIDDLE]

        while True:
            # play until computer returns 3 outputs or raises a signal
            try:
                x, y, tile = self.computer.step_until(3)
            except Halt:
                break
            except NeedInput:
                self.set_input()
                continue

            # update current score when game reports it
            if (x, y) == (-1, 0):
                score = tile
                print(f"score is {score}")
                continue

            # Otherwise, instruction to update game grid
            self.grid[(x, y)] = tile
            print(f"tile {tile} at {x},{y}")

            # track and joystick positions
            if tile == BALL:
                self.ball_pos = (x, y)
            elif tile == PADDLE:
                self.paddle_pos = (x, y)

            # print game world whenver ball or paddle moves
            if tile in (BALL, PADDLE):
                print_grid(self.grid)

        return score

    def set_input(self):
        """Set input value based on desired location."""
        if self.paddle_pos[0] < self.ball_pos[0]:
            inp = J_RIGHT
        elif self.paddle_pos[0] > self.ball_pos[0]:
            inp = J_LEFT
        else:
            inp = J_MIDDLE

        print(f"setting joystick input to: {inp}")
        self.computer.inputs += [inp]


def print_grid(grid):
    """Print a map of (x, y) -> tiles to the console."""
    if not grid:
        return

    icons = {
        EMPTY: " ",
        WALL: "|",
        BLOCK: "x",
        PADDLE: "_",
        BALL: "o",
    }

    # Calculate offsets for printing potentially negative range
    min_x = min(grid, key=lambda item: item[0])[0]
    min_y = min(grid, key=lambda item: item[1])[1]
    max_x = max(grid, key=lambda item: item[0])[0]
    max_y = max(grid, key=lambda item: item[1])[1]

    # Loop over grid adjusting for flipped Y perspective
    for y in range(max_y, min_y - 1, -1):
        row = ""
        for x in range(min_x, max_x + 1):
            tile = grid[(x, y)]
            row += icons[tile]
        print(row)


def test():
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    computer = Computer(program)
    computer.inputs += [8]
    assert computer.process()[0] == 1

    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    output = Computer(program).process()
    assert output == program

    program = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    output = Computer(program).process()
    assert len(str(output[0])) == 16

    program = [104, 1125899906842624, 99]
    output = Computer(program).process()
    assert output[0] == 1125899906842624


def main():
    # Convert the text program into a list of integers (Intcode)
    with open("data/day13.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(",")]

    # Set number quarters inserted to 2 to play for free
    program[0] = 2

    game = Game(program)
    score = game.play_to_win()
    print(f"score after breaking all blocks is: {score}")


if __name__ == "__main__":
    test()
    main()
