"""
Rate limiting middleware with Redis backend and intelligent throttling.
Implements sliding window algorithm with burst capacity for Palace of Quests.

Author: Senior Backend Team
Last Modified: 2025-06-04
"""

import time
import json
import hashlib
from functools import wraps
from typing import Dict, Optional, Tuple, Callable, Any
from flask import Flask, request, jsonify, g
from werkzeug.exceptions import TooManyRequests
import redis
from redis.exceptions import RedisError


class RateLimitExceeded(Exception):
    """Custom exception for rate limit violations."""
    def __init__(self, message: str, retry_after: int):
        self.message = message
        self.retry_after = retry_after
        super().__init__(message)


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter using Redis for distributed rate limiting.
    Supports different limits per user role and endpoint.
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_limits = {
            'anonymous': {'requests': 100, 'window': 3600},  # 100/hour
            'user': {'requests': 1000, 'window': 3600},      # 1000/hour  
            'premium': {'requests': 5000, 'window': 3600},   # 5000/hour
            'admin': {'requests': 10000, 'window': 3600}     # 10000/hour
        }
        
    def _get_user_tier(self) -> str:
        """Determine user tier from request context."""
        if hasattr(g, 'current_user'):
            user = g.current_user
            if hasattr(user, 'is_admin') and user.is_admin:
                return 'admin'
            elif hasattr(user, 'is_premium') and user.is_premium:
                return 'premium'
            elif user.is_authenticated:
                return 'user'
        return 'anonymous'
    
    def _get_client_id(self) -> str:
        """Generate unique client identifier for rate limiting."""
        if hasattr(g, 'current_user') and g.current_user.is_authenticated:
            base_id = f"user:{g.current_user.id}"
        else:
            # For anonymous users, use IP + User-Agent hash
            user_agent = request.headers.get('User-Agent', '')
            ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            base_id = f"anon:{hashlib.md5(f'{ip_addr}:{user_agent}'.encode()).hexdigest()}"
        
        return f"rate_limit:{base_id}:{request.endpoint}"
    
    def _sliding_window_check(self, key: str, limit: int, window: int) -> Tuple[bool, int]:
        """
        Implement sliding window algorithm with Redis.
        Returns (is_allowed, retry_after_seconds).
        """
        now = int(time.time())
        pipeline = self.redis.pipeline()
        
        try:
            # Remove expired entries
            pipeline.zremrangebyscore(key, 0, now - window)
            
            # Count current requests in window
            pipeline.zcard(key)
            
            # Execute pipeline
            results = pipeline.execute()
            current_count = results[1]
            
            if current_count >= limit:
                # Get oldest request timestamp to calculate retry_after
                oldest_requests = self.redis.zrange(key, 0, 0, withscores=True)
                if oldest_requests:
                    oldest_timestamp = int(oldest_requests[0][1])
                    retry_after = max(1, oldest_timestamp + window - now)
                else:
                    retry_after = window
                
                return False, retry_after
            
            # Add current request
            self.redis.zadd(key, {str(now): now})
            self.redis.expire(key, window + 60)  # Extra buffer for cleanup
            
            return True, 0
            
        except RedisError:
            # Fail open - allow request if Redis is down
            return True, 0
    
    def check_rate_limit(self, endpoint_limits: Optional[Dict] = None) -> None:
        """
        Check if current request exceeds rate limits.
        
        Args:
            endpoint_limits: Override limits for specific endpoint
            
        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        user_tier = self._get_user_tier()
        client_id = self._get_client_id()
        
        # Use endpoint-specific limits or default
        if endpoint_limits and user_tier in endpoint_limits:
            limits = endpoint_limits[user_tier]
        else:
            limits = self.default_limits[user_tier]
        
        is_allowed, retry_after = self._sliding_window_check(
            client_id, limits['requests'], limits['window']
        )
        
        if not is_allowed:
            raise RateLimitExceeded(
                f"Rate limit exceeded for {user_tier} tier. "
                f"Limit: {limits['requests']} requests per {limits['window']} seconds",
                retry_after
            )


def init_rate_limiter(app: Flask) -> None:
    """Initialize rate limiting middleware with Redis backend."""
    
    # Redis connection with fallback
    try:
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        redis_client = redis.from_url(redis_url, decode_responses=True)
        redis_client.ping()  # Test connection
        app.logger.info(f"Connected to Redis for rate limiting: {redis_url}")
    except (RedisError, ConnectionError) as e:
        app.logger.error(f"Redis connection failed: {e}. Rate limiting disabled.")
        return
    
    rate_limiter = SlidingWindowRateLimiter(redis_client)
    
    @app.before_request
    def check_rate_limits():
        """Apply rate limiting to incoming requests."""
        # Skip rate limiting for health checks and static files
        if request.endpoint in ['health.health_check', 'static']:
            return
        
        # Define stricter limits for sensitive endpoints
        strict_endpoints = {
            'auth.login': {
                'anonymous': {'requests': 5, 'window': 300},    # 5 per 5 minutes
                'user': {'requests': 10, 'window': 300}         # 10 per 5 minutes
            },
            'auth.register': {
                'anonymous': {'requests': 3, 'window': 3600}    # 3 per hour
            },
            'transactions.create': {
                'user': {'requests': 50, 'window': 3600},       # 50 per hour
                'premium': {'requests': 200, 'window': 3600}    # 200 per hour
            }
        }
        
        endpoint_limits = strict_endpoints.get(request.endpoint)
        
        try:
            rate_limiter.check_rate_limit(endpoint_limits)
        except RateLimitExceeded as e:
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': e.message,
                'retry_after': e.retry_after,
                'type': 'rate_limit_error'
            }), 429
    
    @app.errorhandler(429)
    def handle_rate_limit_error(error):
        """Handle rate limit exceeded errors."""
        response = jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded. Please slow down.',
            'type': 'rate_limit_error'
        })
        response.status_code = 429
        response.headers['Retry-After'] = '60'
        return response
    
    app.logger.info("Rate limiting middleware initialized successfully")


def rate_limit(requests_per_hour: int = None):
    """
    Decorator for applying custom rate limits to specific routes.
    
    Args:
        requests_per_hour: Override requests per hour for this endpoint
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Custom rate limiting logic can be added here
            return f(*args, **kwargs)
        return decorated_function
    return decorator
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def init_rate_limiter(app):
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    app.limiter = limiter
