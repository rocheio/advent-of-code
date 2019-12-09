"""
https://adventofcode.com/2019/day/6
"""

def new_orbit_map(orbit_paths):
    """Return a map of {orbiting obj} -> {obj it orbits} from text."""
    orbit_map = {}  # orbiting object -> object it orbits
    for row in orbit_paths:
        center, orbiter = row.split(")")
        if orbiter in orbit_map:
            raise ValueError(f"object {orbiter} can only have on center")
        orbit_map[orbiter] = center
    return orbit_map


def orbit_count_checksum(orbit_map):
    return sum(total_orbits(orbit_map, orbiter) for orbiter in orbit_map)


def total_orbits(orbit_map, orbiter):
    total_orbits = 0
    while total_orbits < len(orbit_map):
        try:
            orbiter = orbit_map[orbiter]
            total_orbits += 1
        except KeyError:
            return total_orbits


def path_to_com(orbit_map, start):
    """Return the direct path of objects from start to COM."""
    path = []
    current = start
    while current != "COM":
        current = orbit_map[current]
        path += [current]
    return path


def path_to_obj(orbit_map, start, end):
    """Return the path of transfers from start to end."""
    path1 = path_to_com(orbit_map, start)
    path2 = path_to_com(orbit_map, end)

    # Find the first shared object on path to COM
    first_shared = "COM"
    for val1, val2 in zip(reversed(path1), reversed(path2)):
        if val1 != val2:
            break
        first_shared = val1

    # Create the full path from [start -> first_shared -> end]
    path = path1[:path1.index(first_shared)+1]
    path += list(reversed(path2[:path2.index(first_shared)]))
    return path


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
    assert orbit_count_checksum(new_orbit_map(orbit_paths)) == 42

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
        "K)YOU",
        "I)SAN",
    ]
    path = path_to_obj(new_orbit_map(orbit_paths), "YOU", "SAN")
    assert len(path) - 1 == 4


def main():
    with open("data/day6.txt", "r") as file:
        orbit_paths = file.read().splitlines()
    orbit_map = new_orbit_map(orbit_paths)
    path = path_to_obj(orbit_map, "YOU", "SAN")
    print(f"minimum orbital transfer number is: {len(path) - 1}")


if __name__ == "__main__":
    test()
    main()
