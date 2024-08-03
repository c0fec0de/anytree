# -*- coding: utf-8 -*-
"""
Tree Iteration.

* :any:`PreOrderIter`: iterate over tree using pre-order strategy (self, children)
* :any:`PostOrderIter`: iterate over tree using post-order strategy (children, self)
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelOrderGroupIter`: iterate over tree using level-order strategy returning group for every level
* :any:`ZigZagGroupIter`: iterate over tree using level-order strategy returning group for every level
"""

# pylint: disable=useless-import-alias
from .abstractiter import AbstractIter as AbstractIter  # noqa
from .levelordergroupiter import LevelOrderGroupIter as LevelOrderGroupIter  # noqa
from .levelorderiter import LevelOrderIter as LevelOrderIter  # noqa
from .postorderiter import PostOrderIter as PostOrderIter  # noqa
from .preorderiter import PreOrderIter as PreOrderIter  # noqa
from .zigzaggroupiter import ZigZagGroupIter as ZigZagGroupIter  # noqa
