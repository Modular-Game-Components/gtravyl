Usage
=====

A Simple Example
----------------

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

.. note:: Values instead of indices.
   Another representation we may have is:

   .. code-block::

      3001111
      0001111
      0000000
      1101110
      1101114
   
   Where ``3`` and ``4`` are used to indicate the start and end vertices, respectively. To accomidate for this, we may replace
   
   .. code-block:: python

      import numpy as np
      import gtravyl as gt
      world = np.array([[0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 1, 1, 1, 0],
                        [1, 1, 0, 1, 1, 1, 0]])
      path = gt.shortest_path(world, (0, 0), (4, 6))

   with

   .. code-block:: python
      import numpy as np
      import gtravyl as gt
      world = np.array([[3, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 1, 1, 1, 0],
                        [1, 1, 0, 1, 1, 1, 4]])
      path = gt.shortest_path(world, sv=3, tv=4)

   ``sv`` and ``tv`` are short for "start value" and "end value, respectively.

--------------------
A Variant: Diagonals
--------------------

You might notice that we did not move diagonally, but you may want this for your application. By default, the neighborhood for a cell is the von Neumann neighborhood. This does *not* include diagonals. Fortunately, we can also supply the Moore neighborhood which *does* include diagonals. The following allows for diagonal movement:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 0, 1, 1, 1, 0],
                     [1, 1, 0, 1, 1, 1, 0]])
   path = gt.shortest_path(world, (0, 0), (4, 6),
                           neighbors=gt.moore_neighbors)
   for cell in path:
       world[cell] = 2

   print(world)

This gives the following output (notice the diagonal movement!):

.. code-block:: python

   [[2 2 0 1 1 1 1]
    [0 0 2 1 1 1 1]
    [0 0 0 2 2 2 0]
    [1 1 0 1 1 1 2]
    [1 1 0 1 1 1 2]]

This might not look like the shortest distance, but that is because, by default we assume every neighbor is ``1`` unit away from each other (even diagonals!).

------------------
Euclidean Distance
------------------

We fix the above by supplying the standard ``euclidean_dist`` function for the ``dist`` dictionary argument. This is what the new code looks like:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 1, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 0, 1, 1, 1, 0],
                     [1, 1, 0, 1, 1, 1, 0]])
   path = gt.shortest_path(world, (0, 0), (4, 6),
                           neighbors=gt.moore_neighbors,
                           dist=gt.euclidean_dist)
   for cell in path:
       world[cell] = 2

   print(world)

The output changes to accomidate the Euclidean distance:

.. code-block:: python

   [[2 0 0 1 1 1 1]
    [0 2 0 1 1 1 1]
    [0 0 2 2 2 2 0]
    [1 1 0 1 1 1 2]
    [1 1 0 1 1 1 2]]

-------------------------
``wrap``: Another Example
-------------------------

Consider the following world map:

.. code-block::

   0001000
   0001000
   0001000

And consider running the previous example with the new map. That is,

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0]])
   path = gt.shortest_path(world, (0, 0), (4, 6),
                           neighbors=gt.moore_neighbors,
                           dist=gt.euclidean_dist)
   for cell in path:
       world[cell] = 2

   print(world)

This gives a result of:

.. code-block:: python

  [[0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]] 

There are no ``2`` values because no path can be found. But what if we "wrap" the grid aroud a globe and allow (for instance) moving from ``(0, 0)`` to ``(0, 6)`` by moving left. We can do this by specifying the ``wrap`` keyword argument. Observe:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0]])
   path = gt.shortest_path(world, (0, 0), (4, 6),
                           neighbors=gt.moore_neighbors,
                           dist=gt.euclidean_dist,
                           wrap=gt.wrap)
   for cell in path:
       world[cell] = 2

   print(world)

This now gives:

.. code-block:: python

  [[2 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 0]
   [0 0 0 1 0 0 2]]
