from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .nodemixin import NodeMixin


def _repr(node: NodeMixin[Any], args: list[str] | None = None, nameblacklist: Sequence[str] | None = None) -> str:
    classname = node.__class__.__name__
    args = args or []
    nameblacklist = nameblacklist or []
    for key, value in filter(
        lambda item: not item[0].startswith("_") and item[0] not in nameblacklist,
        sorted(node.__dict__.items(), key=lambda item: item[0]),
    ):
        args.append(f"{key}={value!r}")
    return "{}({})".format(classname, ", ".join(args))
