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

.. note:: You can use values instead of indices.
   For instance, another representation we may have is:

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

   ``sv`` and ``tv`` are short for "start value" and "destination value", respectively.

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

------------------
Euclidean Distance
------------------

We remark, that although we have computed the shortest path, we assumed the "unit metric". That is each distance (including diagonals!) is ``1``. It would make much more sense if the diagonals had a value of ``sqrt(2)``. To do so, we can supply the ``euclidean_dist`` function for the ``dist`` keyword argument. This is what the new code looks like:

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

In this case, we got lucky and the path remains the same as above:

.. code-block:: python

   [[2 2 0 1 1 1 1]
    [0 0 2 1 1 1 1]
    [0 0 0 2 2 2 0]
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


A Slightly More Complicated Example
-----------------------------------

Realistically, the world is not represented as *just* ``1`` and ``0``. We may also have other values. For instance we may have something like:

.. code-block::

   000222
   000222
   000123
   444333
   444113
   444113

Where each number corresponds, to say, the height. A couple issues arise:

* ``4`` may represent a mountain, and we may not want units to be able to travelto mountains.
* Traveling from one height to another might incur a penalty in terms of length. For instance, it might be slower to travel from a cell with value (height) ``0`` to a cell with value (height) ``2`` than it is to travel from a cell with value (height) ``2`` to a cell with value (height) ``2``.

We adress these two issues in the proceeding sections.

------------------
Avoiding Mountains
------------------

We can do this by changed the ``allowed`` keyword argument. ``allowed`` is a function that takes a value and returns a boolean as to whether it is permissible to travel to that square. Thus, we may do:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 2, 2, 2],
                     [0, 0, 0, 2, 2, 2],
                     [0, 0, 0, 1, 2, 3],
                     [4, 4, 4, 3, 3, 3]
                     [4, 4, 4, 1, 1, 1],
                     [4, 4, 4, 1, 1, 1]])
   path = gt.shortest_path(world, (0, 0), (5, 5),
                           neighbors=gt.moore_neighbors,
                           allowed=lambda x: x < 4)
   for cell in path:
       world[cell] = 9

   print(world)

This gives:

.. code-block:: python

   [[9 0 0 2 2 2]
    [0 9 0 2 2 2]
    [0 0 9 2 2 2]
    [4 4 4 9 3 3]
    [4 4 4 1 9 1]
    [4 4 4 1 1 9]]

------------------------------------
Elevation: A Closer Look at Distance
------------------------------------

To account for elevation we can make a custom distance function. A distance function takes in ``4`` arguments instead of the expected ``2``. Why? To account for *both* indices *and* values. The ``euclidean_dist`` esentially uses only the index values to compute the distance. It is implemented as follows:

.. code-block:: python

   def euclidean_dist(ind1: tuple[int, int], ind2: tuple[int, int],
                 value1: Any, value2: Any):
       return sqrt((ind1[0] - ind2[0]) ** 2 + (ind1[1] - ind2[1]) ** 2)

For dealing with elevation, we can essentially use the values as the ``z`` coordinate and make:

.. code-block:: python

   def ext_euclid(ind1: tuple[int, int], ind2: tuple[int, int],
                  value1: Any, value2: Any):
       return sqrt((ind1[0] - ind2[0]) ** 2 + \
                   (ind1[1] - ind2[1]) ** 2 + \
                   (value1 - value2) ** 2)

Now we may simply supply ``ext_euclid`` as the ``dist`` keyword argument:

.. code-block:: python

   import numpy as np
   import gtravyl as gt
   world = np.array([[0, 0, 0, 2, 2, 2],
                     [0, 0, 0, 2, 2, 2],
                     [0, 0, 2, 2, 2, 2],
                     [4, 4, 4, 3, 3, 3]
                     [4, 4, 4, 1, 1, 1],
                     [4, 4, 4, 1, 1, 1]])
   path = gt.shortest_path(world, (0, 0), (5, 5),
                           neighbors=gt.moore_neighbors,
                           allowed=lambda x: x < 4,
                           dist=ext_euclid)
   for cell in path:
       world[cell] = 9

   print(world)

This gives:

.. code-block:: python

   [[9 9 0 2 2 2]
    [0 0 9 2 2 2]
    [0 0 0 9 2 3]
    [4 4 4 3 9 3]
    [4 4 4 1 1 9]
    [4 4 4 1 1 9]]
