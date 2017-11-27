"""
Powerful and Lightweight Python Tree Data Structure with various plugins.
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path


def _read_metainfo(filepath):
    import re
    pat = re.compile(r"__(?P<name>[a-z_]+)__ = (?P<expr>.*)")
    metainfo = {}
    with open(filepath) as fh:
        for line in fh:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            match = pat.match(line)
            if match:
                metainfo[match.group("name")] = eval(match.group("expr"))
    return metainfo


config = _read_metainfo("anytree/__init__.py")
config['name'] = 'anytree'
config['license'] = 'Apache 2.0'
config['classifiers'] = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]
config['keywords'] = 'tree, tree data, treelib, tree walk, tree structure'
config['packages'] = ['anytree', 'anytree.node', 'anytree.iterators', 'anytree.importer', 'anytree.exporter']
config['install_requires'] = ['six>=1.9.0']
config['extras_require'] = {
    'dev': ['check-manifest'],
    'test': ['coverage'],
}
config['tests_require'] = ['nose']
config['test_suite'] = 'nose.collector'

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    config['long_description'] = f.read()

# python 2.6 does not implement OrderedDict, so we have to install it
try:
    from collections import OrderedDict  # noqa
except ImportError:
    config['install_requires'].append("ordereddict")

setup(**config)
