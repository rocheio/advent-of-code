"""
https://adventofcode.com/2019/day/1
"""


def fuel_needed(mass):
    """Return total mass of fuel required to launch a mass including added fuel."""
    total_fuel = 0
    new_fuel = fuel_calc(mass)
    while new_fuel > 0:
        total_fuel += new_fuel
        new_fuel = fuel_calc(new_fuel)
    return total_fuel


def fuel_calc(mass):
    """Return mass of fuel directly needed to launch a mass."""
    return int(mass / 3) - 2


def test():
    assert fuel_needed(12) == 2
    assert fuel_needed(14) == 2
    assert fuel_needed(1969) == 966
    assert fuel_needed(100756) == 50346


def main():
    total_fuel = 0
    with open("data/day1.txt", "r") as file:
        for line in file:
            total_fuel += fuel_needed(int(line))
    print(f"total fuel needed: {total_fuel}")


if __name__ == "__main__":
    test()
    main()
