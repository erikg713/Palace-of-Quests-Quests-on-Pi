"""
Quest management system with advanced features and optimizations.
Includes quest progression, reward distribution, and performance tracking.

Author: Erik G. - Palace of Quests Team
Last Updated: 2025-06-04
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal

from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.orm import joinedload, selectinload

from app.models.quest import Quest, QuestCategory, QuestDifficulty
from app.models.user_quest import UserQuest, QuestStatus
from app.models.user import User
from app.models.reward import Reward, RewardType
from app import db
from app.blueprints.quests import quests_bp
from app.utils.quest_engine import QuestEngine
from app.utils.caching import cache_result
from app.utils.pagination import paginate_query
from app.utils.permissions import require_permission

logger = logging.getLogger(__name__)

# Quest system constants
DAILY_QUEST_LIMIT = 10
WEEKLY_QUEST_LIMIT = 25
XP_MULTIPLIERS = {
    QuestDifficulty.EASY: Decimal('1.0'),
    QuestDifficulty.MEDIUM: Decimal('1.5'),
    QuestDifficulty.HARD: Decimal('2.0'),
    QuestDifficulty.EPIC: Decimal('3.0'),
    QuestDifficulty.LEGENDARY: Decimal('5.0')
}

class QuestManager:
    """Centralized quest management with business logic."""
    
    @staticmethod
    def get_available_quests(user: User, page: int = 1, 
                           category: Optional[str] = None,
                           difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Get quests available to user with filtering and pagination."""
        query = Quest.query.filter(
            Quest.is_active == True,
            Quest.min_level <= user.level,
            Quest.max_level >= user.level
        )
        
        # Filter by category if specified
        if category:
            query = query.filter(Quest.category == category)
        
        # Filter by difficulty if specified
        if difficulty:
            query = query.filter(Quest.difficulty == difficulty)
        
        # Exclude already completed quests
        completed_quest_ids = db.session.query(UserQuest.quest_id).filter(
            UserQuest.user_id == user.id,
            UserQuest.status == QuestStatus.COMPLETED
        ).subquery()
        
        query = query.filter(~Quest.id.in_(completed_quest_ids))
        
        # Apply ordering for better UX
        query = query.order_by(
            Quest.priority.desc(),
            Quest.xp_reward.desc(),
            Quest.created_at.desc()
        )
        
        return paginate_query(query, page, per_page=20)
    
    @staticmethod
    def start_quest(user: User, quest_id: int) -> Tuple[bool, str, Dict[str, Any]]:
        """Start a quest for a user with comprehensive validation."""
        try:
            quest = Quest.query.get(quest_id)
            if not quest:
                return False, "Quest not found", {}
            
            # Validation checks
            if not quest.is_active:
                return False, "This quest is no longer available", {}
            
            if user.level < quest.min_level:
                return False, f"You need to reach level {quest.min_level} to start this quest", {}
            
            if user.level > quest.max_level:
                return False, "You have outgrown this quest", {}
            
            # Check if user already has this quest
            existing_quest = UserQuest.query.filter_by(
                user_id=user.id,
                quest_id=quest_id
            ).first()
            
            if existing_quest:
                if existing_quest.status == QuestStatus.COMPLETED:
                    return False, "You have already completed this quest", {}
                elif existing_quest.status == QuestStatus.IN_PROGRESS:
                    return False, "You are already working on this quest", {}
            
            # Check daily/weekly limits
            today = datetime.utcnow().date()
            daily_count = UserQuest.query.filter(
                UserQuest.user_id == user.id,
                func.date(UserQuest.started_at) == today
            ).count()
            
            if daily_count >= DAILY_QUEST_LIMIT:
                return False, f"Daily quest limit reached ({DAILY_QUEST_LIMIT})", {}
            
            # Check prerequisites
            if quest.prerequisite_quests:
                completed_prerequisites = db.session.query(UserQuest.quest_id).filter(
                    UserQuest.user_id == user.id,
                    UserQuest.quest_id.in_(quest.prerequisite_quests),
                    UserQuest.status == QuestStatus.COMPLETED
                ).all()
                
                if len(completed_prerequisites) < len(quest.prerequisite_quests):
                    return False, "You must complete prerequisite quests first", {}
            
            # Create user quest record
            user_quest = UserQuest(
                user_id=user.id,
                quest_id=quest_id,
                status=QuestStatus.IN_PROGRESS,
                started_at=datetime.utcnow(),
                progress_data={
                    'objectives': {obj.id: 0 for obj in quest.objectives},
                    'started_level': user.level,
                    'initial_stats': {
                        'xp': user.xp,
                        'pi_balance': user.pi_balance
                    }
                }
            )
            
            db.session.add(user_quest)
            db.session.commit()
            
            logger.info(f"User {user.username} started quest {quest.title}")
            
            return True, "Quest started successfully!", {
                'quest': quest.to_dict(),
                'user_quest_id': user_quest.id,
                'objectives': [obj.to_dict() for obj in quest.objectives]
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to start quest {quest_id} for user {user.id}: {str(e)}")
            return False, "An error occurred while starting the quest", {}

@quests_bp.route('/available')
@login_required
@cache_result(timeout=300)  # Cache for 5 minutes
def get_available_quests():
    """Get available quests for the current user."""
    page = int(request.args.get('page', 1))
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    result = QuestManager.get_available_quests(
        current_user, page, category, difficulty
    )
    
    # Add user-specific context
    for quest in result['items']:
        quest_dict = quest.to_dict()
        quest_dict['can_start'] = current_user.level >= quest.min_level
        quest_dict['xp_multiplier'] = float(XP_MULTIPLIERS.get(quest.difficulty, 1.0))
        quest_dict['estimated_duration'] = quest.estimated_completion_time
        result['items'][result['items'].index(quest)] = quest_dict
    
    return jsonify({
        'success': True,
        'data': result,
        'user_context': {
            'level': current_user.level,
            'daily_quests_completed': current_user.daily_quests_completed_today(),
            'weekly_quests_completed': current_user.weekly_quests_completed(),
            'available_quest_slots': DAILY_QUEST_LIMIT - current_user.daily_quests_completed_today()
        }
    })

@quests_bp.route('/start', methods=['POST'])
@login_required
def start_quest():
    """Start a new quest for the current user."""
    data = request.get_json()
    quest_id = data.get('quest_id')
    
    if not quest_id:
        return jsonify({
            'success': False,
            'message': 'Quest ID is required'
        }), 400
    
    success, message, quest_data = QuestManager.start_quest(current_user, quest_id)
    
    status_code = 200 if success else 400
    return jsonify({
        'success': success,
        'message': message,
        'data': quest_data
    }), status_code

@quests_bp.route('/progress/<int:user_quest_id>', methods=['POST'])
@login_required
def update_quest_progress(user_quest_id: int):
    """Update progress on a user's active quest."""
    try:
        user_quest = UserQuest.query.filter_by(
            id=user_quest_id,
            user_id=current_user.id,
            status=QuestStatus.IN_PROGRESS
        ).first()
        
        if not user_quest:
            return jsonify({
                'success': False,
                'message': 'Active quest not found'
            }), 404
        
        data = request.get_json()
        objective_id = data.get('objective_id')
        progress_value = data.get('progress', 0)
        
        if not objective_id:
            return jsonify({
                'success': False,
                'message': 'Objective ID is required'
            }), 400
        
        # Update progress using quest engine
        quest_engine = QuestEngine()
        result = quest_engine.update_objective_progress(
            user_quest, objective_id, progress_value
        )
        
        if result['quest_completed']:
            # Handle quest completion
            rewards_granted = quest_engine.complete_quest(user_quest)
            
            return jsonify({
                'success': True,
                'message': 'Quest completed! Congratulations!',
                'data': {
                    'quest_completed': True,
                    'rewards': rewards_granted,
                    'total_progress': result['total_progress'],
                    'xp_gained': rewards_granted.get('xp', 0),
                    'pi_earned': rewards_granted.get('pi_coins', 0)
                }
            })
        
        return jsonify({
            'success': True,
            'message': 'Progress updated successfully',
            'data': {
                'quest_completed': False,
                'total_progress': result['total_progress'],
                'objectives_progress': result['objectives_progress']
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to update quest progress: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating progress'
        }), 500

@quests_bp.route('/my-quests')
@login_required  
def get_user_quests():
    """Get all quests for the current user with detailed progress."""
    status_filter = request.args.get('status', 'all')
    page = int(request.args.get('page', 1))
    
    query = UserQuest.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Use eager loading for better performance
    query = query.options(
        joinedload(UserQuest.quest).joinedload(Quest.objectives),
        joinedload(UserQuest.quest).joinedload(Quest.rewards)
    ).order_by(desc(UserQuest.started_at))
    
    result = paginate_query(query, page, per_page=15)
    
    # Format response with rich data
    formatted_quests = []
    for user_quest in result['items']:
        quest_data = user_quest.quest.to_dict()
        quest_data.update({
            'user_quest_id': user_quest.id,
            'status': user_quest.status.value,
            'progress_percentage': user_quest.calculate_progress_percentage(),
            'started_at': user_quest.started_at.isoformat(),
            'completed_at': user_quest.completed_at.isoformat() if user_quest.completed_at else None,
            'time_spent': user_quest.calculate_time_spent(),
            'objectives_progress': user_quest.get_objectives_progress()
        })
        formatted_quests.append(quest_data)
    
    return jsonify({
        'success': True,
        'data': {
            'quests': formatted_quests,
            'pagination': result['pagination'],
            'summary': {
                'total_quests': current_user.total_quests_started(),
                'completed_quests': current_user.completed_quests_count(),
                'in_progress_quests': current_user.active_quests_count(),
                'completion_rate': current_user.quest_completion_rate()
            }
        }
    })

@quests_bp.route('/leaderboard')
@cache_result(timeout=600)  # Cache for 10 minutes
def quest_leaderboard():
    """Get quest completion leaderboard."""
    period = request.args.get('period', 'weekly')  # daily, weekly, monthly, all-time
    limit = min(int(request.args.get('limit', 50)), 100)
    
    # Calculate date range based on period
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'weekly':
        start_date = now - timedelta(days=7)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = datetime.min
    
    # Query for leaderboard
    leaderboard_query = db.session.query(
        User.id,
        User.username,
        User.display_name,
        User.level,
        func.count(UserQuest.id).label('quests_completed'),
        func.sum(Quest.xp_reward).label('total_xp_earned'),
        func.sum(Quest.pi_reward).label('total_pi_earned')
    ).join(
        UserQuest, User.id == UserQuest.user_id
    ).join(
        Quest, UserQuest.quest_id == Quest.id
    ).filter(
        UserQuest.status == QuestStatus.COMPLETED,
        UserQuest.completed_at >= start_date
    ).group_by(
        User.id, User.username, User.display_name, User.level
    ).order_by(
        desc('quests_completed'),
        desc('total_xp_earned')
    ).limit(limit).all()
    
    leaderboard_data = []
    for rank, entry in enumerate(leaderboard_query, 1):
        leaderboard_data.append({
            'rank': rank,
            'user_id': entry.id,
            'username': entry.username,
            'display_name': entry.display_name,
            'level': entry.level,
            'quests_completed': entry.quests_completed,
            'total_xp_earned': float(entry.total_xp_earned or 0),
            'total_pi_earned': float(entry.total_pi_earned or 0)
        })
    
    return jsonify({
        'success': True,
        'data': {
            'leaderboard': leaderboard_data,
            'period': period,
            'updated_at': now.isoformat()
        }
    })

@quests_bp.route('/categories')
@cache_result(timeout=3600)  # Cache for 1 hour
def get_quest_categories():
    """Get all available quest categories with statistics."""
    categories = db.session.query(
        QuestCategory.name,
        QuestCategory.description,
        QuestCategory.icon,
        func.count(Quest.id).label('quest_count'),
        func.avg(Quest.xp_reward).label('avg_xp_reward')
    ).join(
        Quest, QuestCategory.name == Quest.category
    ).filter(
        Quest.is_active == True
    ).group_by(
        QuestCategory.name, QuestCategory.description, QuestCategory.icon
    ).all()
    
    category_data = []
    for category in categories:
        category_data.append({
            'name': category.name,
            'description': category.description,
            'icon': category.icon,
            'quest_count': category.quest_count,
            'avg_xp_reward': float(category.avg_xp_reward or 0)
        })
    
    return jsonify({
        'success': True,
        'data': {'categories': category_data}
    })
