"""
NeoZork Pocket Hedge Fund - Main Application Entry Point

This module provides the main application entry point for the NeoZork Pocket Hedge Fund
including system initialization, startup, and graceful shutdown.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

from .integration.system_integrator import SystemIntegrator, SystemStatus
from .deployment.deployment_manager import DeploymentManager, DeploymentEnvironment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/neozork.log')
    ]
)
logger = logging.getLogger(__name__)

class NeoZorkApplication:
    """Main NeoZork Pocket Hedge Fund application"""
    
    def __init__(self):
        self.system_integrator = None
        self.deployment_manager = None
        self.environment = DeploymentEnvironment.DEVELOPMENT
        self.shutdown_event = asyncio.Event()
        
    async def initialize(self, environment: str = "development", config_path: Optional[str] = None):
        """Initialize the application"""
        try:
            logger.info("Initializing NeoZork Pocket Hedge Fund Application")
            
            # Set environment
            self.environment = DeploymentEnvironment(environment)
            
            # Initialize system integrator
            self.system_integrator = SystemIntegrator()
            await self.system_integrator.initialize(config_path)
            
            # Initialize deployment manager
            self.deployment_manager = DeploymentManager()
            await self.deployment_manager.initialize(self.environment)
            
            logger.info("Application initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Application initialization failed: {e}")
            raise
    
    async def start(self):
        """Start the application"""
        try:
            logger.info("Starting NeoZork Pocket Hedge Fund Application")
            
            # Start system integrator
            await self.system_integrator.start()
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            logger.info("Application started successfully")
            
            # Keep running until shutdown
            await self.shutdown_event.wait()
            
        except Exception as e:
            logger.error(f"Application startup failed: {e}")
            raise
    
    async def stop(self):
        """Stop the application gracefully"""
        try:
            logger.info("Stopping NeoZork Pocket Hedge Fund Application")
            
            # Stop system integrator
            if self.system_integrator:
                await self.system_integrator.stop()
            
            # Set shutdown event
            self.shutdown_event.set()
            
            logger.info("Application stopped successfully")
            
        except Exception as e:
            logger.error(f"Application shutdown failed: {e}")
            raise
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown")
            asyncio.create_task(self.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def get_health_status(self):
        """Get application health status"""
        try:
            if self.system_integrator:
                return await self.system_integrator.get_system_health()
            else:
                return {
                    "status": "not_initialized",
                    "error": "System integrator not initialized"
                }
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_metrics(self):
        """Get application metrics"""
        try:
            if self.system_integrator:
                return await self.system_integrator.get_system_metrics()
            else:
                return {
                    "status": "not_initialized",
                    "error": "System integrator not initialized"
                }
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

# Global application instance
app = None

async def main():
    """Main application entry point"""
    global app
    
    try:
        # Parse command line arguments
        import argparse
        parser = argparse.ArgumentParser(description="NeoZork Pocket Hedge Fund")
        parser.add_argument("--environment", default="development", 
                          choices=["development", "staging", "production"],
                          help="Deployment environment")
        parser.add_argument("--config", help="Configuration file path")
        parser.add_argument("--deploy", action="store_true", 
                          help="Deploy the application")
        parser.add_argument("--version", default="1.0.0", 
                          help="Application version")
        
        args = parser.parse_args()
        
        # Create application instance
        app = NeoZorkApplication()
        
        # Initialize application
        await app.initialize(args.environment, args.config)
        
        # Deploy if requested
        if args.deploy:
            logger.info(f"Deploying application version {args.version}")
            deployment_id = await app.deployment_manager.deploy(args.version)
            logger.info(f"Deployment completed: {deployment_id}")
            return
        
        # Start application
        await app.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    finally:
        if app:
            await app.stop()

def run():
    """Run the application"""
    try:
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(exist_ok=True)
        
        # Run the application
        asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Failed to run application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()