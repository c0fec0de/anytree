"""
Node Classes.

* :any:`AnyNode`: a generic tree node with any number of attributes.
* :any:`Node`: a simple tree node with at least a name attribute and any number of additional attributes.
* :any:`NodeMixin`: extends any python class to a tree node.
* :any:`SymlinkNode`: Tree node which references to another tree node.
* :any:`SymlinkNodeMixin`: extends any Python class to a symbolic link to a tree node.
* :any:`LightNodeMixin`: A :any:`NodeMixin` using slots.
"""

from .anynode import AnyNode as AnyNode  # noqa: PLC0414
from .exceptions import LoopError as LoopError  # noqa: PLC0414
from .exceptions import TreeError as TreeError  # noqa: PLC0414
from .lightnodemixin import LightNodeMixin as LightNodeMixin  # noqa: PLC0414
from .node import Node as Node  # noqa: PLC0414
from .nodemixin import NodeMixin as NodeMixin  # noqa: PLC0414
from .symlinknode import SymlinkNode as SymlinkNode  # noqa: PLC0414
from .symlinknodemixin import SymlinkNodeMixin as SymlinkNodeMixin  # noqa: PLC0414

__all__ = [
    "AnyNode",
    "LightNodeMixin",
    "LoopError",
    "Node",
    "NodeMixin",
    "SymlinkNode",
    "SymlinkNodeMixin",
    "TreeError",
]
