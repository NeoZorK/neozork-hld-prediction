"""
Main FastAPI application for Pocket Hedge Fund.

This module provides the main FastAPI application with all routes,
middleware, and configuration for the Pocket Hedge Fund system.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .database import DatabaseManager
from .auth import AuthManager
from .auth.middleware import AuthMiddleware
from .api import AuthAPI, FundAPI, PortfolioAPI, PerformanceAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    """
    # Startup
    logger.info("Starting Pocket Hedge Fund API...")
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        await db_manager.initialize()
        app.state.db_manager = db_manager
        logger.info("Database manager initialized")
        
        # Initialize auth manager
        auth_manager = AuthManager(db_manager)
        await auth_manager.initialize()
        app.state.auth_manager = auth_manager
        logger.info("Auth manager initialized")
        
        # Create database tables if they don't exist
        await db_manager.create_tables()
        logger.info("Database tables created/verified")
        
        logger.info("Pocket Hedge Fund API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start Pocket Hedge Fund API: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Pocket Hedge Fund API...")
    
    try:
        # Close database connections
        if hasattr(app.state, 'db_manager'):
            await app.state.db_manager.close()
            logger.info("Database connections closed")
        
        logger.info("Pocket Hedge Fund API shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="Pocket Hedge Fund API",
    description="REST API for Pocket Hedge Fund - Advanced Trading and Portfolio Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Add authentication middleware
@app.middleware("http")
async def auth_middleware(request, call_next):
    """Authentication middleware wrapper."""
    if hasattr(app.state, 'auth_manager'):
        auth_middleware_instance = AuthMiddleware(app, app.state.auth_manager)
        return await auth_middleware_instance.dispatch(request, call_next)
    else:
        # If auth manager not initialized, skip authentication
        return await call_next(request)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the API
    """
    try:
        # Check database connection
        db_status = "healthy"
        if hasattr(app.state, 'db_manager'):
            try:
                await app.state.db_manager.health_check()
            except Exception:
                db_status = "unhealthy"
        
        # Check auth manager
        auth_status = "healthy"
        if not hasattr(app.state, 'auth_manager'):
            auth_status = "unhealthy"
        
        overall_status = "healthy" if db_status == "healthy" and auth_status == "healthy" else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": "2024-01-01T00:00:00Z",  # Will be replaced with actual timestamp
            "version": "1.0.0",
            "services": {
                "database": db_status,
                "authentication": auth_status
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    
    Returns:
        API information
    """
    return {
        "message": "Pocket Hedge Fund API",
        "version": "1.0.0",
        "description": "Advanced Trading and Portfolio Management System",
        "docs_url": "/docs",
        "health_url": "/health"
    }


# Include API routers
app.include_router(AuthAPI.router, prefix="/api/v1")
app.include_router(FundAPI.router, prefix="/api/v1")
app.include_router(PortfolioAPI.router, prefix="/api/v1")
app.include_router(PerformanceAPI.router, prefix="/api/v1")


# Custom OpenAPI schema
def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Pocket Hedge Fund API",
        version="1.0.0",
        description="""
        ## Pocket Hedge Fund API
        
        Advanced Trading and Portfolio Management System with:
        
        * **Authentication & Authorization** - JWT-based auth with RBAC
        * **Fund Management** - Create and manage investment funds
        * **Portfolio Management** - Track positions and performance
        * **Performance Analytics** - Comprehensive performance metrics
        * **Risk Management** - Advanced risk monitoring and controls
        
        ### Features
        
        * 🔐 **Secure Authentication** - JWT tokens with refresh mechanism
        * 📊 **Real-time Analytics** - Live performance tracking
        * 🛡️ **Risk Controls** - Automated risk management
        * 📈 **Advanced Metrics** - Sharpe ratio, VaR, drawdown analysis
        * 🔄 **API Integration** - RESTful API with OpenAPI documentation
        
        ### Getting Started
        
        1. Register a new account via `/auth/register`
        2. Login to get access token via `/auth/login`
        3. Create a fund via `/funds/`
        4. Manage positions via `/portfolios/{fund_id}/positions`
        5. Track performance via `/performance/{fund_id}/metrics`
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add security requirements
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Development server configuration
if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting Pocket Hedge Fund API on {host}:{port}")
    
    uvicorn.run(
        "src.pocket_hedge_fund.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )