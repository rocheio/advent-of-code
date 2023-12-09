"""https://adventofcode.com/2023/day/2"""


def part1():
    """
    As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

    To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

    You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

    For example, the record of a few games might look like this:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

    The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

    Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    """
    loaded_with = {"green": 13, "red": 12, "blue": 14}
    games_possible = []
    with open("data/2023/day2.txt") as puzzle:
        for line in puzzle.readlines():
            parsed_game = parse_game(line)
            if game_is_possible(loaded_with, parsed_game):
                games_possible.append(parsed_game["game"])
    print(sum(games_possible))


def part2():
    """
    The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

    As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

    Again consider the example games from earlier:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

        In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
        Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
        Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
        Game 4 required at least 14 red, 3 green, and 15 blue cubes.
        Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

    The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

    For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
    """
    power_set_sum = 0
    with open("data/2023/day2.txt") as puzzle:
        for line in puzzle.readlines():
            parsed_game = parse_game(line)
            power_set_sum += power_of_min_cubes(parsed_game)
    print(power_set_sum)


def parse_game(value: str) -> dict:
    parsed = {"game": None, "reveals": []}

    game_str, reveal_str = value.split(":")
    parsed["game"] = int(game_str.replace("Game ", ""))

    for reveal in reveal_str.split(";"):
        reveal_counts = {}
        for number_and_color in reveal.split(","):
            number_and_color = number_and_color.strip()
            if number_and_color.endswith(" blue"):
                reveal_counts["blue"] = int(number_and_color[:-5])
            elif number_and_color.endswith(" green"):
                reveal_counts["green"] = int(number_and_color[:-6])
            elif number_and_color.endswith(" red"):
                reveal_counts["red"] = int(number_and_color[:-4])

        parsed["reveals"].append(reveal_counts)

    return parsed


def game_is_possible(loaded_with: dict, parsed_game: dict) -> bool:
    colors = ["red", "blue", "green"]
    for reveal in parsed_game["reveals"]:
        for color in colors:
            if reveal.get(color, 0) > loaded_with.get(color, 0):
                return False
    return True


def power_of_min_cubes(parsed_game: dict) -> int:
    min_cubes_required = {"green": 0, "red": 0, "blue": 0}
    for reveal in parsed_game["reveals"]:
        for color, reveal_req in reveal.items():
            if min_cubes_required[color] < reveal_req:
                min_cubes_required[color] = reveal_req
    return (
        min_cubes_required["red"]
        * min_cubes_required["blue"]
        * min_cubes_required["green"]
    )


def test():
    parsed = parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert parsed == {
        "game": 1,
        "reveals": [
            {"blue": 3, "red": 4},
            {"green": 2, "red": 1, "blue": 6},
            {"green": 2},
        ],
    }
    assert game_is_possible({"green": 13, "red": 12, "blue": 14}, parsed)
    assert not game_is_possible({"green": 1, "red": 1, "blue": 1}, parsed)

    assert power_of_min_cubes(parsed) == 48


if __name__ == "__main__":
    test()
    part1()
    part2()
