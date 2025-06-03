FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Installation minimal system dependencies only needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .

# Optimize requirements installation by removing comments and empty lines
RUN pip install --no-cache-dir --upgrade pip && \
    grep -v "^#" requirements.txt > requirements-prod.txt && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    find /opt/venv -name '*.pyc' -delete && \
    find /opt/venv -name '__pycache__' -delete && \
    find /opt/venv -name '*.dist-info' -print0 | xargs -0 rm -rf && \
    find /opt/venv -name '*.egg-info' -print0 | xargs -0 rm -rf && \
    rm -rf /root/.cache /tmp/* /var/tmp/*

# Final stage - copy only necessary files
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary application files
COPY run_analysis.py mcp_server.py mcp.json ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY docker-entrypoint.sh ./

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Create necessary directories with appropriate permissions
RUN mkdir -p /app/data/cache /app/data/raw_parquet /app/logs /tmp/matplotlib-cache /app/results/plots /app/.pytest_cache \
    && chmod -R 777 /tmp/matplotlib-cache /app/results /app/data /app/logs /app/.pytest_cache

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLCONFIGDIR=/tmp/matplotlib-cache
ENV PYTHONDONTWRITEBYTECODE=1

# Minimal system dependencies for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc
