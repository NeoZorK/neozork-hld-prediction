FROM python:3.11-slim

WORKDIR /app

# Installation system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copying requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/cache /app/data/raw_parquet /app/logs

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "mcp_server.py"]

USER nobody