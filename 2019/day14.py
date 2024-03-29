"""
https://adventofcode.com/2019/day/14
"""

from collections import defaultdict
import math
from queue import Queue


MAX_ORE = 1000000000000


def parse_ingredient(text):
    """Return a (chemical, quantity) tuple from a text ingredient in a reaction."""
    parts = text.split(" ")
    return (parts[1], int(parts[0]))


def parse_reactions(text):
    """Return map of ingredient inputs to reactions that make them
    e.g. {(ingredient...): (ingredient...)}
    """
    reactions = {}
    for line in text.strip().splitlines():
        inputs, output = line.split(" => ")
        reactions[parse_ingredient(output)] = [
            parse_ingredient(inp) for inp in inputs.strip().split(", ")
        ]
    return reactions


def get_min_reaction(reactions, chemical):
    """Return the minimum reaction that can create the chemical."""
    matches = [ingr for ingr in reactions if ingr[0] == chemical]
    match = min(matches, key=lambda x: x[1])
    return match, reactions[match]


def ore_for_fuel(reactions, want_fuel=1):
    # Create a map of {chemical: quantity} on hand
    # ORE is tracked separately from all other chems
    stock = defaultdict(int)
    ore_needed = 0
    orders = Queue()
    orders.put({"chemical": "FUEL", "quantity": want_fuel})

    # Work "backwards" from desired chemicals to ingredients using
    # reactions until only ORE is left which we have infinite of.
    while not orders.empty():
        order = orders.get()

        # account for ORE separately
        if order["chemical"] == "ORE":
            ore_needed += order["quantity"]
            continue

        # use stock if it already exists
        if stock[order["chemical"]] >= order["quantity"]:
            stock[order["chemical"]] -= order["quantity"]
            continue

        # otherwise, put in an order to make more
        needed = order["quantity"] - stock[order["chemical"]]
        output, inputs = get_min_reaction(reactions, order["chemical"])
        batches = math.ceil(needed / output[1])
        for chem, quant in inputs:
            orders.put({"chemical": chem, "quantity": quant * batches})

        # add leftovers to stock
        leftover = batches * output[1] - needed
        stock[output[0]] = leftover

    return ore_needed


def max_fuel(reactions):
    """Run a binary search to see how much fuel can be made with MAX_ORE."""
    min_fuel = 0
    max_fuel = 100000000
    while (max_fuel - min_fuel) > 1:
        pointer = (max_fuel + min_fuel) // 2
        ore = ore_for_fuel(reactions, pointer)
        if ore <= MAX_ORE:
            min_fuel = pointer
        else:
            max_fuel = pointer

    return min_fuel


def test():
    formulas = """
        10 ORE => 10 A
        1 ORE => 1 B
        7 A, 1 B => 1 C
        7 A, 1 C => 1 D
        7 A, 1 D => 1 E
        7 A, 1 E => 1 FUEL
    """
    assert ore_for_fuel(parse_reactions(formulas)) == 31

    formulas = """
        9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL
    """
    assert ore_for_fuel(parse_reactions(formulas)) == 165

    formulas = """
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
    """
    reactions = parse_reactions(formulas)
    assert ore_for_fuel(reactions) == 13312
    assert max_fuel(reactions) == 82892753

    formulas = """
        2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF
    """
    reactions = parse_reactions(formulas)
    assert ore_for_fuel(reactions) == 180697
    assert max_fuel(reactions) == 5586022

    formulas = """
        171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX
    """
    reactions = parse_reactions(formulas)
    assert ore_for_fuel(reactions) == 2210736
    assert max_fuel(reactions) == 460664


def main():
    with open("data/day14.txt", "r") as file:
        formulas = file.read()
    reactions = parse_reactions(formulas)
    print(f"max fuel from ore is: {max_fuel(reactions)}")


if __name__ == "__main__":
    test()
    main()
