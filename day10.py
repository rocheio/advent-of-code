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
    count_los = get_los_counts(asteroid_map)
    return max(count_los, key=count_los.get)


def get_los_counts(asteroid_map):
    """Return the direct line of sight count for each (x, y) asteroid on a map."""
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

    # count number of lines of sights from each asteroid
    count_los = {}
    for src, dests in all_los.items():
        # remove self-reference
        dests.remove(src)

        # convert src / list of dests into map of:
        # {degree of angle -> set of coordinates on that line}
        degrees_to_dests = defaultdict(set)
        for dest in dests:
            degree = math.atan2(dest[1] - src[1], dest[0] - src[0])
            degrees_to_dests[degree].add(dest)

        # for now we just need to know the distinct lines of sights
        count_los[src] = len(degrees_to_dests)

    return count_los


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
    assert best_location(asteroid_map) == (11, 13)


def main():
    with open("data/day10.txt", "r") as file:
        asteroid_map = file.read()

    count_los = get_los_counts(asteroid_map)
    best = max(count_los, key=count_los.get)
    print(f"best location is: {best} with count: {count_los[best]}")


if __name__ == "__main__":
    test()
    main()
