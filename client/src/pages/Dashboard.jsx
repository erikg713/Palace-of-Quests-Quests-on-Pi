/**
 * Enhanced Quest Dashboard with Professional UX/UI
 * Features real-time updates, performance optimization, and accessibility
 * 
 * @author Erik G. - Palace of Quests Development Team
 * @version 2.1.0
 * @since 2025-06-05
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AnimatePresence, motion } from 'framer-motion';
import { 
    Trophy, 
    Target, 
    TrendingUp, 
    Star, 
    Clock, 
    Award,
    Users,
    Coins,
    ChevronRight,
    Play,
    Pause,
    RefreshCw
} from 'lucide-react';

import QuestCard from '../components/QuestCard';
import ProgressRing from '../components/ProgressRing';
import StatCard from '../components/StatCard';
import NotificationToast from '../components/NotificationToast';
import LoadingSpinner from '../components/LoadingSpinner';

import { fetchUserQuests, updateQuestProgress } from '../redux/slices/questsSlice';
import { fetchUserProfile } from '../redux/slices/userSlice';
import { formatPiAmount, formatTimeAgo, calculateQuestReward } from '../utils/formatters';
import piNetworkService from '../services/piNetworkService';

import './Dashboard.css';

const REFRESH_INTERVAL = 30000; // 30 seconds
const ANIMATION_DURATION = 0.3;

const Dashboard = () => {
    // Redux state management
    const dispatch = useDispatch();
    const { 
        activeQuests, 
        completedQuests, 
        availableQuests, 
        isLoading: questsLoading,
        error: questsError 
    } = useSelector(state => state.quests);
    
    const { 
        profile, 
        isLoading: profileLoading, 
        error: profileError 
    } = useSelector(state => state.user);

    // Local component state
    const [selectedQuestCategory, setSelectedQuestCategory] = useState('all');
    const [dashboardMetrics, setDashboardMetrics] = useState({
        totalXp: 0,
        piEarned: 0,
        questsCompleted: 0,
        currentStreak: 0
    });
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [lastActivity, setLastActivity] = useState(new Date());

    // Refs for performance optimization
    const refreshIntervalRef = useRef(null);
    const notificationTimeoutRef = useRef(null);

    /**
     * Fetch initial dashboard data with error handling
     */
    const initializeDashboard = useCallback(async () => {
        try {
            setIsRefreshing(true);
            
            // Parallel data fetching for better performance
            const [questsResult, profileResult] = await Promise.allSettled([
                dispatch(fetchUserQuests()).unwrap(),
                dispatch(fetchUserProfile()).unwrap()
            ]);

            // Handle any failed requests gracefully
            if (questsResult.status === 'rejected') {
                console.warn('Failed to fetch quests:', questsResult.reason);
                addNotification('Unable to load quests. Please try refreshing.', 'warning');
            }

            if (profileResult.status === 'rejected') {
                console.warn('Failed to fetch profile:', profileResult.reason);
                addNotification('Profile data unavailable.', 'warning');
            }

            setLastActivity(new Date());
            
        } catch (error) {
            console.error('Dashboard initialization failed:', error);
            addNotification('Failed to load dashboard. Please refresh the page.', 'error');
        } finally {
            setIsRefreshing(false);
        }
    }, [dispatch]);

    /**
     * Calculate dashboard metrics from quest data
     */
    const calculateDashboardMetrics = useMemo(() => {
        if (!activeQuests && !completedQuests) return dashboardMetrics;

        const allQuests = [...(activeQuests || []), ...(completedQuests || [])];
        
        const metrics = {
            totalXp: allQuests.reduce((sum, quest) => sum + (quest.xpRewarded || 0), 0),
            piEarned: allQuests.reduce((sum, quest) => sum + (quest.piRewarded || 0), 0),
            questsCompleted: completedQuests?.length || 0,
            currentStreak: profile?.questStreak || 0,
            avgCompletionTime: calculateAverageCompletionTime(completedQuests || []),
            weeklyProgress: calculateWeeklyProgress(completedQuests || [])
        };

        return metrics;
    }, [activeQuests, completedQuests, profile]);

    /**
     * Filter quests by category with performance optimization
     */
    const filteredActiveQuests = useMemo(() => {
        if (!activeQuests) return [];
        
        if (selectedQuestCategory === 'all') return activeQuests;
        
        return activeQuests.filter(quest => 
            quest.category?.toLowerCase() === selectedQuestCategory.toLowerCase()
        );
    }, [activeQuests, selectedQuestCategory]);

    /**
     * Handle quest action with optimistic updates
     */
    const handleQuestAction = useCallback(async (questId, action, additionalData = {}) => {
        try {
            const quest = activeQuests?.find(q => q.id === questId);
            if (!quest) {
                throw new Error('Quest not found');
            }

            switch (action) {
                case 'start':
                    await startQuest(questId);
                    break;
                case 'update_progress':
                    await updateProgressOptimistically(questId, additionalData.progress);
                    break;
                case 'complete':
                    await completeQuest(questId);
                    break;
                default:
                    throw new Error(`Unknown quest action: ${action}`);
            }

            addNotification(`Quest ${action} successful!`, 'success');
            
        } catch (error) {
            console.error(`Quest ${action} failed:`, error);
            addNotification(`Failed to ${action} quest. Please try again.`, 'error');
        }
    }, [activeQuests]);

    /**
     * Start a quest with Pi Network integration
     */
    const startQuest = useCallback(async (questId) => {
        const quest = availableQuests?.find(q => q.id === questId);
        if (!quest) return;

        // Check if quest requires payment
        if (quest.entranceFee > 0) {
            try {
                const paymentResult = await piNetworkService.createPayment({
                    amount: quest.entranceFee,
                    memo: `Palace of Quests - ${quest.title}`,
                    userId: profile?.id,
                    itemId: questId,
                    transactionType: 'quest_entrance'
                });

                if (paymentResult.status === 'initiated') {
                    addNotification('Payment initiated. Complete payment to start quest.', 'info');
                }
            } catch (error) {
                throw new Error(`Payment failed: ${error.message}`);
            }
        }

        // Start quest via API
        await dispatch(updateQuestProgress({ 
            questId, 
            action: 'start',
            timestamp: new Date().toISOString()
        })).unwrap();
        
    }, [availableQuests, profile, dispatch]);

    /**
     * Update quest progress with optimistic UI updates
     */
    const updateProgressOptimistically = useCallback(async (questId, progressData) => {
        // Optimistic update
        const optimisticUpdate = {
            questId,
            progress: progressData.progress,
            timestamp: new Date().toISOString()
        };

        // Update UI immediately
        dispatch(updateQuestProgress(optimisticUpdate));

        // Send to backend
        try {
            await fetch('/api/quests/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${profile?.accessToken}`
                },
                body: JSON.stringify(optimisticUpdate)
            });
        } catch (error) {
            // Revert optimistic update on failure
            console.error('Failed to sync progress:', error);
            throw error;
        }
    }, [dispatch, profile]);

    /**
     * Complete quest and handle rewards
     */
    const completeQuest = useCallback(async (questId) => {
        const quest = activeQuests?.find(q => q.id === questId);
        if (!quest) return;

        const completionData = {
            questId,
            completedAt: new Date().toISOString(),
            rewards: calculateQuestReward(quest, profile?.level || 1)
        };

        await dispatch(updateQuestProgress({
            ...completionData,
            action: 'complete'
        })).unwrap();

        // Show celebration animation/notification
        addNotification(
            `🎉 Quest completed! Earned ${completionData.rewards.xp} XP and ${formatPiAmount(completionData.rewards.pi)}`,
            'success',
            5000
        );
    }, [activeQuests, dispatch, profile]);

    /**
     * Add notification with auto-dismiss
     */
    const addNotification = useCallback((message, type = 'info', duration = 3000) => {
        const id = Date.now() + Math.random();
        const notification = { id, message, type, timestamp: new Date() };
        
        setNotifications(prev => [...prev, notification]);

        // Auto-dismiss notification
        setTimeout(() => {
            setNotifications(prev => prev.filter(n => n.id !== id));
        }, duration);
    }, []);

    /**
     * Manual refresh handler
     */
    const handleManualRefresh = useCallback(async () => {
        await initializeDashboard();
        addNotification('Dashboard refreshed successfully!', 'success');
    }, [initializeDashboard]);

    /**
     * Calculate average completion time for analytics
     */
    const calculateAverageCompletionTime = useCallback((quests) => {
        if (!quests.length) return 0;
        
        const completionTimes = quests
            .filter(q => q.startedAt && q.completedAt)
            .map(q => new Date(q.completedAt) - new Date(q.startedAt));
        
        return completionTimes.length > 0 
            ? completionTimes.reduce((sum, time) => sum + time, 0) / completionTimes.length
            : 0;
    }, []);

    /**
     * Calculate weekly progress for trends
     */
    const calculateWeeklyProgress = useCallback((quests) => {
        const now = new Date();
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        
        return quests.filter(q => 
            q.completedAt && new Date(q.completedAt) >= weekAgo
        ).length;
    }, []);

    // Initialize dashboard on mount
    useEffect(() => {
        initializeDashboard();
        
        // Set up auto-refresh interval
        refreshIntervalRef.current = setInterval(initializeDashboard, REFRESH_INTERVAL);
        
        return () => {
            if (refreshIntervalRef.current) {
                clearInterval(refreshIntervalRef.current);
            }
        };
    }, [initializeDashboard]);

    // Update metrics when quest data changes
    useEffect(() => {
        setDashboardMetrics(calculateDashboardMetrics);
    }, [calculateDashboardMetrics]);

    // Loading state
    if (questsLoading || profileLoading) {
        return (
            <div className="dashboard-loading">
                <LoadingSpinner size="large" message="Loading your palace..." />
            </div>
        );
    }

    // Error state
    if (questsError || profileError) {
        return (
            <div className="dashboard-error">
                <div className="error-content">
                    <h2>Oops! Something went wrong</h2>
                    <p>We couldn't load your dashboard. Please try refreshing the page.</p>
                    <button 
                        className="refresh-button" 
                        onClick={handleManualRefresh}
                        disabled={isRefreshing}
                    >
                        <RefreshCw className={isRefreshing ? 'spinning' : ''} />
                        Refresh Dashboard
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            {/* Notification System */}
            <AnimatePresence>
                {notifications.map(notification => (
                    <NotificationToast
                        key={notification.id}
                        notification={notification}
                        onDismiss={(id) => setNotifications(prev => prev.filter(n => n.id !== id))}
                    />
                ))}
            </AnimatePresence>

            {/* Dashboard Header */}
            <motion.header 
                className="dashboard-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: ANIMATION_DURATION }}
            >
                <div className="header-content">
                    <div className="welcome-section">
                        <h1>Welcome back, {profile?.displayName || 'Adventurer'}!</h1>
                        <p className="welcome-subtitle">
                            Ready to continue your quest? You have {filteredActiveQuests.length} active quest{filteredActiveQuests.length !== 1 ? 's' : ''}.
                        </p>
                    </div>
                    
                    <div className="header-actions">
                        <button 
                            className="refresh-btn"
                            onClick={handleManualRefresh}
                            disabled={isRefreshing}
                            title="Refresh dashboard"
                        >
                            <RefreshCw className={isRefreshing ? 'spinning' : ''} size={20} />
                        </button>
                        <div className="last-updated">
                            Last updated: {formatTimeAgo(lastActivity)}
                        </div>
                    </div>
                </div>
            </motion.header>

            {/* Stats Overview */}
            <motion.section 
                className="stats-overview"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: ANIMATION_DURATION, delay: 0.1 }}
            >
                <StatCard
                    icon={<Trophy />}
                    title="Total XP"
                    value={dashboardMetrics.totalXp.toLocaleString()}
                    change={`+${Math.round(dashboardMetrics.totalXp * 0.1)} this week`}
                    trend="up"
                    color="gold"
                />
                
                <StatCard
                    icon={<Coins />}
                    title="Pi Earned"
                    value={formatPiAmount(dashboardMetrics.piEarned)}
                    change={`${dashboardMetrics.weeklyProgress} quests this week`}
                    trend="up"
                    color="blue"
                />
                
                <StatCard
                    icon={<Target />}
                    title="Quests Completed"
                    value={dashboardMetrics.questsCompleted}
                    change={`${Math.round((dashboardMetrics.questsCompleted / (dashboardMetrics.questsCompleted + filteredActiveQuests.length)) * 100)}% completion rate`}
                    trend="stable"
                    color="green"
                />
                
                <StatCard
                    icon={<Star />}
                    title="Current Streak"
                    value={`${dashboardMetrics.currentStreak} days`}
                    change={dashboardMetrics.currentStreak > 0 ? "Keep it up!" : "Start your streak today!"}
                    trend={dashboardMetrics.currentStreak > 0 ? "up" : "neutral"}
                    color="purple"
                />
            </motion.section>

            {/* Quest Categories Filter */}
            <motion.section 
                className="quest-categories"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: ANIMATION_DURATION, delay: 0.2 }}
            >
                <div className="categories-header">
                    <h2>Active Quests</h2>
                    <div className="category-filters">
                        {['all', 'exploration', 'combat', 'social', 'economy'].map(category => (
                            <button
                                key={category}
                                className={`category-filter ${selectedQuestCategory === category ? 'active' : ''}`}
                                onClick={() => setSelectedQuestCategory(category)}
                            >
                                {category.charAt(0).toUpperCase() + category.slice(1)}
                            </button>
                        ))}
                    </div>
                </div>
            </motion.section>

            {/* Active Quests Grid */}
            <motion.section 
                className="active-quests-grid"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: ANIMATION_DURATION, delay: 0.3 }}
            >
                <AnimatePresence mode="wait">
                    {filteredActiveQuests.length > 0 ? (
                        <motion.div 
                            className="quests-grid"
                            layout
                        >
                            {filteredActiveQuests.map((quest, index) => (
                                <motion.div
                                    key={quest.id}
                                    layout
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    transition={{ 
                                        duration: ANIMATION_DURATION,
                                        delay: index * 0.1 
                                    }}
                                >
                                    <QuestCard
                                        quest={quest}
                                        onAction={handleQuestAction}
                                        userLevel={profile?.level || 1}
                                        showProgress={true}
                                        interactive={true}
                                    />
                                </motion.div>
                            ))}
                        </motion.div>
                    ) : (
                        <motion.div 
                            className="no-quests-message"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            <div className="empty-state">
                                <Target size={64} className="empty-icon" />
                                <h3>No active quests</h3>
                                <p>Start a new adventure from the quest marketplace!</p>
                                <button 
                                    className="cta-button"
                                    onClick={() => window.location.href = '/quests/marketplace'}
                                >
                                    Explore Quests <ChevronRight size={20} />
                                </button>
                            </div>
                        </motion.div>
         
