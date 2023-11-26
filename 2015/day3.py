"""https://adventofcode.com/2015/day/3"""



def houses_visited(moves: str) -> int:
    """
    Santa is delivering presents to an infinite two-dimensional grid of houses.

    He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

    However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?
    """
    coords_seen = set()
    x = 0
    y = 0

    coords_seen.add((x, y))
    for move in moves:
        if move == ">":
            x += 1
        if move == "<":
            x -= 1
        if move == "^":
            y += 1
        if move == "v":
            y -= 1
        coords_seen.add((x, y))

    return len(coords_seen)


def houses_visited_with_robot(moves: str) -> int:
    """
    The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

    Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

    This year, how many houses receive at least one present?
    """
    coords_seen = set()
    sx = 0
    sy = 0
    rx = 0
    ry = 0

    coords_seen.add((sx, sy))
    for index, move in enumerate(moves):
        move_santa = index % 2 == 0
        if move == ">":
            if move_santa:
                sx += 1
            else:
                rx += 1
        if move == "<":
            if move_santa:
                sx -= 1
            else:
                rx -= 1
        if move == "^":
            if move_santa:
                sy += 1
            else:
                ry += 1
        if move == "v":
            if move_santa:
                sy -= 1
            else:
                ry -= 1

        if move_santa:
            coords_seen.add((sx, sy))
        else:
            coords_seen.add((rx, ry))

    return len(coords_seen)


def test():
    assert houses_visited(">") == 2
    assert houses_visited("^>v<") == 4
    assert houses_visited("^v^v^v^v^v") == 2
    assert houses_visited_with_robot("^v") == 3
    assert houses_visited_with_robot("^>v<") == 3
    assert houses_visited_with_robot("^v^v^v^v^v") == 11


if __name__ == "__main__":
    test()

    with open("data/2015/day3.txt") as stream:
        data = stream.read()

    print(houses_visited(data))
    print(houses_visited_with_robot(data))
