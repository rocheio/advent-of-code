"""
https://adventofcode.com/2019/day/10
"""

from collections import defaultdict
import math

# Constants for asteroid map symbols
EMPTY = "."
ASTEROID = "#"


def best_location(asteroid_map):
    """Return the (x, y) coordinates of the best monitoring station location.
    Best is defined as having direct line of sight to the most asteroids in the map.
    """
    all_los = get_line_of_sights(asteroid_map)
    count_los = {}
    for src, dests in all_los.items():
        # remove self-references
        dests.remove(src)
        degree_map = get_dests_by_degrees(src, dests)
        count_los[src] = len(degree_map)
    return max(count_los, key=count_los.get)


def get_line_of_sights(asteroid_map):
    """Return a {(x, y) <--> (x, y)} map of all pairs of asteroids on the map."""
    # parse the set of (x, y) coordinates that have asteroids from the map
    asteroids = set()
    for y, row in enumerate(asteroid_map.split()):
        for x, char in enumerate(row):
            if char == ASTEROID:
                asteroids.add((x, y))

    # calculate full set of (x, y) <--> (x, y) potential lines of sight (bi-directional)
    all_los = defaultdict(set)
    for src in asteroids:
        for dest in asteroids:
            all_los[src].add(dest)
            all_los[dest].add(src)

    return all_los


def get_dests_by_degrees(src, dests):
    """Return map of {degree of angle from src -> set of dest on that line}.
    Degrees are from 0 to 360, starting horizontal right and moving counter clockwise.
    """
    degree_map = defaultdict(set)
    for dest in dests:
        degree = math.degrees(math.atan2(dest[1] - src[1], dest[0] - src[0])) + 180
        degree_map[degree].add(dest)

    return degree_map


def closest_point(src, dests):
    """Return the closest (x, y) to src from a set of dests."""
    distances = {}
    for dest in dests:
        distances[dest] = math.sqrt((dest[0] - src[0]) ** 2 + (dest[1] - src[1]) ** 2)
    return min(distances, key=distances.get)


def destruction_order(asteroid_map, src, start_degree=90):
    """Return the destruction order [(x, y)...] of a lazer rotating from src."""
    all_los = get_line_of_sights(asteroid_map)
    degree_map = get_dests_by_degrees(src, all_los[src])

    # Get order of degrees asteroids will be hit on this round
    order = []
    first_round = True
    while degree_map:
        # copy degree_map so elements can be removed during loop
        check_order = sorted(degree_map)
        for degree in check_order:
            if first_round and degree < start_degree:
                continue

            dests = degree_map[degree]
            if not dests:
                del degree_map[degree]
                continue

            closest = closest_point(src, dests)

            order += [closest]
            # remove the element from the map now that it has been destroyed
            degree_map[degree].remove(closest)

        first_round = False

    return order


def test():
    asteroid_map = """
        .#..#
        .....
        #####
        ....#
        ...##
    """
    assert best_location(asteroid_map) == (3, 4)

    asteroid_map = """
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
    """
    assert best_location(asteroid_map) == (5, 8)

    asteroid_map = """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
    """
    best = best_location(asteroid_map)
    assert best == (11, 13)

    destructions = destruction_order(asteroid_map, best)
    testcases = [
        (1, (11, 12)),
        (2, (12, 1)),
        (3, (12, 2)),
        (10, (12, 8)),
        (20, (16, 0)),
        (50, (16, 9)),
        (100, (10, 16)),
        (199, (9, 6)),
        (200, (8, 2)),
        (201, (10, 9)),
        (300, (11, 1)),
    ]
    for position, want in testcases:
        assert destructions[position - 1] == want


def main():
    with open("data/day10.txt", "r") as file:
        asteroid_map = file.read()

    best = best_location(asteroid_map)
    destructions = destruction_order(asteroid_map, best)
    print(f"200th asteroid destroyed will be: {destructions[199]}")


if __name__ == "__main__":
    test()
    main()
