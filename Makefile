# Use .venv Python if available, otherwise system python
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python)
UV := $(if $(wildcard .venv/bin/uv),.venv/bin/uv,uv)

.PHONY: help install install-dev test test-cov lint format security clean run docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	$(UV) pip install --python .venv/bin/python -e .

install-dev: ## Install development dependencies
	$(UV) pip install --python .venv/bin/python -e ".[dev]"
	$(PYTHON) -m pre_commit install

test: ## Run tests
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Run tests with coverage
	$(PYTHON) -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

lint: ## Run linting
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy .
	$(PYTHON) -m pylint **/*.py

format: ## Format code
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

security: ## Run security checks
	$(PYTHON) -m bandit -r .
	$(PYTHON) -m safety check

qa: format lint security test-cov ## Run all quality assurance checks

qa-score: ## Quick quality score assessment
	@./qa-fast.sh

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run: ## Run the Streamlit application
	$(PYTHON) -m streamlit run app.py

dev: ## Setup development environment and run app
	./setup-dev.sh
	$(MAKE) run

docker-build: ## Build Docker image
	docker build -t campus-management .

docker-run: ## Run Docker container
	docker run -p 8501:8501 campus-management

docker-compose-dev: ## Run with docker-compose for development
	docker-compose up --build

build: ## Build distribution packages
	$(PYTHON) -m build

release: clean build ## Build and check distribution packages
	$(PYTHON) -m build
	$(PYTHON) -m twine check dist/*

upload-test: build ## Upload to test PyPI
	$(PYTHON) -m twine upload --repository testpypi dist/*

upload: build ## Upload to PyPI
	$(PYTHON) -m twine upload dist/*

# Development workflow shortcuts
dev-setup: install-dev ## Setup development environment
	@echo "Development environment ready!"

ci-local: qa ## Run CI checks locally
	@echo "All CI checks passed!"

pre-commit-all: ## Run pre-commit on all files
	$(PYTHON) -m pre_commit run --all-files

update-deps: ## Update dependencies
	$(UV) pip install --python .venv/bin/python --upgrade -e ".[dev]"

# UV specific commands
uv-install: ## Install dependencies using uv (explicit python)
	$(UV) pip install --python .venv/bin/python -e ".[dev]"

uv-run: ## Run Streamlit app using uv
	$(UV) run --python .venv/bin/python streamlit run app.py

uv-test: ## Run tests using uv
	$(UV) run --python .venv/bin/python pytest tests/ -v

uv-guide: ## Show UV usage guide
	./uv-guide.sh

# Documentation commands
docs-install: ## Install documentation dependencies
	$(UV) pip install --python .venv/bin/python -e ".[docs]"

docs-serve: ## Serve documentation locally
	$(PYTHON) -m mkdocs serve

docs-build: ## Build documentation
	$(PYTHON) -m mkdocs build

docs-deploy: ## Deploy documentation to GitHub Pages
	$(PYTHON) -m mkdocs gh-deploy --force