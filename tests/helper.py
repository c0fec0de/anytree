"""Helper Methods for testing."""

from contextlib import contextmanager


def eq_(one, other):
    assert one == other, f"{one} != {other}"


# hack own assert_raises, because py26 has a different implementation
@contextmanager
def assert_raises(exccls, msg):
    """Check exception of class `exccls` to be raised with message `msg`."""
    try:
        yield
        raise AssertionError(f"{exccls!r} not raised")
    except Exception as exc:
        assert isinstance(exc, exccls), f"{exc!r} is not a {exccls!r}"
        eq_(str(exc), msg)
