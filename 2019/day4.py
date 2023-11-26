"""
https://adventofcode.com/2019/day/4
"""

PUZZLE_INPUT = "367479-893698"


def maybe_valid_password(number):
    """Return True if a number is a potentially valid password."""
    # Track the count of times numbers repeat
    count_repeatings = []
    digits = str(number)

    count_repeatings += [1]
    previous = digits[0]
    for current in digits[1:]:
        # Digits in password must never decrease
        if current < previous:
            return False

        if current == previous:
            count_repeatings[-1] += 1
        else:
            count_repeatings += [1]

        previous = current

    return 2 in count_repeatings


def test():
    assert maybe_valid_password(112233)
    assert not maybe_valid_password(123444)
    assert maybe_valid_password(111122)


def main():
    potential_passwords = []
    valid_range = [int(val) for val in PUZZLE_INPUT.split("-")]
    for number in range(valid_range[0], valid_range[1] + 1):
        if maybe_valid_password(number):
            potential_passwords += [number]
    print(f"total number of potential passwords is: {len(potential_passwords)}")


if __name__ == "__main__":
    test()
    main()
