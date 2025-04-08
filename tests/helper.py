"""Helper Methods for testing."""

from contextlib import contextmanager
from subprocess import run


def eq_(one, other):
    assert one == other, f"{one} != {other}"


# hack own assert_raises, because py26 has a different implementation
@contextmanager
def assert_raises(exccls, msg):
    """Check exception of class `exccls` to be raised with message `msg`."""
    try:
        yield
        assert False, "%r not raised" % exccls
    except Exception as exc:
        assert isinstance(exc, exccls), "%r is not a %r" % (exc, exccls)
        eq_(str(exc), msg)


def is_installed(cmd: tuple[str, ...]) -> bool:
    try:
        return run(cmd, check=False).returncode == 0
    except FileNotFoundError:
        return False


GRAPHVIZ_INSTALLED = is_installed(("dot", "--version"))
