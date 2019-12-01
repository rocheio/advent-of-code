"""
https://adventofcode.com/2019/day/1
"""


def fuel_needed(mass):
    """Return total mass of fuel required to launch a mass including added fuel."""
    fuel_for_mass = fuel_calc(mass)
    if fuel_for_mass < 0:
        return 0
    return fuel_for_mass + fuel_needed(fuel_for_mass)


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
