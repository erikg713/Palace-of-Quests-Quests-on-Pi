"""
Database utilities and helpers for Palace of Quests.
Includes connection management, query helpers, and transaction decorators.

Author: Senior Backend Team
Last Modified: 2025-06-04
"""

import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Dict, List, Optional, Callable, Union
from flask import current_app
from sqlalchemy import text, func
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
from app import db


class DatabaseManager:
    """Database connection and query management utilities."""
    
    @staticmethod
    def health_check() -> Dict[str, Any]:
        """
        Perform database health check with connection and query tests.
        
        Returns:
            Dictionary with health status and metrics
        """
        start_time = time.time()
        
        try:
            # Test basic connectivity
            result = db.session.execute(text('SELECT 1')).scalar()
            
            if result != 1:
                raise Exception("Database returned unexpected result")
            
            # Test transaction handling
            with db.session.begin():
                db.session.execute(text('SELECT COUNT(*) FROM information_schema.tables'))
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                'status': 'healthy',
                'response_time_ms': round(response_time, 2),
                'connection_pool': {
                    'size': db.engine.pool.size(),
                    'checked_in': db.engine.pool.checkedin(),
                    'checked_out': db.engine.pool.checkedout(),
                    'overflow': db.engine.pool.overflow(),
                }
            }
            
        except Exception as e:
            current_app.logger.error(f"Database health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'response_time_ms': (time.time() - start_time) * 1000
            }
    
    @staticmethod
    def get_table_stats() -> Dict[str, int]:
        """Get row counts for all main tables."""
        tables = ['users', 'quests', 'user_quests', 'transactions', 'marketplace_items']
        stats = {}
        
        for table in tables:
            try:
                count = db.session.execute(
                    text(f'SELECT COUNT(*) FROM {table}')
                ).scalar()
                stats[table] = count
            except SQLAlchemyError:
                stats[table] = -1  # Indicate error
        
        return stats
    
    @staticmethod
    @contextmanager
    def transaction():
        """
        Context manager for database transactions with automatic rollback.
        
        Usage:
            with DatabaseManager.transaction():
                # database operations
                pass
        """
        try:
            yield db.session
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()


def with_db_transaction(func: Callable) -> Callable:
    """
    Decorator that wraps function in database transaction.
    Automatically commits on success, rolls back on error.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception:
            db.session.rollback()
            raise
    return wrapper


def retry_db_operation(max_retries: int = 3, delay: float = 0.1):
    """
    Decorator to retry database operations on transient failures.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    last_exception = e
                    if attempt < max_retries:
                        current_app.logger.warning(
                            f"Database operation failed (attempt {attempt + 1}): {str(e)}"
                        )
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        continue
                    break
                except Exception:
                    # Don't retry non-transient errors
                    raise
            
            # All retries exhausted
            current_app.logger.error(f"Database operation failed after {max_retries} retries")
            raise last_exception
        
        return wrapper
    return decorator


class QueryBuilder:
    """Helper class for building complex database queries safely."""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = db.session.query(model_class)
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None
    
    def filter_by(self, **kwargs):
        """Add filter conditions to query."""
        for key, value in kwargs.items():
            if hasattr(self.model_class, key):
                self._filters.append(getattr(self.model_class, key) == value)
        return self
    
    def filter(self, condition):
        """Add raw filter condition."""
        self._filters.append(condition)
        return self
    
    def order_by(self, *columns):
        """Add ordering to query."""
        self._order_by.extend(columns)
        return self
    
    def limit(self, count: int):
        """Add limit to query."""
        self._limit = count
        return self
    
    def offset(self, count: int):
        """Add offset to query."""
        self._offset = count
        return self
    
    def paginate(self, page: int, per_page: int = 20):
        """Add pagination to query."""
        self._limit = per_page
        self._offset = (page - 1) * per_page
        return self
    
    def build(self):
        """Build and return the final query."""
        query = self.query
        
        # Apply filters
        for filter_condition in self._filters:
            query = query.filter(filter_condition)
        
        # Apply ordering
        if self._order_by:
            query = query.order_by(*self._order_by)
        
        # Apply pagination
        if self._offset:
            query = query.offset(self._offset)
        if self._limit:
            query = query.limit(self._limit)
        
        return query
    
    def count(self) -> int:
        """Get count of matching records."""
        query = db.session.query(func.count(self.model_class.id))
        for filter_condition in self._filters:
            query = query.filter(filter_condition)
        return query.scalar()
    
    def execute(self) -> List:
        """Execute query and return results."""
        return self.build().all()
    
    def first(self):
        """Execute query and return first result."""
        return self.build().first()


# Database initialization helpers
def init_database():
    """Initialize database with tables and indexes."""
    try:
        db.create_all()
        current_app.logger.info("Database tables created successfully")
        
        # Create indexes for performance
        create_performance_indexes()
        
    except Exception as e:
        current_app.logger.error(f"Database initialization failed: {str(e)}")
        raise


def create_performance_indexes():
    """Create database indexes for better query performance."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)", 
        "CREATE INDEX IF NOT EXISTS idx_quests_status ON quests(status)",
        "CREATE INDEX IF NOT EXISTS idx_user_quests_user_id ON user_quests(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_user_quests_quest_id ON user_quests(quest_id)",
        "CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at)",
    ]
    
    for index_sql in indexes:
        try:
            db.session.execute(text(index_sql))
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.warning(f"Failed to create index: {index_sql} - {str(e)}")
            db.session.rollback()
