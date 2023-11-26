"""https://adventofcode.com/2015/day/4"""

import hashlib

INPUT = "yzbqklnj"


def md5_lowest_start(value: str, target="00000") -> int:
    i = 1
    while True:
        hashed = hashlib.md5((value + str(i)).encode())
        if hashed.hexdigest().startswith(target):
            return i
        i += 1


def part_1():
    """
    Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

    To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.
    """
    print(md5_lowest_start(INPUT))


def part_2():
    """Now find one that starts with six zeroes."""
    print(md5_lowest_start(INPUT, target="000000"))


def test():
    assert md5_lowest_start("abcdef") == 609043
    assert md5_lowest_start("pqrstuv") == 1048970


if __name__ == "__main__":
    test()
    part_1()
    part_2()
