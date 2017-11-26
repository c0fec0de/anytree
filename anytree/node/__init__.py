"""
Node Classes.

* :any:`AnyNode`: a generic tree node with any number of attributes.
* :any:`Node`: a simple tree node with at least a name attribute and any number of additional attributes.
* :any:`NodeMixin`: extends any python class to a tree node.
"""

from .anynode import AnyNode   # noqa
from .exceptions import LoopError   # noqa
from .exceptions import TreeError   # noqa
from .node import Node   # noqa
from .nodemixin import NodeMixin   # noqa
