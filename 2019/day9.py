"""
https://adventofcode.com/2019/day/9
"""

# Constants for Intcode computer modes
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


class Computer:
    """An Intcode computer that can run a program."""

    def __init__(self, program):
        # program is converted from list of integers to a {index -> integer}
        # map to support arbitrary memory assignment
        # (e.g. writing to position 1mil without the associated 0's in memory)
        self.program = {i: v for i, v in enumerate(program)}
        self.inputs = []
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
        outputs = []

        # Prevent infinite loop programs / bugs while developing
        while True:
            # parse opcode and parameter mode(s) from instruction
            # (convert integer into 5-digit string with zeroes before parsing)
            instruction = str(self.program[self.index]).zfill(5)
            opcode = int(instruction[-2:])
            param1_mode = int(instruction[-3])
            param2_mode = int(instruction[-4])
            param3_mode = int(instruction[-5])

            # opcode to halt program
            if opcode == 99:
                return outputs

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
                continue

            # opcode for input
            if opcode == 3:
                self.set_value(self.index + 1, param1_mode, self.inputs.pop(0))
                self.index += 2
                continue

            # opcode for output
            if opcode == 4:
                outputs += [self.get_value(self.index + 1, param1_mode)]
                self.index += 2
                continue

            # opcodes for jump-if-true / jump-if-false
            if opcode in (5, 6):
                val1 = self.get_value(self.index + 1, param1_mode)
                val2 = self.get_value(self.index + 2, param2_mode)

                # Should jump; update instruction pointer directly
                if (opcode == 5 and val1 != 0) or (opcode == 6 and val1 == 0):
                    self.index = val2
                    continue

                # No action, continue to next instruction
                self.index += 3
                continue

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
                continue

            # opcode for relative base offset
            if opcode == 9:
                self.relative_base += self.get_value(self.index + 1, param1_mode)
                self.index += 2
                continue

            raise Exception("unknown opcode, something went wrong")


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
    with open("data/day9.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(",")]

    computer = Computer(program)
    computer.inputs += [2]
    output = computer.process()

    print(f"Distress signal is at: {output}")


if __name__ == "__main__":
    test()
    main()
