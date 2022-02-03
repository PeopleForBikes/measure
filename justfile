src_dir := "measure"


# Setup the environment.
setup:
    conda env create --file environment-{{os()}}-{{arch()}}.yaml \
      || conda env update --file environment-{{os()}}-{{arch()}}.yaml \
      || conda env create --file environment.yaml \
      || conda env update --file environment.yaml

# Meta task running ALL the CI tasks at onces.
ci: lint test

# Meta task running all the linters at once.
lint: lint-md lint-python

# Lint markown files.
lint-md:
    npx --yes markdownlint-cli2 "**/*.md"

# Lint python files.
lint-python:
    isort . --check
    black --check {{src_dir}}
    flake8 {{src_dir}}
    pylint {{src_dir}}
    pydocstyle {{src_dir}}

# Meta tasks running all formatters at once.
fmt: fmt-md fmt-python

# Format markdown files.
fmt-md:
    npx --yes prettier --write --prose-wrap always **/*.md

# Format python files.
fmt-python:
    isort .
    black {{src_dir}}

# Save environment
conda-export:
    conda env export --from-history > environment.yaml
    conda env export > environment-{{os()}}-{{arch()}}.yaml

# Run the unit tests.
test:
  pytest -x --cov-report term-missing --cov-report html --cov={{src_dir}}
