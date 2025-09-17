"""Community API - RESTful API endpoints for community features"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uuid

logger = logging.getLogger(__name__)

# Initialize FastAPI router
router = APIRouter(prefix="/api/v1/community", tags=["community"])
security = HTTPBearer()


class CopyMode(str, Enum):
    """Copy mode enumeration."""
    FULL_COPY = "full_copy"
    PROPORTIONAL_COPY = "proportional_copy"
    SIGNAL_ONLY = "signal_only"


class PostType(str, Enum):
    """Post type enumeration."""
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"
    STRATEGY_SHARE = "strategy_share"
    MARKET_ANALYSIS = "market_analysis"


class FollowTraderRequest(BaseModel):
    """Request model for following a trader."""
    leader_id: str = Field(..., description="Leader trader ID")
    copy_mode: CopyMode = Field(default=CopyMode.PROPORTIONAL_COPY, description="Copy mode")
    copy_percentage: float = Field(default=1.0, description="Copy percentage", ge=0, le=1)
    max_copy_amount: float = Field(default=10000.0, description="Max copy amount", gt=0)


class CreatePostRequest(BaseModel):
    """Request model for creating a post."""
    title: str = Field(..., description="Post title", min_length=1, max_length=200)
    content: str = Field(..., description="Post content", min_length=1, max_length=10000)
    post_type: PostType = Field(default=PostType.DISCUSSION, description="Post type")
    tags: Optional[List[str]] = Field(None, description="Post tags")


class CommunityAPI:
    """Community features API endpoints."""
    
    def __init__(self):
        self.social_trading = None  # Will be injected
        self.leaderboard_system = None  # Will be injected
        self.forum_system = None  # Will be injected
        self.gamification_system = None  # Will be injected
        
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
        """Get current authenticated user."""
        # TODO: Implement JWT token validation
        return "user_123"  # Placeholder
    
    # Social Trading Endpoints
    @router.post("/follow")
    async def follow_trader(
        self,
        request: FollowTraderRequest,
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Follow a trader for copy trading."""
        try:
            result = await self.social_trading.follow_trader(
                follower_id=current_user,
                leader_id=request.leader_id,
                copy_mode=request.copy_mode,
                copy_percentage=request.copy_percentage,
                max_copy_amount=request.max_copy_amount
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Successfully following trader',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Failed to follow trader: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/following")
    async def get_following(
        self,
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get list of traders being followed."""
        try:
            result = await self.social_trading.get_following(current_user)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Failed to get following: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    # Forum Endpoints
    @router.post("/forums/{forum_id}/posts")
    async def create_post(
        self,
        forum_id: str = Path(..., description="Forum ID"),
        request: CreatePostRequest,
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Create a new post in a forum."""
        try:
            result = await self.forum_system.create_post(
                forum_id=forum_id,
                author_id=current_user,
                title=request.title,
                content=request.content,
                post_type=request.post_type,
                tags=request.tags
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'message': 'Post created successfully',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Failed to create post: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @router.get("/forums/{forum_id}/posts")
    async def get_forum_posts(
        self,
        forum_id: str = Path(..., description="Forum ID"),
        page: int = Query(1, description="Page number", ge=1),
        page_size: int = Query(20, description="Page size", ge=1, le=100),
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get posts from a forum."""
        try:
            result = await self.forum_system.get_forum_posts(
                forum_id=forum_id,
                page=page,
                page_size=page_size
            )
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Failed to get forum posts: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    # Gamification Endpoints
    @router.get("/profile")
    async def get_user_profile(
        self,
        current_user: str = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """Get user's gamification profile."""
        try:
            result = await self.gamification_system.get_user_profile(current_user)
            
            if 'error' in result:
                raise HTTPException(status_code=400, detail=result['error'])
            
            return {
                'status': 'success',
                'data': result
            }
            
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


# Create API instance
community_api = CommunityAPI()

# Add routes to router
router.add_api_route("/follow", community_api.follow_trader, methods=["POST"])
router.add_api_route("/following", community_api.get_following, methods=["GET"])
router.add_api_route("/forums/{forum_id}/posts", community_api.create_post, methods=["POST"])
router.add_api_route("/forums/{forum_id}/posts", community_api.get_forum_posts, methods=["GET"])
router.add_api_route("/profile", community_api.get_user_profile, methods=["GET"])