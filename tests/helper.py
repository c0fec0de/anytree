"""Helper Methods for testing."""
from contextlib import contextmanager

import six


def eq_(one, other):
    assert one == other


# hack own assert_raises, because py26 has a different impelmentation
@contextmanager
def assert_raises(exccls, msg):
    """Check exception of class `exccls` to be raised with message `msg`."""
    try:
        yield
        assert False, "%r not raised" % exccls
    except Exception as exc:
        assert isinstance(exc, exccls), "%r is not a %r" % (exc, exccls)
        eq_(str(exc), msg)


def eq_str(value, expected):
    """Python 2.x and 3.x compatible string compare."""
    if six.PY2:
        eq_(value.decode("utf-8"), expected)
    else:
        eq_(value, expected)


def with_setup(setup=None, teardown=None):
    def decorate(func, setup=setup, teardown=teardown):
        if setup:
            if hasattr(func, "setup"):
                _old_s = func.setup

                def _s():
                    setup()
                    _old_s()

                func.setup = _s
            else:
                func.setup = setup
        if teardown:
            if hasattr(func, "teardown"):
                _old_t = func.teardown

                def _t():
                    _old_t()
                    teardown()

                func.teardown = _t
            else:
                func.teardown = teardown
        return func

    return decorate
