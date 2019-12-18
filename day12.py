"""
https://adventofcode.com/2019/day/12
"""

from functools import reduce
from itertools import combinations
from math import gcd
import re
from typing import List

INPUT = """
    <x=-10, y=-13, z=7>
    <x=1, y=2, z=1>
    <x=-15, y=-3, z=13>
    <x=3, y=7, z=-4>
"""


class Point:
    """Point represents position or velocity in 3d space."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

    def __eq__(self, o):
        return all((
            self.x == o.x,
            self.y == o.y,
            self.z == o.z,
        ))

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        self.z += o.z
        return self

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def sumabs(self):
        return sum((abs(self.x), abs(self.y), abs(self.z)))


class Body:
    def __init__(self, position: Point, velocity: Point = None):
        self.position = position
        if not velocity:
            velocity = Point(0, 0, 0)
        self.velocity = velocity

    def __repr__(self):
        return f"<Body POS={self.position} VEL={self.velocity}>"

    def __eq__(self, o):
        return self.position == o.position and self.velocity == o.velocity

    def __hash__(self):
        return hash((self.position, self.velocity))

    def total_energy(self):
        return self.position.sumabs() * self.velocity.sumabs()


class Simulation:
    def __init__(self, starts: List[Point]):
        self.bodies = [Body(start) for start in starts]

    def stepn(self, n):
        for _ in range(n):
            self.step()

    def step(self):
        """Run a single step of the simulation."""
        for dim in ('x', 'y', 'z'):
            self.step_dimension(dim)

    def step_dimension(self, dim):
        """Run a single step of the simulation in one dimension (x, y, z)."""
        # Update the velocity of each moon by applying gravity.
        for body1, body2 in combinations(self.bodies, 2):
            pos1 = getattr(body1.position, dim)
            pos2 = getattr(body2.position, dim)
            # adjust velocity based on x positions
            if pos1 < pos2:
                setattr(body1.velocity, dim, getattr(body1.velocity, dim) + 1)
                setattr(body2.velocity, dim, getattr(body2.velocity, dim) - 1)
            elif pos1 > pos2:
                setattr(body1.velocity, dim, getattr(body1.velocity, dim) - 1)
                setattr(body2.velocity, dim, getattr(body2.velocity, dim) + 1)

        # Update the position of each body by applying velocity
        for body in self.bodies:
            setattr(body.position, dim, getattr(body.position, dim) + getattr(body.velocity, dim))

    def total_energy(self):
        """Return the total energy in the system."""
        return sum(body.total_energy() for body in self.bodies)

    def steps_until_repeat(self):
        """Find the first step that repeats any previous step.

        As an optimization, find the repetition cycle of each dimension
        indepently, then the total is the LCM of all dimensional cycles.
        """
        dim_steps = {}
        for dimension in ('x', 'y', 'z'):
            # Find steps before repeat for this dimension
            start = hash(tuple(self.bodies))
            index = 0
            while True:
                self.step_dimension(dimension)
                index += 1
                if hash(tuple(self.bodies)) == start:
                    dim_steps[dimension] = index
                    print(f"dim {dimension} repeats in {index}")
                    break

        return lcm(dim_steps.values())


def lcm(denoms):
    """Return the Least Common Multiple of a set of integers."""
    return reduce(lambda a, b: a*b // gcd(a, b), denoms)


def parse_ints(text: str) -> List[int]:
    return (int(num) for num in re.findall(r"-?\d+", text))


def parse_start_positions(text) -> List[Point]:
    lines = (line.strip() for line in text.strip().split("\n"))
    return [Point(*parse_ints(line)) for line in lines]


def parse_want_bodies(text) -> List[Body]:
    lines = (line.strip() for line in text.strip().split("\n"))
    numbers = (list(parse_ints(line)) for line in lines)
    return [Body(Point(*nums[:3]), Point(*nums[3:])) for nums in numbers]


def test1():
    starts = parse_start_positions("""
        <x=-1, y=0, z=2>
        <x=2, y=-10, z=-7>
        <x=4, y=-8, z=8>
        <x=3, y=5, z=-1>
    """)
    sim = Simulation(starts)

    # Start position (Step 0)
    want = parse_want_bodies("""
        pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
        pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
        pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
        pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>
    """)
    assert sim.bodies == want

    # Step 1
    sim.step()
    want = parse_want_bodies("""
        pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
        pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
        pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
        pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>
    """)
    assert sim.bodies == want

    # Step 2
    sim.step()
    want = parse_want_bodies("""
        pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
        pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
        pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
        pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>
    """)
    assert sim.bodies == want

    # Step 10
    sim.stepn(8)
    want = parse_want_bodies("""
        pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
        pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
        pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
        pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
    """)
    assert sim.bodies == want
    assert sim.total_energy() == 179

    # Step 2772 (first repeating state)
    sim.stepn(2762)
    want = parse_want_bodies("""
        pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>
    """)
    assert sim.bodies == want

    # Can calculate the first repeating state from scratch
    sim = Simulation(starts)
    assert sim.steps_until_repeat() == 2772


def test2():
    starts = parse_start_positions("""
        <x=-8, y=-10, z=0>
        <x=5, y=5, z=10>
        <x=2, y=-7, z=3>
        <x=9, y=-8, z=-3>
    """)
    sim = Simulation(starts)

    # Start position (Step 0)
    want = parse_want_bodies("""
        pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
        pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>
    """)
    assert sim.bodies == want

    # Step 10
    sim.stepn(10)
    want = parse_want_bodies("""
        pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
        pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
        pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
        pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>
    """)
    assert sim.bodies == want

    # Step 100
    sim.stepn(90)
    want = parse_want_bodies("""
        pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
        pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
        pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
        pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>
    """)
    assert sim.bodies == want
    assert sim.total_energy() == 1940

    # Can calculate the first repeating state from scratch
    sim = Simulation(starts)
    assert sim.steps_until_repeat() == 4686774924


def main():
    starts = parse_start_positions(INPUT)
    sim = Simulation(starts)
    steps = sim.steps_until_repeat()
    print(f"simulation repeasts in {steps} steps")


if __name__ == "__main__":
    test1()
    test2()
    # main()
