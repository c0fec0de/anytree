# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "anytree"
copyright = "2016-2023, c0fec0de"
author = "c0fec0de"
description = "Python Tree Data"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = ".rst"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxdoc"
html_static_path = ["static"]

intersphinx_mapping = {
    "python": ("http://docs.python.org/3", None),
}
intersphinx_cache_limit = 1

autodoc_default_options = {
    "members": None,  # Include all members (methods).
    "member-order": "bysource",
}
autoclass_content = "both"
