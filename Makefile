NAME := wolproxypycli
INSTALL_STAMP := .install.stamp
UPDATE_STAMP := .update.stamp
PRODUCTION_STAMP := .production.stamp
EXPORT_STAMP := .export.stamp
BUILD_STAMP := .build.stamp
DOCS_STAMP := .docs.stamp
PRECOMMIT_CONF := .pre-commit-config.yaml
SRC := $(NAME) config/
TESTS := tests/
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

all: tests build export docs

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install     install the package dependencies and prepare the development environment"
	@echo "  update      force-udpate packages dependencies"
	@echo "  production  install the root package for production"
	@echo "  build       build dist wheel and tarball files"
	@echo "  export      export all requirements to requirements.txt"
	@echo "  docs        build documentation via MkDocs"
	@echo "  clean       remove all temporary files"
	@echo "  lint        run the code linters"
	@echo "  format      reformat code"
	@echo "  precommit   run the pre-commit checks on all files"
	@echo "  tests       run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install
	$(POETRY) lock --no-update
	$(POETRY) run pre-commit install
	touch $(INSTALL_STAMP)

update: $(UPDATE_STAMP)
$(UPDATE_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) update
	$(POETRY) lock --no-update
	$(POETRY) run pre-commit install
	$(POETRY) run pre-commit autoupdate
	touch $(UPDATE_STAMP)

production: $(PRODUCTION_STAMP)
$(PRODUCTION_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install --only main --no-interaction
	touch $(PRODUCTION_STAMP)

build: $(BUILD_STAMP)
$(BUILD_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	rm -rf dist/
	$(POETRY) build
	touch $(BUILD_STAMP)

export: $(EXPORT_STAMP) update
$(EXPORT_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes
	$(POETRY) export -f requirements.txt --output requirements-dev.txt --with dev --without-hashes
	$(POETRY) export -f requirements.txt --output requirements-docs.txt --with docs --without-hashes
	touch $(EXPORT_STAMP)

docs: $(DOCS_STAMP) export
$(DOCS_STAMP): requirements-docs.txt mkdocs.yml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run mkdocs build
	touch $(DOCS_STAMP)

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) $(PRODUCTION_STAMP) $(EXPORT_STAMP) $(BUILD_STAMP) .coverage .mypy_cache

.PHONY: lint
lint: format
	$(POETRY) run flake8 --max-line-length 120 --ignore=E203,E266,E501,W503,F403,F401,E402,B008,FS001,FS003 $(TESTS) $(SRC)
	$(POETRY) run mypy $(TESTS) $(SRC)
	$(POETRY) run pydocstyle $(TESTS) $(SRC)
	$(POETRY) run bandit -c pyproject.toml -r $(SRC)

.PHONY: format
format:
	$(POETRY) run isort $(TESTS) $(SRC)
	$(POETRY) run black $(TESTS) $(SRC)

.PHONY: precommit
precommit: $(INSTALL_STAMP) $(PRECOMMIT_CONF) lint
	$(POETRY) run pre-commit run --all-files

.PHONY: tests
tests: $(INSTALL_STAMP)
	$(POETRY) run pytest $(TESTS)
