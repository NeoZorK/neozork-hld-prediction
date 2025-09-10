"""
Main application file for Pocket Hedge Fund

This is the main entry point for the Pocket Hedge Fund application.
It provides a comprehensive FastAPI-based hedge fund management system
with investor portal, fund management, and real-time portfolio tracking.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.pocket_hedge_fund.database.connection import init_database, close_database, get_db_manager
from src.pocket_hedge_fund.database.models import Base
from src.pocket_hedge_fund.auth.auth_manager import get_auth_manager
from src.pocket_hedge_fund.api.fund_api import router as fund_router
from src.pocket_hedge_fund.api.investment_api import router as investment_router
from src.pocket_hedge_fund.api.portfolio_api import router as portfolio_router
from src.pocket_hedge_fund.api.returns_api import router as returns_router
from src.pocket_hedge_fund.api.web_api import router as web_router
from src.pocket_hedge_fund.api.mobile_api import router as mobile_router

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

# Pydantic models
class UserRegistration(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class PocketHedgeFundApp:
    """Main application class for Pocket Hedge Fund."""
    
    def __init__(self):
        self.app = FastAPI(
            title="NeoZork Pocket Hedge Fund API",
            description="AI-powered hedge fund management platform",
    version="1.0.0",
    docs_url="/docs",
            redoc_url="/redoc"
        )
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup middleware for the application."""
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
        self.app.include_router(web_router)
        self.app.include_router(mobile_router)
        
        # Authentication endpoints
        @self.app.post("/api/v1/auth/register")
        async def register_user(user_data: UserRegistration):
            """Register a new user."""
            try:
                auth_manager = await get_auth_manager()
                
                success, message, user_info = await auth_manager.register_user(
                    email=user_data.email,
                    username=user_data.username,
                    password=user_data.password,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name
                )
                
                if success:
                    return {
                        "success": True,
                        "message": "User registered successfully",
                        "user": user_info
                    }
                else:
                    raise HTTPException(status_code=400, detail=message)
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Registration failed: {e}")
                raise HTTPException(status_code=500, detail="Registration failed")

        @self.app.post("/api/v1/auth/login")
        async def login_user(login_data: UserLogin):
            """Login user."""
            try:
                auth_manager = await get_auth_manager()
                
                success, message, auth_data = await auth_manager.login_user(
                    email=login_data.email,
                    password=login_data.password
                )
                
                if success:
                    return auth_data
                else:
                    raise HTTPException(
                        status_code=401, 
                        detail="Invalid email or password"
                    )
                    
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Login failed: {e}")
                raise HTTPException(status_code=500, detail="Login failed")

        # Error handlers
        @self.app.exception_handler(404)
        async def not_found_handler(request, exc):
            return JSONResponse(
                status_code=404,
                content={"error": "Not found", "message": "The requested resource was not found"}
            )

        @self.app.exception_handler(500)
        async def internal_error_handler(request, exc):
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "message": "An unexpected error occurred"}
            )

    async def startup(self):
        """Application startup."""
        logger.info("🚀 NeoZork Pocket Hedge Fund - Starting Up")
        print("=" * 50)
        print("📊 Features:")
        print("- AI-powered hedge fund management")
        print("- Multi-tier fund support (Mini, Standard, Premium)")
        print("- Real-time portfolio tracking")
        print("- Advanced risk management")
        print("- Investor portal")
        print("- Strategy marketplace")
        print("- Community features")
        print("🔧 Configuration:")
        print("- Host: 0.0.0.0")
        print("- Port: 8080")
        print("- Database: localhost:5432/neozork_fund")
        print("- Debug Mode: false")
        print("📚 API Documentation:")
        print("- Swagger UI: http://0.0.0.0:8080/docs")
        print("- ReDoc: http://0.0.0.0:8080/redoc")
        print("- Health Check: http://0.0.0.0:8080/health")
        print("🎯 Quick Start:")
        print("1. Register a user: POST /api/v1/auth/register")
        print("2. Login: POST /api/v1/auth/login")
        print("3. Create a fund: POST /api/v1/funds/")
        print("4. Invest in fund: POST /api/v1/funds/{fund_id}/invest")
        print("=" * 50)
        
        logger.info("Initializing Pocket Hedge Fund application...")
        
        # Initialize database
        logger.info("Initializing database...")
        await init_database()
        
        # Initialize authentication
        logger.info("Initializing authentication...")
        
        logger.info("Pocket Hedge Fund application initialized successfully")

    async def shutdown(self):
        """Application shutdown."""
        logger.info("Shutting down Pocket Hedge Fund application...")
        await close_database()
        logger.info("Pocket Hedge Fund application shutdown completed")

# Global application instance
app_instance = PocketHedgeFundApp()
app = app_instance.app

# Event handlers
@app.on_event("startup")
async def startup_event():
    """FastAPI startup event."""
    try:
        await app_instance.startup()
        logger.info("Starting Pocket Hedge Fund API server on 0.0.0.0:8080")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """FastAPI shutdown event."""
    try:
        await app_instance.shutdown()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

async def main():
    """Main application entry point."""
    import uvicorn
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "src.pocket_hedge_fund.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    asyncio.run(main())
