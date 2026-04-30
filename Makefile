# workingclass — local task runner
# Mirrors what CI runs in .github/workflows/ci.yml.
# Use `make help` to list targets.

PY ?= python
PYTEST ?= pytest

.PHONY: help install test test-unit test-e2e validate validate-strict index check-translations all clean

help: ## Show this message
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dev dependencies via pip (use `uv sync` if you prefer uv)
	$(PY) -m pip install -e ".[dev]"

test: test-unit test-e2e ## Run all tests (unit + e2e)

test-unit: ## Unit + structural tests (fast)
	$(PYTEST) -m "not e2e"

test-e2e: ## End-to-end tests (subprocess, stub LLM)
	$(PYTEST) -m e2e

validate: ## Validate skill / commands / cases (errors only)
	$(PY) evals/validate_structure.py

validate-strict: ## Validate with --strict (errors + warnings fail)
	$(PY) evals/validate_structure.py --strict

index: ## Rebuild evals/cases/INDEX.md
	$(PY) evals/build_index.py

check-translations: ## Flag README translations that lag behind README.md
	$(PY) tools/check_translation_staleness.py

all: validate-strict test index ## Everything CI runs
	@echo "✓ all green"

clean: ## Remove caches
	rm -rf .pytest_cache __pycache__ */__pycache__ */*/__pycache__ .coverage htmlcov
