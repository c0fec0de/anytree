class TreeError(RuntimeError):

    """Tree Error."""

    pass


class LoopError(TreeError):

    """Tree contains infinite loop."""

    pass
