FROM python:3.11-slim-bookworm AS builder

# Accept build argument for UV usage
ARG USE_UV=true

WORKDIR /app

# Installation minimal system dependencies only needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install uv if USE_UV is true
RUN if [ "$USE_UV" = "true" ]; then \
        mkdir -p /tmp/uv-installer \
        && curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh \
        && chmod +x /tmp/uv-installer/installer.sh \
        && /tmp/uv-installer/installer.sh \
        && if [ -f /root/.local/bin/env ]; then . /root/.local/bin/env; fi \
        && ln -s /root/.local/bin/uv /usr/local/bin/uv \
        && rm -rf /tmp/uv-installer; \
    fi

# Update PATH to include uv if installed
ENV PATH="/root/.local/bin:$PATH"

# Copy configuration and requirements
COPY uv.toml /app/uv.toml
COPY requirements.txt .

# Install dependencies based on USE_UV setting
RUN if [ "$USE_UV" = "true" ]; then \
        grep -v "^#" requirements.txt > requirements-prod.txt && \
        uv pip install --no-cache -r requirements-prod.txt; \
    else \
        grep -v "^#" requirements.txt > requirements-prod.txt && \
        pip install --no-cache-dir -r requirements-prod.txt; \
    fi && \
    find /opt/venv -name '*.pyc' -delete && \
    find /opt/venv -name '__pycache__' -delete && \
    find /opt/venv -name '*.egg-info' -print0 | xargs -0 rm -rf && \
    rm -rf /root/.cache /tmp/* /var/tmp/* /root/.cargo /root/.local/share/uv

# Final stage - copy only necessary files
FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary application files
COPY run_analysis.py ./
COPY neozork_mcp_server.py ./
COPY cursor_mcp_config.json ./
COPY docker.env ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY uv_setup/ ./uv_setup/
COPY docker-entrypoint.sh ./

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh /app/uv_setup/setup_uv.sh /app/uv_setup/update_deps.sh

# Fix readline config for better shell experience
RUN mkdir -p /tmp/bash_config && \
    printf '%s\n' '"\\e[A": history-search-backward' > /tmp/bash_config/.inputrc && \
    printf '%s\n' '"\\e[B": history-search-forward' >> /tmp/bash_config/.inputrc && \
    chmod -R 777 /tmp/bash_config

# Create necessary directories with appropriate permissions
RUN mkdir -p /app/data/cache/csv_converted /app/data/raw_parquet /app/logs /tmp/matplotlib-cache /app/results/plots /app/.pytest_cache \
    && chmod -R 777 /tmp/matplotlib-cache /app/results /app/data /app/logs /app/.pytest_cache

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLCONFIGDIR=/tmp/matplotlib-cache
ENV PYTHONDONTWRITEBYTECODE=1

# Minimize final layer: install only absolutely necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    imagemagick \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc

# Create a non-root user to run the application
RUN groupadd -r neozork && useradd -r -g neozork -s /bin/bash -d /home/neozork neozork \
    && mkdir -p /home/neozork \
    && chown -R neozork:neozork /home/neozork /app

# Switch to non-root user
USER neozork
