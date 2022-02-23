# -*- coding: utf-8 -*-
"""
Tree Iteration.

* :any:`AscendingIter`: iterate upwards toward the root of the tree
* :any:`PreOrderIter`: iterate over tree using pre-order strategy (self, children)
* :any:`PostOrderIter`: iterate over tree using post-order strategy (children, self)
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelOrderGroupIter`: iterate over tree using level-order strategy returning group for every level
* :any:`ZigZagGroupIter`: iterate over tree using level-order strategy returning group for every level
"""

from .abstractiter import AbstractIter  # noqa
from .ascendingiter import AscendingIter  # noqa
from .levelordergroupiter import LevelOrderGroupIter  # noqa
from .levelorderiter import LevelOrderIter  # noqa
from .postorderiter import PostOrderIter  # noqa
from .preorderiter import PreOrderIter  # noqa
from .zigzaggroupiter import ZigZagGroupIter  # noqa
