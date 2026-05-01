# workingclass — local task runner
# Mirrors what CI runs in .github/workflows/ci.yml.
# Use `make help` to list targets.

PY ?= python
PYTEST ?= pytest

.PHONY: help install test test-unit test-e2e validate validate-strict index check-translations eval-record eval-record-api eval-diff eval-baseline all clean

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

eval-record: ## CLI mode (subprocess; inherits Claude Code memory). Use eval-record-api for memory-isolated.
	@if [ -z "$(LLM)" ]; then LLM=claude; fi; \
	DATE=$$(date -u +%Y-%m-%d); \
	TAG=$${TAG:-$$LLM}; \
	OUT=evals/runs/RESULTS-$$DATE-$$TAG.json; \
	echo "Recording to $$OUT (LLM=$$LLM)."; \
	echo "⚠ This runs the LLM as a subprocess; it inherits CLAUDE.md memory."; \
	echo "  For a memory-isolated run, use 'make eval-record-api' instead."; \
	sleep 2; \
	$(PY) evals/run_evals.py --auto --llm-command "$$LLM" --record "$$OUT"

eval-record-api: ## Memory-isolated run via Anthropic SDK. Requires $$ANTHROPIC_API_KEY. Set MODEL=... to override.
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then echo "ANTHROPIC_API_KEY is not set."; exit 2; fi; \
	DATE=$$(date -u +%Y-%m-%d); \
	MODEL=$${MODEL:-claude-opus-4-7}; \
	TAG=$${TAG:-$$MODEL-api}; \
	OUT=evals/runs/RESULTS-$$DATE-$$TAG.json; \
	echo "Recording to $$OUT via Anthropic SDK (model=$$MODEL)."; \
	echo "✓ Memory-isolated — does NOT load CLAUDE.md."; \
	sleep 2; \
	$(PY) evals/run_evals.py --api --model "$$MODEL" --record "$$OUT"

eval-baseline: ## Regenerate evals/runs/BASELINE-stub.json from the stub LLM (no API needed)
	$(PY) evals/run_evals.py --auto --llm-command tests/fixtures/stub_llm_pass.sh --record evals/runs/BASELINE-stub.json

eval-diff: ## Diff two recordings: make eval-diff BASELINE=path/to/a.json CURRENT=path/to/b.json
	@if [ -z "$(BASELINE)" ] || [ -z "$(CURRENT)" ]; then \
		echo "usage: make eval-diff BASELINE=<path> CURRENT=<path> [SHOW=1]"; exit 2; \
	fi; \
	if [ "$(SHOW)" = "1" ]; then \
		$(PY) evals/eval_diff.py "$(BASELINE)" "$(CURRENT)" --show-output; \
	else \
		$(PY) evals/eval_diff.py "$(BASELINE)" "$(CURRENT)"; \
	fi

all: validate-strict test index ## Everything CI runs
	@echo "✓ all green"

clean: ## Remove caches
	rm -rf .pytest_cache __pycache__ */__pycache__ */*/__pycache__ .coverage htmlcov
