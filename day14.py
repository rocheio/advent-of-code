"""
https://adventofcode.com/2019/day/14
"""

from collections import defaultdict


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


def ore_for_fuel(reactions):
    # Create a map of {chemical: quantity} on hand
    # Use negative numbers to represent desired amounts
    chemicals = defaultdict(lambda: 0)
    chemicals["FUEL"] -= 1

    # Work "backwards" from desired chemicals to ingredients using
    # reactions until only ORE is left which we have infinite of.
    while True:
        # Find chemicals we still need to convert
        need_chems = {
            chem: quant for chem, quant in chemicals.items()
            if chem != "ORE" and quant < 0
        }
        if not need_chems:
            return chemicals["ORE"] * -1

        # Look for reactions that could create the chemicals we want
        for chem, quant in need_chems.items():
            output, inputs = get_min_reaction(reactions, chem)
            # "perform" the reaction and now want ingredients
            chemicals[chem] += output[1]
            for rchem, rquant in inputs:
                chemicals[rchem] -= rquant


def test():
    testcases = [
        # ORE expected, formulas
        (31, """
            10 ORE => 10 A
            1 ORE => 1 B
            7 A, 1 B => 1 C
            7 A, 1 C => 1 D
            7 A, 1 D => 1 E
            7 A, 1 E => 1 FUEL
        """),
        (165, """
            9 ORE => 2 A
            8 ORE => 3 B
            7 ORE => 5 C
            3 A, 4 B => 1 AB
            5 B, 7 C => 1 BC
            4 C, 1 A => 1 CA
            2 AB, 3 BC, 4 CA => 1 FUEL
        """),
        (13312, """
            157 ORE => 5 NZVS
            165 ORE => 6 DCFZ
            44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
            12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
            179 ORE => 7 PSHF
            177 ORE => 5 HKGWZ
            7 DCFZ, 7 PSHF => 2 XJWVT
            165 ORE => 2 GPVTF
            3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
        """),
        (180697, """
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
        """),
        (2210736, """
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
        """),
    ]
    for expected, formulas in testcases:
        assert ore_for_fuel(parse_reactions(formulas)) == expected


def main():
    with open("data/day14.txt", "r") as file:
        formulas = file.read()
    reactions = parse_reactions(formulas)
    ore = ore_for_fuel(reactions)
    print(f"ore required: {ore}")


if __name__ == "__main__":
    test()
    main()
