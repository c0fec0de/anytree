_GREEN:=\033[0;32m
_BLUE:=\033[0;34m
_BOLD:=\033[1m
_NORM:=\033[0m
ENV:=uv run --frozen --
PYTEST_OPTIONS=


.PHONY: help
help:  ## [DEFAULT] Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf "${_BLUE}${_BOLD}%-10s${_NORM} %s\n", $$1, $$2}'


.PHONY: all
all:  ## Do everything taggged with [ALL] below
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep "\[ALL\]" | grep -v "^all" | awk 'BEGIN {FS = ":.*?##"}; {printf "%s ", $$1}' | xargs make
	@echo "\n    ${_GREEN}${_BOLD}PASS${_NORM}\n"


.PHONY: pre-commit
pre-commit: .venv/.valid .git/hooks/pre-commit ## [ALL] Run 'pre-commit' on all files
	${ENV} pre-commit run --all-files

.git/hooks/pre-commit: .venv/.valid
	${ENV} pre-commit install --install-hooks


.PHONY: test
test: .venv/.valid ## [ALL] Run Unittests via 'pytest' with {PYTEST_OPTIONS}
	${ENV} pytest -vv ${PYTEST_OPTIONS}
	@echo  "See coverage report:\n\n    file://${PWD}/htmlcov/index.html\n"


.PHONY: checktypes
checktypes: .venv/.valid ## [ALL] Run Type-Checking via 'mypy'
	${ENV} mypy .


.PHONY: doc
doc: .venv/.valid ## [ALL] Build Documentation via 'mkdocs'
	${ENV} mkdocs build --strict


.PHONY: doc-serve
doc-serve: .venv/.valid ## Start Local Documentation Server via 'mkdocs'
	${ENV} mkdocs serve --no-strict


.PHONY: code
code:  ## Start Visual Studio Code
	code anytree.code-workspace &


.PHONY: clean
clean:  ## Remove everything mentioned by '.gitignore' file
	git clean -Xdf


.PHONY: distclean
distclean:  ## Remove everything mentioned by '.gitignore' file and UNTRACKED files
	git clean -xdf


.PHONY: shell
shell:  ## Open a project specific SHELL. For leaving use 'exit'.
	${ENV} ${SHELL}


# Helper
.venv/.valid: pyproject.toml uv.lock
	uv sync --frozen
	@touch $@

uv.lock:
	uv lock
