# Stage 1: Build the virtual environment using uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV VENV_PATH=/app/.venv
WORKDIR /app

# Create a virtual environment using the global uv
RUN uv venv $VENV_PATH

# Copy only the dependency definitions first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# 1. Install dependencies from the lock file. This is fast and correct.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --python $VENV_PATH/bin/python --frozen --no-dev

# Copy the rest of your application source code
COPY . .

# 2. INSTALL THE LOCAL PROJECT. This is the key step.
#    This command runs the build backend and creates the executable script.
#    We use --no-deps because the dependencies were already installed by `uv sync`.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python $VENV_PATH/bin/python --no-deps .


# Stage 2: Final, minimal image
FROM python:3.12-slim-bookworm

# You might not need git here if your dependencies are all from PyPI.
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the complete virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Note: We don't need to copy the source code again unless your app needs
# to access non-Python files (like templates, data files) at runtime.
# If it's a pure Python API, copying just the venv is enough and more minimal.
# For now, we'll leave this commented out for best practice.
# COPY --from=builder /app /app

# Set the PATH to use the venv's executables
ENV PATH="/app/.venv/bin:$PATH"

# The entrypoint will now find the executable in the PATH
ENTRYPOINT ["flamapy-mcp"]
CMD ["--help"]