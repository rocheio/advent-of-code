"""
https://adventofcode.com/2019/day/8
"""


def chunks(iterable, n):
    """Return list of iterable split into list of evenly n-sized iterables."""
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]


def main():
    with open("data/day8.txt", "r") as file:
        data = file.read().splitlines()[0]

    width = 25
    height = 6

    layers = chunks(data, width*height)
    count_zeroes = {
        image: image.count("0") for image in layers
    }
    fewest = min(count_zeroes, key=count_zeroes.get)
    answer = fewest.count("1") * fewest.count("2")
    print(f"fewest zero layer has {answer} ones and twos")


if __name__ == "__main__":
    main()
