from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator

    from typing_extensions import Self

    from anytree.node.lightnodemixin import LightNodeMixin
    from anytree.node.nodemixin import NodeMixin


NodeT_co = TypeVar("NodeT_co", bound="NodeMixin[Any] | LightNodeMixin[Any]", covariant=True)


class AbstractIter(Generic[NodeT_co]):
    # pylint: disable=R0205
    """
    Iterate over tree starting at `node`.

    Base class for all iterators.

    Keyword Args:
        filter_: function called with every `node` as argument, `node` is returned if `True`.
        stop: stop iteration at `node` if `stop` function returns `True` for `node`.
        maxlevel (int): maximum descending in the node hierarchy.
    """

    def __init__(
        self,
        node: NodeT_co,
        filter_: Callable[[NodeT_co], bool] | None = None,
        stop: Callable[[NodeT_co], bool] | None = None,
        maxlevel: int | None = None,
    ) -> None:
        self.node = node
        self.filter_ = filter_
        self.stop = stop
        self.maxlevel = maxlevel
        self.__iter: Iterator[NodeT_co] | None = None

    def __init(self) -> Iterator[NodeT_co]:
        node = self.node
        maxlevel = self.maxlevel
        filter_ = self.filter_ or AbstractIter.__default_filter
        stop = self.stop or AbstractIter.__default_stop
        children = [] if AbstractIter._abort_at_level(1, maxlevel) else AbstractIter._get_children([node], stop)
        return self._iter(children, filter_, stop, maxlevel)

    @staticmethod
    def __default_filter(node: NodeT_co) -> bool:
        # pylint: disable=W0613
        return True

    @staticmethod
    def __default_stop(node: NodeT_co) -> bool:
        # pylint: disable=W0613
        return False

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> NodeT_co:
        if self.__iter is None:
            self.__iter = self.__init()
        return next(self.__iter)

    @staticmethod
    def _iter(
        children: Iterable[NodeT_co],
        filter_: Callable[[NodeT_co], bool],
        stop: Callable[[NodeT_co], bool],
        maxlevel: int | None,
    ) -> Iterator[NodeT_co]:
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def _abort_at_level(level: int, maxlevel: int | None) -> bool:
        return maxlevel is not None and level > maxlevel

    @staticmethod
    def _get_children(children: Iterable[NodeT_co], stop: Callable[[NodeT_co], bool]) -> list[Any]:
        return [child for child in children if not stop(child)]
