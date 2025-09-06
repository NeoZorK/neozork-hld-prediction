#!/bin/bash
# Deploy NeoZork Interactive System on Apple Container

set -e

echo "🍎 Deploying NeoZork Interactive System on Apple Container"
echo "=========================================================="

# Check if running on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "❌ Error: This script requires Apple Silicon (arm64)"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    exit 1
fi

# Build Apple Container image
echo "🔨 Building Apple Container image..."
docker build -f Dockerfile.apple -t neozork-interactive:apple-latest .

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/{cache/csv_converted,raw_parquet,indicators/{parquet,csv,json},cleaned_data}
mkdir -p logs plots results models monitoring

# Set permissions
echo "🔐 Setting permissions..."
chmod +x interactive/neozork.py
chmod +x scripts/*.sh

# Deploy with docker-compose
echo "🚀 Deploying with docker-compose..."
docker-compose -f docker-compose.apple.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose -f docker-compose.apple.yml ps

# Show logs
echo "📋 Recent logs:"
docker-compose -f docker-compose.apple.yml logs --tail=20

echo ""
echo "✅ Deployment completed!"
echo "🌐 Interactive system: http://localhost:8080"
echo "📊 Monitoring: http://localhost:9090"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose -f docker-compose.apple.yml logs -f"
echo "  Stop services: docker-compose -f docker-compose.apple.yml down"
echo "  Restart services: docker-compose -f docker-compose.apple.yml restart"
echo "  Scale services: docker-compose -f docker-compose.apple.yml up -d --scale neozork-interactive=3"
