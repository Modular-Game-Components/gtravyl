Basic Usage
===========

Suppose you are trying to create a real time strategy game. You may have a grid-like map internally represented as a numpy array. It might look something like:

.. code-block::

   0001111
   0001111
   0000000
   1101110
   1101110

where the ``1`` indicates you cannot travel into that cell. Now you want to move a character that is in the cell with index ``(0, 0)`` to the bottom right corner. Ideally, you would like to know the shortest path too. This can be done easily with ``gtravyl``, observe:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 0, 1, 1, 1, 0],
                     [1, 1, 0, 1, 1, 1, 0]])
   path = gt.shortest_path(world, (0, 0), (4, 6))
   for cell in path:
       world[cell] = 2

   print(world)

This gives a path (represented by the cells with ``2``) that looks like one should expect:

.. code-block:: python

   [[2 2 2 1 1 1 1]
    [0 0 2 1 1 1 1]
    [0 0 2 2 2 2 2]
    [1 1 0 1 1 1 2]
    [1 1 0 1 1 1 2]]
