"""Forum System - Community discussions and forums"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class PostType(Enum):
    """Post type enumeration."""
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"
    STRATEGY_SHARE = "strategy_share"
    MARKET_ANALYSIS = "market_analysis"


class PostStatus(Enum):
    """Post status enumeration."""
    ACTIVE = "active"
    LOCKED = "locked"
    DELETED = "deleted"
    PINNED = "pinned"


class ForumSystem:
    """Community discussions and forums system."""
    
    def __init__(self):
        self.forums: Dict[str, Dict[str, Any]] = {}
        self.posts: Dict[str, Dict[str, Any]] = {}
        self.comments: Dict[str, List[Dict[str, Any]]] = {}
        self.user_activity: Dict[str, Dict[str, Any]] = {}
        self.moderators: Dict[str, List[str]] = {}
        
    async def create_forum(self, name: str, description: str,
                          category: str, is_public: bool = True) -> Dict[str, Any]:
        """Create a new forum."""
        try:
            forum_id = str(uuid.uuid4())
            
            forum = {
                'forum_id': forum_id,
                'name': name,
                'description': description,
                'category': category,
                'is_public': is_public,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'post_count': 0,
                'member_count': 0,
                'rules': []
            }
            
            self.forums[forum_id] = forum
            
            logger.info(f"Created forum: {name} ({forum_id})")
            return {
                'status': 'success',
                'forum_id': forum_id,
                'forum': forum
            }
            
        except Exception as e:
            logger.error(f"Failed to create forum: {e}")
            return {'error': str(e)}
    
    async def create_post(self, forum_id: str, author_id: str, title: str,
                         content: str, post_type: PostType = PostType.DISCUSSION,
                         tags: List[str] = None) -> Dict[str, Any]:
        """Create a new post in a forum."""
        try:
            if forum_id not in self.forums:
                return {'error': 'Forum not found'}
            
            post_id = str(uuid.uuid4())
            
            post = {
                'post_id': post_id,
                'forum_id': forum_id,
                'author_id': author_id,
                'title': title,
                'content': content,
                'post_type': post_type.value,
                'tags': tags or [],
                'status': PostStatus.ACTIVE.value,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'view_count': 0,
                'like_count': 0,
                'comment_count': 0,
                'is_pinned': False
            }
            
            self.posts[post_id] = post
            
            # Update forum post count
            self.forums[forum_id]['post_count'] += 1
            self.forums[forum_id]['updated_at'] = datetime.now()
            
            # Initialize comments list
            self.comments[post_id] = []
            
            logger.info(f"Created post: {title} ({post_id}) in forum {forum_id}")
            return {
                'status': 'success',
                'post_id': post_id,
                'post': post
            }
            
        except Exception as e:
            logger.error(f"Failed to create post: {e}")
            return {'error': str(e)}
    
    async def add_comment(self, post_id: str, author_id: str, content: str,
                         parent_comment_id: str = None) -> Dict[str, Any]:
        """Add a comment to a post."""
        try:
            if post_id not in self.posts:
                return {'error': 'Post not found'}
            
            comment_id = str(uuid.uuid4())
            
            comment = {
                'comment_id': comment_id,
                'post_id': post_id,
                'author_id': author_id,
                'content': content,
                'parent_comment_id': parent_comment_id,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'like_count': 0,
                'reply_count': 0
            }
            
            # Add comment
            if post_id not in self.comments:
                self.comments[post_id] = []
            self.comments[post_id].append(comment)
            
            # Update post comment count
            self.posts[post_id]['comment_count'] += 1
            self.posts[post_id]['updated_at'] = datetime.now()
            
            # Update parent comment reply count if applicable
            if parent_comment_id:
                for comment_list in self.comments.values():
                    for c in comment_list:
                        if c['comment_id'] == parent_comment_id:
                            c['reply_count'] += 1
                            break
            
            logger.info(f"Added comment {comment_id} to post {post_id}")
            return {
                'status': 'success',
                'comment_id': comment_id,
                'comment': comment
            }
            
        except Exception as e:
            logger.error(f"Failed to add comment: {e}")
            return {'error': str(e)}
    
    async def get_forum_posts(self, forum_id: str, page: int = 1, 
                            page_size: int = 20, sort_by: str = "newest") -> Dict[str, Any]:
        """Get posts from a forum."""
        try:
            if forum_id not in self.forums:
                return {'error': 'Forum not found'}
            
            # Get all posts for this forum
            forum_posts = [post for post in self.posts.values() 
                          if post['forum_id'] == forum_id and post['status'] == PostStatus.ACTIVE.value]
            
            # Sort posts
            if sort_by == "newest":
                forum_posts.sort(key=lambda x: x['created_at'], reverse=True)
            elif sort_by == "popular":
                forum_posts.sort(key=lambda x: x['view_count'], reverse=True)
            elif sort_by == "most_commented":
                forum_posts.sort(key=lambda x: x['comment_count'], reverse=True)
            
            # Paginate
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_posts = forum_posts[start_idx:end_idx]
            
            return {
                'forum_id': forum_id,
                'posts': paginated_posts,
                'total_posts': len(forum_posts),
                'page': page,
                'page_size': page_size,
                'total_pages': (len(forum_posts) + page_size - 1) // page_size
            }
            
        except Exception as e:
            logger.error(f"Failed to get forum posts: {e}")
            return {'error': str(e)}
    
    async def get_post_comments(self, post_id: str, page: int = 1, 
                              page_size: int = 50) -> Dict[str, Any]:
        """Get comments for a post."""
        try:
            if post_id not in self.posts:
                return {'error': 'Post not found'}
            
            comments = self.comments.get(post_id, [])
            
            # Sort by creation date (oldest first for threaded discussion)
            comments.sort(key=lambda x: x['created_at'])
            
            # Paginate
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_comments = comments[start_idx:end_idx]
            
            return {
                'post_id': post_id,
                'comments': paginated_comments,
                'total_comments': len(comments),
                'page': page,
                'page_size': page_size,
                'total_pages': (len(comments) + page_size - 1) // page_size
            }
            
        except Exception as e:
            logger.error(f"Failed to get post comments: {e}")
            return {'error': str(e)}
    
    async def like_post(self, post_id: str, user_id: str) -> Dict[str, Any]:
        """Like a post."""
        try:
            if post_id not in self.posts:
                return {'error': 'Post not found'}
            
            # TODO: Implement like tracking to prevent duplicate likes
            # For now, just increment the count
            
            self.posts[post_id]['like_count'] += 1
            self.posts[post_id]['updated_at'] = datetime.now()
            
            logger.info(f"User {user_id} liked post {post_id}")
            return {
                'status': 'success',
                'post_id': post_id,
                'like_count': self.posts[post_id]['like_count']
            }
            
        except Exception as e:
            logger.error(f"Failed to like post: {e}")
            return {'error': str(e)}
    
    async def search_posts(self, query: str, forum_id: str = None, 
                          post_type: PostType = None, tags: List[str] = None) -> Dict[str, Any]:
        """Search posts across forums."""
        try:
            matching_posts = []
            
            for post in self.posts.values():
                # Filter by forum if specified
                if forum_id and post['forum_id'] != forum_id:
                    continue
                
                # Filter by post type if specified
                if post_type and post['post_type'] != post_type.value:
                    continue
                
                # Filter by tags if specified
                if tags and not any(tag in post['tags'] for tag in tags):
                    continue
                
                # Text search
                query_lower = query.lower()
                if (query_lower in post['title'].lower() or 
                    query_lower in post['content'].lower() or
                    any(query_lower in tag.lower() for tag in post['tags'])):
                    matching_posts.append(post)
            
            # Sort by relevance (for now, just by creation date)
            matching_posts.sort(key=lambda x: x['created_at'], reverse=True)
            
            return {
                'query': query,
                'matching_posts': matching_posts,
                'total_matches': len(matching_posts)
            }
            
        except Exception as e:
            logger.error(f"Failed to search posts: {e}")
            return {'error': str(e)}
    
    def get_forum_summary(self) -> Dict[str, Any]:
        """Get forum system summary."""
        total_forums = len(self.forums)
        total_posts = len(self.posts)
        total_comments = sum(len(comments) for comments in self.comments.values())
        
        # Category distribution
        category_distribution = {}
        for forum in self.forums.values():
            category = forum['category']
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        return {
            'total_forums': total_forums,
            'total_posts': total_posts,
            'total_comments': total_comments,
            'category_distribution': category_distribution,
            'active_forums': len([f for f in self.forums.values() if f['post_count'] > 0])
        }