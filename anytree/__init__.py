# -*- coding: utf-8 -*-

"""Powerful and Lightweight Python Tree Data Structure."""

__version__ = "2.4.3"
__author__ = "c0fec0de"
__author_email__ = "c0fec0de@gmail.com"
__description__ = """Powerful and Lightweight Python Tree Data Structure.."""
__url__ = "https://github.com/c0fec0de/anytree"

from .search import CountError  # noqa
from .search import find  # noqa
from .search import find_by_attr  # noqa
from .search import findall  # noqa
from .search import findall_by_attr  # noqa
from .iterators import LevelOrderGroupIter  # noqa
from .iterators import LevelOrderIter  # noqa
from .iterators import PostOrderIter  # noqa
from .iterators import PreOrderIter  # noqa
from .iterators import ZigZagGroupIter  # noqa
from .node import AnyNode  # noqa
from .node import LoopError  # noqa
from .node import Node  # noqa
from .node import NodeMixin  # noqa
from .node import TreeError  # noqa
from .render import AbstractStyle  # noqa
from .render import AsciiStyle  # noqa
from .render import ContRoundStyle  # noqa
from .render import ContStyle  # noqa
from .render import DoubleStyle  # noqa
from .render import RenderTree  # noqa
from .resolver import ChildResolverError  # noqa
from .resolver import Resolver  # noqa
from .resolver import ResolverError  # noqa
from .walker import WalkError  # noqa
from .walker import Walker  # noqa

# legacy
LevelGroupOrderIter = LevelOrderGroupIter
