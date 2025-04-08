# CONTRIBUTING

Please follow github workflow. Create a ticket and/or branch. Create a pull-request.

## Local Development

### Installation

Please install these tools:

* [`uv` Installation](https://docs.astral.sh/uv/getting-started/installation/)
* [`make`](https://www.gnu.org/software/make/)
* [`git`](https://git-scm.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [`graphviz`](https://graphviz.org/)


### Editor
Start Visual Studio Code:

```bash
make code
```

### Testing

Run auto-formatting, linting, tests and documentation build:

```bash
make all
```

See `make help` for any further details.

Please note that `tests/refdata` contains reference data from test runs.
`make test2refdata` updates this directory.

## Project Structure

The project contains these files and directories:

| File/Directory | Description |
|---|---|
| `src/` | Python Package Sources - the files this is all about |
| `pyproject.toml` | Python Package Meta File. Also contains all tool settings |
| `.gitignore` | Lists of files and directories ignored by version control system |
| `.github/` | Github Settings |
| `.readthedocs.yaml` | Documentation Server Configuration |
| `.pre-commit-config.yaml` | Pre-Commit Check Configuration |
| `uv.lock` | File with resolved python package dependencies |

Next to that, there are some temporary files ignored by version control system.

| File/Directory | Description |
|---|---|
| `htmlcov/` | Test Execution Code Coverage Report in HTML format |
| `report.xml` | Test Execution Report |
| `.venv` | Virtual Environments |


## Branches

* `2.x.x` main line for `2.x.x`
* `3.x.x` main line for `3.x.x`
    * documentation links refer to `3.x.x`
    * 2.x.x can be merged to 3.x.x
* `main`
    * 2.x.x can be merged to main


### Release

```bash
# Update 3.x.x
git checkout 3.x.x
git pull origin 2.x.x
git push origin 3.x.x

prev_version=$(poetry version -s)

# Version Bump
poetry version minor
# OR
poetry version patch

# Commit, Tag and Push
version=$(poetry version -s)

sed "s/$prev_version/$version/g" -i anytree/__init__.py

git commit -m"version bump to ${version}" pyproject.toml anytree/__init__.py
git tag "${version}" -m "Release ${version}"
git push
git push --tags

# Update main
git checkout main
git pull origin 2.x.x
git push origin main

# Publishing is handled by CI
```
