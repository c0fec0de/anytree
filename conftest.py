import pytest

# https://stackoverflow.com/questions/46962007/how-to-automatically-change-to-pytest-temporary-directory-for-all-doctests


@pytest.fixture(autouse=True)
def _docdir(request):
    # Trigger ONLY for the doctests.
    doctest_plugin = request.config.pluginmanager.getplugin("doctest")
    if isinstance(request.node, doctest_plugin.DoctestItem):
        # Get the fixture dynamically by its name.
        tmpdir = request.getfixturevalue("tmpdir")

        # Chdir only for the duration of the test.
        with tmpdir.as_cwd():
            yield

    else:
        # For normal tests, we have to yield, since this is a yield-fixture.
        yield
