import typing

import gtravyl as gt
import numpy as np

def test_basic():
    world = np.array([[0, 0, 0, 1, 1, 1, 1],
                      [0, 0, 0, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 1, 1, 1, 0]])
    typing.cast(list[list[int]], world)
    path = gt.shortest_path(world, (0, 0), (4, 6))
    for cell in path:
        world[cell] = 2

    assert np.array_equal(world, np.array([[2, 2, 2, 1, 1, 1, 1],
                                           [0, 0, 2, 1, 1, 1, 1],
                                           [0, 0, 2, 2, 2, 2, 2],
                                           [1, 1, 0, 1, 1, 1, 2],
                                           [1, 1, 0, 1, 1, 1, 2]]))
