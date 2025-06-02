FROM python:3.11-slim as builder

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
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage - copy only necessary files
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary application files
COPY run_analysis.py mcp_server.py mcp.json ./
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create necessary directories
RUN mkdir -p /app/data/cache /app/data/raw_parquet /app/logs

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Set non-root user for security
USER nobody

# Container entrypoint is defined in docker-compose.yml

