import six


class AbstractIter(six.Iterator):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Base class for all iterators.

        Iterate over tree starting at `node`.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.
        """
        self.node = node
        self.filter_ = filter_
        self.stop = stop
        self.maxlevel = maxlevel
        self.__iter = None

    def __init(self):
        node = self.node
        maxlevel = self.maxlevel
        if self.filter_ is None:
            def filter_(node):
                return True
        else:
            filter_ = self.filter_
        if self.stop is None:
            def stop(node):
                return False
        else:
            stop = self.stop
        children = [] if AbstractIter._abort_at_level(1, maxlevel) else AbstractIter._get_children([node], stop)
        return self._iter(children, filter_, stop, maxlevel)

    def __iter__(self):
        return self.__init()

    def __next__(self):
        if self.__iter is None:
            self.__iter = self.__init()
        return next(self.__iter)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def _abort_at_level(level, maxlevel):
        return maxlevel is not None and level > maxlevel

    @staticmethod
    def _get_children(children, stop):
        return [child for child in children if not stop(child)]
