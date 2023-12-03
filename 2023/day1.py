"""https://adventofcode.com/2023/day/1"""


WORDS_TO_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def first_number_in_string(value: str) -> int:
    for i in range(len(value)):
        if value[i].isdigit():
            return int(value[i])

        for num_chars in (3, 4, 5):
            testword = value[i : i + num_chars]
            if testword in WORDS_TO_DIGITS:
                return WORDS_TO_DIGITS[testword]


def last_number_in_string(value: str) -> int:
    rev_lookup = {str(reversed(k)): v for k, v in WORDS_TO_DIGITS.items()}
    for i in range(len(value) - 1, -1, -1):
        if value[i].isdigit():
            return int(value[i])

        for num_chars in (3, 4, 5):
            testword = value[i - num_chars + 1 : i + 1]
            if testword in WORDS_TO_DIGITS:
                return WORDS_TO_DIGITS[testword]


def calibration_value(value: str) -> int:
    value = value.strip()
    if not value:
        return 0

    first_num = None
    last_num = None
    for char in value:
        if not char.isdigit():
            continue
        if first_num is None:
            first_num = char
        last_num = char

    return int(first_num + last_num)


def calibration_with_words(value: str) -> int:
    return int(str(first_number_in_string(value)) + str(last_number_in_string(value)))


def part1():
    """
    As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

    The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

    In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

    Consider your entire calibration document. What is the sum of all of the calibration values?
    """
    calibration_sum = 0
    with open("data/2023/day1.txt") as data:
        for line in data.readlines():
            calibration_sum += calibration_value(line)
    print(calibration_sum)


def part2():
    """
    Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

    Equipped with this new information, you now need to find the real first and last digit on each line. For example:

    What is the sum of all of the calibration values?
    """
    calibration_sum = 0
    with open("data/2023/day1.txt") as data:
        for line in data.readlines():
            calibration_sum += calibration_with_words(line)
    print(calibration_sum)


def test():
    assert calibration_value("1abc2") == 12
    assert calibration_value("pqr3stu8vwx") == 38
    assert calibration_value("a1b2c3d4e5f") == 15
    assert calibration_value("treb7uchet") == 77

    # Part 2

    assert first_number_in_string("two1nine") == 2
    assert first_number_in_string("eightwothree") == 8
    assert last_number_in_string("two1nine") == 9
    assert last_number_in_string("eightwothree") == 3

    assert calibration_with_words("two1nine") == 29
    assert calibration_with_words("eightwothree") == 83
    assert calibration_with_words("abcone2threexyz") == 13
    assert calibration_with_words("xtwone3four") == 24
    assert calibration_with_words("4nineeightseven2") == 42
    assert calibration_with_words("zoneight234") == 14
    assert calibration_with_words("7pqrstsixteen") == 76
    assert calibration_with_words("eightwo") == 82


if __name__ == "__main__":
    test()
    part1()
    part2()
