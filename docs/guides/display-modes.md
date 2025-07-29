# Display Modes Guide

This guide explains how to use different display modes in the analysis tool.

## Available Display Modes

- `term`: Terminal-based plotting using plotext
- `fast`: Interactive web-based plotting using Bokeh
- `fastest`: Basic terminal output
- `plt`/`mpl`: Matplotlib-based plotting
- `plotly`: Plotly-based interactive plots
- `seaborn`/`sb`: Seaborn statistical visualizations

## Environment Detection & Overrides

By default, the tool automatically detects the environment and adjusts the display mode:

- In Docker/SSH: Forces `term` mode for compatibility
- Local environment: Uses specified mode

### Environment Variables

You can control the environment detection behavior using these environment variables:

1. `DISABLE_DOCKER_DETECTION`: Completely disables Docker environment detection
   ```bash
   DISABLE_DOCKER_DETECTION=true uv run run_analysis.py ...
   ```

2. `FORCE_DISPLAY_MODE`: Forces the use of specified display mode regardless of environment
   ```bash
   FORCE_DISPLAY_MODE=true uv run run_analysis.py show csv mn1 -d fast
   ```

## Common Use Cases

### 1. Default Docker Behavior
```bash
# Automatically uses term mode in Docker
uv run run_analysis.py show csv mn1 -d fast --rule supertrend:10,2,close
```

### 2. Force Fast Mode in Docker
```bash
# Forces fast mode even in Docker
FORCE_DISPLAY_MODE=true uv run run_analysis.py show csv mn1 -d fast --rule supertrend:10,2,close
```

### 3. Local Development
```bash
# Uses specified mode
uv run run_analysis.py show csv mn1 -d fast --rule supertrend:10,2,close
```

## Display Mode Features

### Term Mode (`-d term`)
- Works in SSH/Docker environments
- Text-based visualization
- Low resource usage
- No browser required

### Fast Mode (`-d fast`)
- Interactive web-based plots
- Zoomable charts
- Support for large datasets
- Requires browser access
- Uses Bokeh backend

### Fastest Mode (`-d fastest`)
- Basic terminal output
- No plotting overhead
- Best performance
- Limited visualization

## Troubleshooting

### Known Issues

1. Display mode switching to term in Docker:
   - Expected behavior for compatibility
   - Use `FORCE_DISPLAY_MODE=true` to override

2. Browser access in Docker:
   - Some modes require browser access
   - Use SSH port forwarding or expose ports

### Common Solutions

1. If plots don't display:
   ```bash
   # Try terminal mode
   uv run run_analysis.py show csv mn1 -d term
   ```

2. For Docker/SSH sessions:
   ```bash
   # Terminal mode is recommended
   uv run run_analysis.py show csv mn1 -d term
   ```

3. For local development:
   ```bash
   # Any mode works
   uv run run_analysis.py show csv mn1 -d fast
   ```

## Best Practices

1. **Docker/SSH Usage:**
   - Use `term` mode by default
   - Consider resource limitations

2. **Local Development:**
   - Use `fast` or `plotly` for interactivity
   - `fastest` for quick checks

3. **CI/CD Pipelines:**
   - Use `fastest` mode
   - Avoid browser-dependent modes
