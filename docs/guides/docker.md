# Docker Guide

Containerized development and deployment setup.

## Quick Start

```bash
# Build and run
docker compose up --build

# Interactive mode
docker compose run --rm neozork-hld

# Run analysis in container
docker compose run --rm neozork-hld python run_analysis.py demo
```

## Configuration

**Main files:**
- `docker-compose.yml` - Container configuration
- `Dockerfile` - Image definition
- `docker-entrypoint.sh` - Startup script

## Common Commands

```bash
# Build image
docker compose build

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Clean up
docker compose down -v
docker system prune -a
```

## Environment Variables

Set in `.env` file or shell:

```bash
POLYGON_API_KEY=your_key_here
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

## Troubleshooting

**Build issues:**
```bash
docker compose build --no-cache
```

**Permission errors:**
```bash
chmod +x docker-entrypoint.sh
```

**Clean restart:**
```bash
docker compose down -v
docker system prune -a
docker compose up --build
```

For CI/CD integration: [CI/CD Guide](ci-cd.md)