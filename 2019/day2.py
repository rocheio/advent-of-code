"""
https://adventofcode.com/2019/day/2
"""


from copy import deepcopy


def process(program):
    for index in range(0, len(program), 4):
        opcode = program[index]
        if opcode == 99:
            # opcode to exit normally
            break

        val1 = program[program[index + 1]]
        val2 = program[program[index + 2]]
        dest = program[index + 3]

        if opcode == 1:
            program[dest] = val1 + val2
            continue

        if opcode == 2:
            program[dest] = val1 * val2
            continue

        raise Exception("unknown opcode, something went wrong")


def set_input_1202(program):
    """Adjust the program to the 1202 state before running."""
    set_input(program, 12, 2)


def set_input(program, noun, verb):
    """Set the initial state of a program."""
    program[1] = noun
    program[2] = verb


def find_inputs(program, want_output):
    """Return the (noun, verb) pair that produces want_output from a program."""
    for noun in range(0, 100):
        for verb in range(0, 100):
            instance = deepcopy(program)
            set_input(instance, noun, verb)
            process(instance)
            if instance[0] == want_output:
                print(f"noun {noun} and verb {verb} produce {want_output}")
                return noun, verb

    raise Exception(f"no noun/verb combination between 0-99 produces {want_output}")


def test():
    testcases = [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
    ]
    for program, expected in testcases:
        process(program)
        assert program == expected


def main():
    # Convert the text program into a list of integers (Intcode)
    with open("data/day2.txt", "r") as file:
        text = file.read().strip()
    program = [int(number) for number in text.split(",")]

    # Find the noun / verb inputs that produce the wanted output
    noun, verb = find_inputs(program, want_output=19690720)
    print(f"answer is: {100 * noun + verb}")


if __name__ == "__main__":
    test()
    main()
