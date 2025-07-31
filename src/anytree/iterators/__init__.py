"""
Tree Iteration.

* :any:`PreOrderIter`: iterate over tree using pre-order strategy (self, children)
* :any:`PostOrderIter`: iterate over tree using post-order strategy (children, self)
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelOrderGroupIter`: iterate over tree using level-order strategy returning group for every level
* :any:`ZigZagGroupIter`: iterate over tree using level-order strategy returning group for every level
"""

from .abstractiter import AbstractIter as AbstractIter  # noqa: PLC0414
from .levelordergroupiter import LevelOrderGroupIter as LevelOrderGroupIter  # noqa: PLC0414
from .levelorderiter import LevelOrderIter as LevelOrderIter  # noqa: PLC0414
from .postorderiter import PostOrderIter as PostOrderIter  # noqa: PLC0414
from .preorderiter import PreOrderIter as PreOrderIter  # noqa: PLC0414
from .zigzaggroupiter import ZigZagGroupIter as ZigZagGroupIter  # noqa: PLC0414

__all__ = [
    "AbstractIter",
    "LevelOrderGroupIter",
    "LevelOrderIter",
    "PostOrderIter",
    "PreOrderIter",
    "ZigZagGroupIter",
]
