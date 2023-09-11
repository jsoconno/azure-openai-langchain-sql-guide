.PHONY: start install upgrade env run lint format test clean docker-build docker-run

start:
	@echo "Setting up virtual environment..."
	@export VIRTUAL_ENV=".venv" && python3 -m venv $$VIRTUAL_ENV
	@echo "Virtual environment setup complete."
	@echo "To activate the virtual environment, run 'source .venv/bin/activate'"

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "Dependencies installed."

upgrade:
	@echo "Upgrading all packages..."
	@pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
	@echo "All packages upgraded."

env:
	@echo "Run 'set -o allexport; source .env; set +o allexport' to load environment variables."

run:
	@echo "Running application..."
	@python app.py

lint:
	@echo "Running linter..."
	@flake8 .
	@echo "Linting complete."

format:
	@echo "Running black code formatter..."
	@black .
	@echo "Code formatting complete."

test:
	@echo "Running tests..."
	@pytest
	@echo "Tests complete."

clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@echo "Cleaned up."

docker-build:
	@echo "Building Docker image..."
	@docker build -t azure-openai-langchain -f docker/Dockerfile .
	@echo "Docker image built successfully."

docker-run:
	@echo "Running Docker container..."
	@docker run --env-file .env -it azure-openai-langchain /bin/bash
	@echo "Docker container is running."
