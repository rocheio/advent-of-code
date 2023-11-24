"""
https://adventofcode.com/2019/day/8
"""

# Color constants
BLACK = "0"
WHITE = "1"
TRANSPARENT = "2"


def chunks(iterable, n):
    """Return list of iterable split into list of evenly n-sized iterables."""
    return [iterable[i:i+n] for i in range(0, len(iterable), n)]


def decode_image(data, width, height):
    """Return a list of strings representing the fully decoded image."""
    layers = [chunks(layer, width) for layer in chunks(data, width*height)]
    output = []
    # Process all layers for each cell in the image
    for row in zip(*layers):
        output_row = ""
        for cell in zip(*row):
            output_row += decode_cell_layers(cell)
        output += [output_row]
    return output


def decode_cell_layers(cell):
    """Return the processed image color for a cell.
    Cell data is a tuple of string integers for each layer from top-to-bottom.
    """
    for pixel in cell:
        if pixel == TRANSPARENT:
            continue
        return pixel
    return TRANSPARENT


def test():
    data = "0222112222120000"
    width = 2
    height = 2
    want = [
        "01",
        "10"
    ]
    assert decode_image(data, width, height) == want


def main():
    with open("data/day8.txt", "r") as file:
        data = file.read().splitlines()[0]

    width = 25
    height = 6
    image = decode_image(data, width, height)
    for row in image:
        print(row.replace(BLACK, " "))


if __name__ == "__main__":
    test()
    main()
