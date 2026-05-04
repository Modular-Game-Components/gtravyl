from collections import defaultdict
from heapq import heappush, heappop
from typing import Any

import numpy as np


def in_bounds(pt: tuple[int, int], dim: tuple[int, int]) -> bool:
    """Checks if the candidate point actually exists in the grid.

    :param pt: The point to check if it is in bounds.
    :param dim: Dimensions (row, column) of the grid.
    """
    return 0 <= pt[0] < dim[0] and 0 <= pt[1] < dim[1]

def vn_neighbors(ind: tuple[int, int], 
                 grid: np.array):
    """Return the von Neumann neighborhood of a particular cell in the grid.

    :param ind: Index to compute von Neumann neighborhood of.
    :param grid: The grid ``ind`` belongs to.
    """
    left = (ind[0] - 1, ind[1])
    right = (ind[0] + 1, ind[1])
    up = (ind[0], ind[1] - 1)
    down = (ind[0], ind[1] + 1)
    nbs = [left, right, up, down]
    nbs = filter(lambda x: in_bounds(x, grid.shape) and grid[x] != 1, nbs)
    return nbs

def unit_dist(ind1: tuple[int, int], ind2: tuple[int, int],
              value1: Any, value2: Any):
    return 1

def euclidean_dist(ind1: tuple[int, int], ind2: tuple[int, int],
              value1: Any, value2: Any):
    return (ind1[0] - ind2[0]) ** 2 + (ind1[1] - ind2[1]) ** 2

def moore_neighbors(ind: tuple[int, int],
                    grid: np.array, wrap=False):
    """Return the Moore neighborhood of a particular cell in the grid.

    :param ind: Index to compute Moore neighborhood of.
    :param grid: The grid ``ind`` belongs to.
    """
    left_tcorner = (ind[0] - 1, ind[1] + 1)
    left = (ind[0] - 1, ind[1])
    left_bcorner = (ind[0] - 1, ind[1] - 1)
    right_tcorner = (ind[0] + 1, ind[1] + 1)
    right = (ind[0] + 1, ind[1])
    right_bcorner = (ind[0] + 1, ind[1] - 1)
    up = (ind[0], ind[1] - 1)
    down = (ind[0], ind[1] + 1)
    nbs = [left_tcorner, left, left_bcorner,
           right_tcorner, right, right_bcorner,
           up, down]
    nbs = filter(lambda x: in_bounds(x, grid.shape) and grid[x] != 1, nbs)
    return nbs

def shortest_path(grid: np.array,
                  si: tuple[int, int] | None = None, 
                  ti: tuple[int, int] | None = None,
                  sv: Any | None = None,
                  tv: Any | None = None,
                  neighbors=vn_neighbors,
                  dist=unit_dist) -> list[tuple[int, int]]:
    """Find shortest path from ``s`` to ``t`` in a given `grid`.

    :param grid: numpy array representation of the world to traverse.
    :param s: The "source" index, i.e. where the path search starts.
    :param t: The "desitination" index, i.e. where the path should end.
    :param neighbors: Computes the neighborhood of any choice of index in the
       grid.
    """
    i1 = None
    i2 = None
    if sv is not None:
        i1 = np.where(grid == sv)[0][0]
    if tv is not None:
        i2 = np.where(grid == tv)[0][0]
    s, t = i1 or si, i2 or ti
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
    heappush(frontier, (0, s))
    parents[s] = None
    while frontier:
        (score, candidate) = heappop(frontier)
        if candidate == t:
            break
        seen.add(candidate)
        for nb in neighbors(candidate, grid):
            if nb not in seen:
                d = dist(candidate, nb, grid[candidate], grid[nb])
                if score + d < scores[nb]:
                    scores[nb] = score + d
                    parents[nb] = candidate
                    heappush(frontier, (score + 1, nb)) 
    else:
        return []
    
    # Reconstruct:
    path = [candidate]
    while (parent := parents[candidate]) is not None:
        path = [parent] + path
        candidate = parent
    return path
