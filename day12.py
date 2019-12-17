"""
https://adventofcode.com/2019/day/12
"""

from collections import namedtuple
from itertools import combinations
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
        # Update the velocity of each moon by applying gravity.
        # Each body is pulled toward each other body by 1 on each (x, y) axis
        for body1, body2 in combinations(self.bodies, 2):
            # adjust velocity based on x positions
            if body1.position.x < body2.position.x:
                body1.velocity.x += 1
                body2.velocity.x -= 1
            elif body1.position.x > body2.position.x:
                body1.velocity.x -= 1
                body2.velocity.x += 1

            # adjust velocity based on y positions
            if body1.position.y < body2.position.y:
                body1.velocity.y += 1
                body2.velocity.y -= 1
            elif body1.position.y > body2.position.y:
                body1.velocity.y -= 1
                body2.velocity.y += 1

            # adjust velocity based on z positions
            if body1.position.z < body2.position.z:
                body1.velocity.z += 1
                body2.velocity.z -= 1
            elif body1.position.z > body2.position.z:
                body1.velocity.z -= 1
                body2.velocity.z += 1

        # Update the position of each body by applying velocity
        for body in self.bodies:
            body.position += body.velocity

    def total_energy(self):
        """Return the total energy in the system."""
        return sum(body.total_energy() for body in self.bodies)


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


def main():
    starts = parse_start_positions(INPUT)
    sim = Simulation(starts)
    sim.stepn(1000)
    print(f"total energy in system after 1000 steps is: {sim.total_energy()}")


if __name__ == "__main__":
    test1()
    test2()
    main()
