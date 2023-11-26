"""https://adventofcode.com/2015/day/5"""


def is_string_nice_p1(value: str) -> bool:
    vowels = "aeiou"
    invalid = {"ab", "cd", "pq", "xy"}

    count_vowels = 0
    last_letter = None
    has_double_letters = False

    for letter in value:
        if letter in vowels:
            count_vowels += 1

        if letter == last_letter:
            has_double_letters = True

        if last_letter and last_letter + letter in invalid:
            return False

        last_letter = letter

    return count_vowels >= 3 and has_double_letters


def is_string_nice_p2(value: str) -> bool:
    has_two_letter_pair_no_overlap = False
    has_letter_pair_with_one_in_middle = False

    pairs_seen = set()
    count_same_letter_in_a_row = 1

    letter_2_back = None
    letter_1_back = None

    for letter in value:
        if letter == letter_1_back:
            count_same_letter_in_a_row += 1
        else:
            count_same_letter_in_a_row = 1

        # It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
        if letter_2_back == letter:
            has_letter_pair_with_one_in_middle = True

        # It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
        # NOTE: `aaaa` WILL count and needs to not be filtered out by exclusion logic
        # Effectively, 3 of the same letter in a row is no good, but 4+ is fine
        if letter_1_back:
            current_pair = letter_1_back + letter
            if current_pair in pairs_seen and count_same_letter_in_a_row != 3:
                has_two_letter_pair_no_overlap = True

            pairs_seen.add(current_pair)

        letter_2_back = letter_1_back
        letter_1_back = letter

    return has_two_letter_pair_no_overlap and has_letter_pair_with_one_in_middle


def puzzle_input() -> list:
    with open("data/2015/day5.txt") as stream:
        return [line for line in stream.readlines() if line]


def part_1():
    """
    Santa needs help figuring out which strings in his text file are naughty or nice.

    How many strings are nice?
    """
    count_nice_strings = 0
    for line in puzzle_input():
        if is_string_nice_p1(line):
            count_nice_strings += 1
    print(count_nice_strings)


def part_2():
    """
    Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

    How many strings are nice under these new rules?
    """
    count_nice_strings = 0
    for line in puzzle_input():
        if is_string_nice_p2(line):
            count_nice_strings += 1
    print(count_nice_strings)


def test():
    assert is_string_nice_p1("ugknbfddgicrmopn")
    assert is_string_nice_p1("aaa")
    assert not is_string_nice_p1("jchzalrnumimnmhp")
    assert not is_string_nice_p1("haegwjzuvuyypxyu")
    assert not is_string_nice_p1("dvszwmarrgswjxmb")
    assert is_string_nice_p2("qjhvhtzxzqqjkmpb")
    assert is_string_nice_p2("xxyxx")
    assert is_string_nice_p2("aaaa")
    assert not is_string_nice_p2("aaa")
    assert not is_string_nice_p2("uurcxstgmygtbstg")
    assert not is_string_nice_p2("ieodomkazucvgmuy")


if __name__ == "__main__":
    test()
    part_1()
    part_2()
