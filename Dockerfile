# Multi-stage Dockerfile for SuperClaude Pro development and production

# Base stage with common dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 superclaude && \
    mkdir -p /home/superclaude/.claude && \
    chown -R superclaude:superclaude /home/superclaude

WORKDIR /app

# Development stage
FROM base as development

# Install development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    less \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install in editable mode with all dev dependencies
RUN pip install -e ".[dev,docs,telemetry]"

# Install pre-commit
RUN pip install pre-commit && \
    git init . && \
    pre-commit install || true

# Copy rest of the application
COPY . .

# Change ownership
RUN chown -R superclaude:superclaude /app

USER superclaude

# Development command
CMD ["bash"]

# Testing stage
FROM base as testing

COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install with test dependencies
RUN pip install -e ".[dev]"

COPY tests/ ./tests/
COPY .coveragerc ./

USER superclaude

# Run tests by default
CMD ["pytest", "--cov=superclaude_pro", "--cov-report=term-missing"]

# Builder stage
FROM base as builder

# Install build dependencies
RUN pip install build twine

COPY pyproject.toml README.md ./
COPY src/ ./src/

# Build wheel
RUN python -m build --wheel --outdir /dist

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN useradd -m -u 1000 superclaude && \
    mkdir -p /home/superclaude/.claude && \
    chown -R superclaude:superclaude /home/superclaude

# Copy wheel from builder
COPY --from=builder /dist/*.whl /tmp/

# Install the wheel
RUN pip install /tmp/*.whl && \
    rm -rf /tmp/*.whl

USER superclaude
WORKDIR /home/superclaude

# Production command
CMD ["superclaude-pro", "--help"]