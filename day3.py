"""
https://adventofcode.com/2019/day/3
"""


def path_to_trail(path):
    """Walk a path starting at (0,0) and return a list of each coordinate hit along the way."""
    trail = []
    current = (0, 0)
    trail += [current]
    for step in path:
        coords = coords_between(current, step)
        trail += coords
        current = coords[-1]
    return trail


def coords_between(current, step):
    """Return all (x,y) coordinate pairs from applying a step from current coords.
    The last step in the returned list is the new current position.
    """
    coords_between = []

    x, y = current
    direction = step[0]
    distance = int(step[1:])

    for _ in range(1, distance+1):
        if direction == "U":
            y += 1
        elif direction == "D":
            y -= 1
        elif direction == "L":
            x -= 1
        elif direction == "R":
            x += 1
        coords_between += [(x, y)]

    return coords_between


def manhattan_distance(path1, path2):
    """Return the smallest Manhattan distance from (0, 0) where two wire paths cross."""
    # Convert each path into a list of locations it passed through
    trail1 = path_to_trail(path1)
    trail2 = path_to_trail(path2)

    # Find all locations that exist in each trail
    collisions = set(trail1) & set(trail2)
    # Origin does not count as an intersection
    collisions -= {(0, 0)}
    # Convert all collisions into distances from origin
    distances = [abs(x) + abs(y) for x, y in collisions]
    return min(distances)


def test():
    path1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
    path2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]
    assert manhattan_distance(path1, path2) == 159

    path1 = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
    path2 = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
    assert manhattan_distance(path1, path2) == 135


def main():
    # Convert text input into two lists of wire paths
    with open("data/day3.txt", "r") as file:
        paths = [path.strip().split(",") for path in file.readlines()]
    distance = manhattan_distance(*paths)
    print(f"closest manhattan distance is: {distance}")


if __name__ == "__main__":
    test()
    main()
