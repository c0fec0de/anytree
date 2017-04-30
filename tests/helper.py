from contextlib import contextmanager
from nose.tools import eq_


# hack own assert_raises, because py26 has a different impelmentation
@contextmanager
def assert_raises(exccls, msg):
    try:
        yield
        assert False, "%r not raised" % exccls
    except Exception as exc:
        assert isinstance(exc, exccls), "%r is not a %r" % (exc, exccls)
        eq_(str(exc), msg)
