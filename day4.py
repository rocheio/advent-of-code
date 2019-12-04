"""
https://adventofcode.com/2019/day/4
"""

PUZZLE_INPUT = "367479-893698"


def maybe_valid_password(number):
    """Return True if a number is a potentially valid password."""
    digits = str(number)
    repeating_numbers = False
    previous = digits[0]
    for current in digits[1:]:
        if current < previous:
            return False
        if current == previous:
            repeating_numbers = True
        previous = current
    return repeating_numbers


def test():
    assert maybe_valid_password(111111)
    assert not maybe_valid_password(223450)
    assert not maybe_valid_password(123789)


def main():
    potential_passwords = []
    valid_range = [int(val) for val in PUZZLE_INPUT.split("-")]
    for number in range(valid_range[0], valid_range[1]+1):
        if maybe_valid_password(number):
            potential_passwords += [number]
    print(f"total number of potential passwords is: {len(potential_passwords)}")


if __name__ == "__main__":
    test()
    main()
