from collections import defaultdict
from math import sqrt
from heapq import heappush, heappop
from typing import Any

import numpy as np
import numpy.typing as npt


def in_bounds(pt: tuple[int, int], dim: tuple[int, int]) -> bool:
    """Checks if the candidate point actually exists in the grid.

    :param pt: The point to check if it is in bounds.
    :param dim: Dimensions (row, column) of the grid.
    """
    return 0 <= pt[0] < dim[0] and 0 <= pt[1] < dim[1]


def no_wrap(ind: tuple[int, int], dim: tuple[int, int]) -> tuple[int, int]:
    """Does not wrap indices. Essentially does nothing in this case.

    :param ind: Needed for type signature. This function is equivalent to:
       id(ind) -> ind
    :param dim: Needed for type signature, it is otherwise ignored.
    """
    return ind

def wrap(ind: tuple[int, int], dim: tuple[int, int]) -> tuple[int, int]:
    """Wraps the cell values around. So, if you start at (0, 0) and go left you
    end up at (x dimension, 0)
    :param ind: The index to potentially modify (that is, wrap it if 
       applicable).
    :param dim: Dimensions of the grid.
    """
    return ind[0] % dim[0], ind[1] % dim[1]


def unit_dist(ind1: tuple[int, int], ind2: tuple[int, int],
              value1: Any, value2: Any):
    """Every neighbor is ``1`` unit distant from the other."""
    return 1

def euclidean_dist(ind1: tuple[int, int], ind2: tuple[int, int],
              value1: Any, value2: Any):
    """Neighbor indices are computed under the standard Euclidean distance.

    :param ind1: Location in Euclidean space for the first point.
    :param ind2: Location in Euclidean space for the second point.
    :param value1: Needed for type signature, essentially ignored.
    :param value2: Needed for type signature, essentially ignored.
    """
    return sqrt((ind1[0] - ind2[0]) ** 2 + (ind1[1] - ind2[1]) ** 2)


def vn_neighbors(ind: tuple[int, int], 
                 grid: npt.NDArray,
                 wrap=no_wrap):
    """Return the von Neumann neighborhood of a particular cell in the grid.

    :param ind: Index to compute von Neumann neighborhood of.
    :param grid: The grid ``ind`` belongs to.
    """
    shape = (len(grid), len(grid[0]))
    left = wrap((ind[0] - 1, ind[1]), shape)
    right = wrap((ind[0] + 1, ind[1]), shape)
    up = wrap((ind[0], ind[1] - 1), shape)
    down = wrap((ind[0], ind[1] + 1), shape)
    nbs = [left, right, up, down]
    nbs = filter(lambda x: in_bounds(x, shape), nbs)
    return nbs

def moore_neighbors(ind: tuple[int, int],
                    grid: npt.NDArray,
                    wrap=no_wrap):
    """Return the Moore neighborhood of a particular cell in the grid.

    :param ind: Index to compute Moore neighborhood of.
    :param grid: The grid ``ind`` belongs to.
    """
    shape = (len(grid), len(grid[0]))
    left_tcorner = wrap((ind[0] - 1, ind[1] + 1), shape)
    left = wrap((ind[0] - 1, ind[1]), shape)
    left_bcorner = wrap((ind[0] - 1, ind[1] - 1), shape)
    right_tcorner = wrap((ind[0] + 1, ind[1] + 1), shape)
    right = wrap((ind[0] + 1, ind[1]), shape)
    right_bcorner = wrap((ind[0] + 1, ind[1] - 1), shape)
    up = wrap((ind[0], ind[1] - 1), shape)
    down = wrap((ind[0], ind[1] + 1), shape)
    nbs = [left_tcorner, left, left_bcorner,
           right_tcorner, right, right_bcorner,
           up, down]
    nbs = filter(lambda x: in_bounds(x, shape), nbs)
    return nbs


def not_one(value: Any):
    """Checks if a value is not 1. You can think of 1 as though there is a wall
    and you are *not* allowed to traverse there. Any other value is fine. (This
    is the default function for the keyword argument ``allowed`` of
    ``shortest_path``.

    :param value: Value to check.
    """
    return value != 1


def no_heuristic(cur: tuple[int, int], t: tuple[int, int], 
                 grid: npt.NDArray):
    return 0

def euclid_heuristic(cur: tuple[int, int], t: tuple[int, int],
                     grid: npt.NDArray):
    return sqrt((cur[0] - t[0]) ** 2 + (cur[1] - t[1]) ** 2)


def shortest_path(grid: npt.NDArray,
                  si: tuple[int, int] | None = None, 
                  ti: tuple[int, int] | None = None,
                  sv: Any | None = None,
                  tv: Any | None = None,
                  neighbors=vn_neighbors,
                  allowed=not_one,
                  wrap=no_wrap,
                  dist=unit_dist,
                  heuristic=no_heuristic) -> list[tuple[int, int]]:
    """Find shortest path from ``s`` to ``t`` in a given `grid`.

    :param grid: grid (2d array) representation of the world to traverse.
    :param si: The "source" index, i.e. where the path search starts.
    :param ti: The "destination" index, i.e. where the path should end.
    :param sv: The "source" value, i.e. the value of the start index.
    :param tv: The "destination" value, i.e. the value of the end index.
    :param neighbors: Computes the neighborhood of any choice of index in the
       grid.
    :param wrap: Does the grid wrap around. Defaults to no wrap.
    :param dist: The distance function used. Defaults to unit distance.
    """
    i1 = None
    i2 = None
    if sv is not None:
        i1 = np.where(grid == sv)[0][0]
    if tv is not None:
        i2 = np.where(grid == tv)[0][0]
    s, t = i1 or si, i2 or ti
    assert type(s) is tuple
    assert type(t) is tuple
    assert len(s) == 2
    assert len(t) == 2
    assert type(s[0]) is int
    assert type(s[1]) is int
    assert type(t[0]) is int
    assert type(t[1]) is int
    # Keep track of which nodes need to be explored.
    frontier = []
    scores = defaultdict(lambda: float('inf')) # candidate -> current 
                                               # best score (ultimately,
                                               # best score)
    parents = {} # candidate -> parent (in particular, the parent with the
                 # shortest path to s.
    seen = set() # Keeps track of already seen indices.
    # Push the node (and it's parent)
    # NOTE s has no parent thus it is set to None.
    heappush(frontier, (0 + heuristic(s, t, grid), s))
    parents[s] = None
    while frontier:
        (score, candidate) = heappop(frontier)
        seen.add(candidate)
        if score > scores[t]:
            continue
        for nb in neighbors(candidate, grid, wrap=wrap):
            if nb not in seen and allowed(grid[nb[0]][nb[1]]):
                d = dist(candidate, nb, 
                         grid[candidate[0]][candidate[1]], grid[nb[0]][nb[1]])
                if score + d < scores[nb]:
                    scores[nb] = score + d
                    parents[nb] = candidate
                    heappush(frontier, 
                             (score + d + heuristic(nb, t, grid), nb)) 
    
    # Reconstruct:
    path: list[tuple[int, int]] = [t]
    try:
        while (parent := parents[t]) is not None:
            path = [parent] + path
            t = parent
        return path
    except KeyError: # No path found!
        return []
