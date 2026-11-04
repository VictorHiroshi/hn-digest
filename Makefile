UV ?= uv
DEV ?= 0

export PATH := $(HOME)/.local/bin:$(PATH)

.PHONY: setup install-uv test lint lint-ruff lint-pyrefly

setup: install-uv
ifeq ($(DEV),1)
	$(UV) sync --group dev
else
	$(UV) sync --no-dev
endif

install-uv:
	@if command -v "$(UV)" >/dev/null 2>&1; then \
		echo "uv is already installed"; \
	else \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

test:
	$(UV) run --group dev pytest

lint: lint-ruff lint-pyrefly

lint-ruff:
	uvx ruff check .

lint-pyrefly:
	uvx pyrefly check
