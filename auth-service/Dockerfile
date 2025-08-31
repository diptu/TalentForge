# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --upgrade pip && pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install production dependencies
RUN uv sync --no-dev

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy the app source code
COPY . .

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Add uv's virtual environment bin to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
