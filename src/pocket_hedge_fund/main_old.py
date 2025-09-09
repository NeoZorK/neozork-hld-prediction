"""
Pocket Hedge Fund - Main Application

This is the main entry point for the Pocket Hedge Fund application.
It initializes all components, sets up the database, and starts the API server.
"""

import asyncio
import logging
import os
import signal
import sys
from pathlib import Path
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import asyncpg

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.database.connection import init_database, close_database, get_db_manager
from src.pocket_hedge_fund.database.models import Base
from src.pocket_hedge_fund.auth.auth_manager import get_auth_manager
from src.pocket_hedge_fund.api.fund_api import router as fund_router
from src.pocket_hedge_fund.api.investment_api import router as investment_router
from src.pocket_hedge_fund.api.portfolio_api import router as portfolio_router
from src.pocket_hedge_fund.api.returns_api import router as returns_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/pocket_hedge_fund.log')
    ]
)
logger = logging.getLogger(__name__)


class PocketHedgeFundApp:
    """
    Main Pocket Hedge Fund application class.
    
    This class orchestrates the entire application including:
    - Database initialization
    - Authentication setup
    - API server configuration
    - Component initialization
    - Graceful shutdown handling
    """
    
    def __init__(self):
        self.app = None
        self.running = False
        self.db_manager = None
        self.auth_manager = None
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        asyncio.create_task(self.shutdown())
    
    async def initialize(self):
        """Initialize all application components."""
        try:
            logger.info("Initializing Pocket Hedge Fund application...")
            
            # Create logs directory
            os.makedirs('logs', exist_ok=True)
            
            # Initialize database
            logger.info("Initializing database...")
            await init_database()
            self.db_manager = await get_db_manager()
            
            # Initialize authentication
            logger.info("Initializing authentication...")
            self.auth_manager = await get_auth_manager()
            
            # Create FastAPI app
            logger.info("Creating FastAPI application...")
            self.app = FastAPI(
                title="NeoZork Pocket Hedge Fund API",
                description="AI-powered hedge fund management platform",
    version="1.0.0",
    docs_url="/docs",
                redoc_url="/redoc"
            )
            
            # Setup middleware
            self._setup_middleware()
            
            # Setup routes
            self._setup_routes()
            
            # Setup error handlers
            self._setup_error_handlers()
            
            logger.info("Pocket Hedge Fund application initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            raise
    
    def _setup_middleware(self):
        """Setup FastAPI middleware."""
        # CORS middleware
        self.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        # Trusted host middleware
        self.app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

    def _setup_routes(self):
        """Setup API routes."""
# Health check endpoint
        @self.app.get("/health")
async def health_check():
            """Health check endpoint."""
            try:
                # Check database connection
                db_manager = await get_db_manager()
                await db_manager.execute_query("SELECT 1")
        
        return {
                    "status": "healthy",
                    "timestamp": "2025-01-05T00:00:00Z",
            "version": "1.0.0",
                    "database": "connected",
                    "authentication": "ready"
                }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
                raise HTTPException(status_code=503, detail="Service unhealthy")

# Root endpoint
        @self.app.get("/")
async def root():
            """Root endpoint."""
    return {
                "message": "NeoZork Pocket Hedge Fund API",
        "version": "1.0.0",
                "docs": "/docs",
                "health": "/health"
    }

# Include API routers
        self.app.include_router(fund_router)
        self.app.include_router(investment_router)
        self.app.include_router(portfolio_router)
        self.app.include_router(returns_router)
        
        # Authentication endpoints
        @self.app.post("/api/v1/auth/register")
        async def register_user(user_data: dict):
            """Register a new user."""
            try:
                auth_manager = await get_auth_manager()
                
                success, message, user_info = await auth_manager.register_user(
                    email=user_data.get('email'),
                    username=user_data.get('username'),
                    password=user_data.get('password'),
                    first_name=user_data.get('first_name', ''),
                    last_name=user_data.get('last_name', ''),
                    phone=user_data.get('phone', ''),
                    country=user_data.get('country', '')
                )
                
                if success:
                    return {"success": True, "message": message, "user": user_info}
                else:
                    raise HTTPException(status_code=400, detail=message)
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"User registration failed: {e}")
                raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
        
        @self.app.post("/api/v1/auth/login")
        async def login_user(credentials: dict):
            """Login user."""
            try:
                auth_manager = await get_auth_manager()
                
                success, message, auth_data = await auth_manager.login_user(
                    email=credentials.get('email'),
                    password=credentials.get('password'),
                    mfa_token=credentials.get('mfa_token'),
                    ip_address=credentials.get('ip_address'),
                    user_agent=credentials.get('user_agent')
                )
                
                if success:
                    return {"success": True, "message": message, "data": auth_data}
                else:
                    raise HTTPException(status_code=401, detail=message)
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"User login failed: {e}")
                raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
        
        @self.app.post("/api/v1/auth/verify")
        async def verify_token(token_data: dict):
            """Verify JWT token."""
            try:
                auth_manager = await get_auth_manager()
                
                success, message, user_data = await auth_manager.verify_token(
                    token_data.get('token')
                )
                
                if success:
                    return {"success": True, "message": message, "user": user_data}
                else:
                    raise HTTPException(status_code=401, detail=message)
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Token verification failed: {e}")
                raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")
    
    def _setup_error_handlers(self):
        """Setup global error handlers."""
        @self.app.exception_handler(Exception)
        async def global_exception_handler(request, exc):
            """Global exception handler."""
            logger.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "detail": str(exc) if os.getenv('DEBUG') == 'true' else None
                }
            )
    
    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        """Run the application."""
        try:
            if not self.app:
                await self.initialize()
            
            logger.info(f"Starting Pocket Hedge Fund API server on {host}:{port}")
            self.running = True
            
            # Run with uvicorn
            config = uvicorn.Config(
                app=self.app,
                host=host,
                port=port,
                log_level="info",
                access_log=True
            )
            server = uvicorn.Server(config)
            await server.serve()
            
        except Exception as e:
            logger.error(f"Failed to run application: {e}")
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Shutdown the application gracefully."""
        if not self.running:
            return
        
        logger.info("Shutting down Pocket Hedge Fund application...")
        self.running = False
        
        try:
            # Close database connections
            if self.db_manager:
                await close_database()
            
            logger.info("Pocket Hedge Fund application shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


async def main():
    """Main entry point."""
    app = PocketHedgeFundApp()
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8080'))
    
    try:
        await app.run(host=host, port=port)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the application
    asyncio.run(main())