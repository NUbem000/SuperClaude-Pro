.PHONY: help install install-dev test test-cov lint format type-check security clean build docs serve-docs release

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python3
PIP := $(PYTHON) -m pip

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)SuperClaude Pro Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install SuperClaude Pro in production mode
	$(PIP) install --upgrade pip
	$(PIP) install .
	@echo "$(GREEN)✓ SuperClaude Pro installed successfully$(NC)"

install-dev: ## Install SuperClaude Pro in development mode with all dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev,docs,telemetry]"
	pre-commit install
	@echo "$(GREEN)✓ Development environment ready$(NC)"

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest -v

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=superclaude_pro --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

lint: ## Run linting checks
	@echo "$(BLUE)Running linting checks...$(NC)"
	ruff check .
	@echo "$(GREEN)✓ Linting passed$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format .
	ruff check --fix .
	@echo "$(GREEN)✓ Code formatted$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy src/superclaude_pro
	@echo "$(GREEN)✓ Type checking passed$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r src/
	pip-audit
	@echo "$(GREEN)✓ Security checks passed$(NC)"

clean: ## Clean build artifacts and cache files
	@echo "$(BLUE)Cleaning up...$(NC)"
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)✓ Build complete$(NC)"

docs: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	cd docs && mkdocs build
	@echo "$(GREEN)✓ Documentation built$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(BLUE)Serving documentation at http://localhost:8000$(NC)"
	cd docs && mkdocs serve

release: ## Create a new release (use: make release VERSION=x.y.z)
	@if [ -z "$(VERSION)" ]; then \
		echo "$(RED)ERROR: VERSION is required. Usage: make release VERSION=x.y.z$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Creating release $(VERSION)...$(NC)"
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)
	@echo "$(GREEN)✓ Release v$(VERSION) created$(NC)"

# Development workflow shortcuts
check: lint type-check test ## Run all checks (lint, type-check, test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

ci: check security ## Run CI checks locally
	@echo "$(GREEN)✓ CI checks passed!$(NC)"

dev: format check ## Format and run checks
	@echo "$(GREEN)✓ Ready for commit!$(NC)"