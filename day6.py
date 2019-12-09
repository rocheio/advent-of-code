"""
https://adventofcode.com/2019/day/6
"""

def orbit_count_checksum(orbit_paths):
    orbit_map = {}  # orbiting object -> object it orbits
    for row in orbit_paths:
        center, orbiter = row.split(")")
        if orbiter in orbit_map:
            raise ValueError(f"object {orbiter} can only have on center")
        orbit_map[orbiter] = center

    return sum(total_orbits(orbit_map, orbiter) for orbiter in orbit_map)


def total_orbits(orbit_map, orbiter):
    total_orbits = 0
    while total_orbits < len(orbit_map):
        try:
            orbiter = orbit_map[orbiter]
            total_orbits += 1
        except KeyError:
            return total_orbits


def test():
    orbit_paths = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    assert orbit_count_checksum(orbit_paths) == 42


def main():
    with open("data/day6.txt", "r") as file:
        orbit_paths = file.read().splitlines()
    checksum = orbit_count_checksum(orbit_paths)
    print(f"checksum of orbit paths is: {checksum}")


if __name__ == "__main__":
    test()
    main()
