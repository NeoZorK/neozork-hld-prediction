"""
Web Interface API Router

This module provides endpoints for serving the web interface
and handling web-specific API requests.
"""

import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.pocket_hedge_fund.auth.auth_manager import get_current_user

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Pydantic models
class UserProfileResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    created_at: str
    is_active: bool

class WebStatsResponse(BaseModel):
    total_users: int
    total_funds: int
    total_investments: int
    total_volume: float

@router.get("/web", response_class=HTMLResponse)
async def serve_web_interface():
    """Serve the main web interface."""
    try:
        web_path = Path(__file__).parent.parent.parent.parent / "src" / "web" / "templates" / "index.html"
        
        if not web_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Web interface not found"
            )
        
        with open(web_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return HTMLResponse(content=content)
    
    except Exception as e:
        logger.error(f"Failed to serve web interface: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to load web interface"
        )

@router.get("/static/{file_path:path}")
async def serve_static_files(file_path: str):
    """Serve static files (CSS, JS, images)."""
    try:
        static_path = Path(__file__).parent.parent.parent.parent / "src" / "web" / "static" / file_path
        
        if not static_path.exists():
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        return FileResponse(static_path)
    
    except Exception as e:
        logger.error(f"Failed to serve static file {file_path}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to load static file"
        )

@router.get("/api/v1/users/profile", response_model=UserProfileResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile information."""
    try:
        return UserProfileResponse(
            id=str(current_user['id']),
            username=current_user.get('username', ''),
            email=current_user.get('email', ''),
            first_name=current_user.get('first_name', ''),
            last_name=current_user.get('last_name', ''),
            role=current_user.get('role', 'investor'),
            created_at=current_user.get('created_at', ''),
            is_active=current_user.get('is_active', True)
        )
    
    except Exception as e:
        logger.error(f"Failed to get user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )

@router.get("/api/v1/web/stats", response_model=WebStatsResponse)
async def get_web_stats():
    """Get general statistics for the web interface."""
    try:
        from src.pocket_hedge_fund.database.connection import get_db_manager
        
        db_manager = await get_db_manager()
        
        # Get user count
        user_result = await db_manager.execute_query("SELECT COUNT(*) as count FROM users")
        total_users = user_result[0]['count'] if user_result else 0
        
        # Get fund count
        fund_result = await db_manager.execute_query("SELECT COUNT(*) as count FROM funds")
        total_funds = fund_result[0]['count'] if fund_result else 0
        
        # Get investment count
        investment_result = await db_manager.execute_query("SELECT COUNT(*) as count FROM investments")
        total_investments = investment_result[0]['count'] if investment_result else 0
        
        # Get total volume
        volume_result = await db_manager.execute_query("SELECT SUM(amount) as total FROM investments")
        total_volume = float(volume_result[0]['total']) if volume_result and volume_result[0]['total'] else 0.0
        
        return WebStatsResponse(
            total_users=total_users,
            total_funds=total_funds,
            total_investments=total_investments,
            total_volume=total_volume
        )
    
    except Exception as e:
        logger.error(f"Failed to get web stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get web statistics"
        )

@router.post("/api/v1/auth/verify")
async def verify_token(token_data: dict):
    """Verify JWT token for web interface."""
    try:
        from src.pocket_hedge_fund.auth.auth_manager import get_auth_manager
        
        auth_manager = await get_auth_manager()
        
        success, message, user_data = await auth_manager.verify_token(
            token_data.get('token')
        )
        
        if success:
            return {
                "success": True,
                "message": message,
                "user": user_data
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )
