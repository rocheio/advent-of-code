"""https://adventofcode.com/2015/day/2"""


def present_wrapping_paper(l: int, w: int, h: int) -> int:
    """
    The elves are running low on wrapping paper, and so they need to submit an order for more. They have a list of the dimensions (length l, width w, and height h) of each present, and only want to order exactly as much as they need.

    Fortunately, every present is a box (a perfect right rectangular prism), which makes calculating the required wrapping paper for each gift a little easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also need a little extra paper for each present: the area of the smallest side.

    All numbers in the elves' list are in feet. How many total square feet of wrapping paper should they order?
    """
    side1 = l * w
    side2 = w * h
    side3 = l * h
    area = 2 * side1 + 2 * side2 + 2 * side3
    extra = min((side1, side2, side3))
    return area + extra


def present_ribbon(l: int, w: int, h: int) -> int:
    """
    The elves are also running low on ribbon. Ribbon is all the same width, so they only have to worry about the length they need to order, which they would again like to be exact.

    The ribbon required to wrap a present is the shortest distance around its sides, or the smallest perimeter of any one face. Each present also requires a bow made out of ribbon as well; the feet of ribbon required for the perfect bow is equal to the cubic feet of volume of the present. Don't ask how they tie the bow, though; they'll never tell.

    How many total feet of ribbon should they order?
    """
    sorted_sides = list(sorted((l, w, h)))
    min_perim = sorted_sides[0] * 2 + sorted_sides[1] * 2
    bow_len = l * w * h
    return min_perim + bow_len


def test():
    assert present_wrapping_paper(2, 3, 4) == 58
    assert present_wrapping_paper(1, 1, 10) == 43
    assert present_ribbon(2, 3, 4) == 34
    assert present_ribbon(1, 1, 10) == 14


def dimensions_from_string(data: str) -> list:
    dimensions = []
    for value in data.split():
        if not value:
            continue

        dimensions.append([int(num) for num in value.split("x")])

    return dimensions


if __name__ == "__main__":
    test()

    with open("data/2015/day2.txt") as data:
        dimensions = dimensions_from_string(data.read())

    print(sum(present_wrapping_paper(*dim) for dim in dimensions))
    print(sum(present_ribbon(*dim) for dim in dimensions))
