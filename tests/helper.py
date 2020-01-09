"""Helper Methods for testing."""
from contextlib import contextmanager

import six
from nose.tools import eq_


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
        eq_(value.decode('utf-8'), expected)
    else:
        eq_(value, expected)
