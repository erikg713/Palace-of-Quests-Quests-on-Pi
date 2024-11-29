CREATE VIEW leaderboard AS
SELECT 
    u.username,
    ps.level,
    ps.total_xp,
    ps.coins
FROM player_stats ps
JOIN users u ON ps.user_id = u.id
ORDER BY ps.total_xp DESC, ps.level DESC
LIMIT 50;
