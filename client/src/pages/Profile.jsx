import React, { useEffect, useState, useCallback } from 'react';
import { Avatar, Spin, Card, Typography, List, message } from 'antd';
import { UserOutlined, TrophyOutlined, RocketOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch user profile data
  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true);
      // Replace with your API endpoint
      const { data } = await axios.get('/api/user/profile');
      setProfile(data.profile);
      setAchievements(data.achievements || []);
      setQuests(data.quests || []);
    } catch (err) {
      message.error('Failed to load profile.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', marginTop: 80 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div style={{ textAlign: 'center', marginTop: 80 }}>
        <Text type="danger">Profile not found.</Text>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 900, margin: '32px auto', padding: 16 }}>
      <Card
        bordered={false}
        style={{ marginBottom: 24, background: '#181c24' }}
        bodyStyle={{ display: 'flex', alignItems: 'center', gap: 32 }}
      >
        <Avatar
          size={96}
          icon={<UserOutlined />}
          src={profile.avatarUrl}
          alt="avatar"
          style={{ backgroundColor: '#4b6cb7' }}
        />
        <div>
          <Title level={2} style={{ color: '#fff', margin: 0 }}>
            {profile.username || 'Adventurer'}
          </Title>
          <Text style={{ color: '#bfc9df' }}>
            Level {profile.level || 1} &middot; XP: {profile.xp || 0}
          </Text>
          <div style={{ marginTop: 8 }}>
            <Text type="secondary">{profile.bio || 'No bio provided.'}</Text>
          </div>
        </div>
      </Card>

      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
        <Card
          title={<span><TrophyOutlined /> Achievements</span>}
          style={{ flex: 1, minWidth: 260, background: '#222738' }}
          bodyStyle={{ padding: 0 }}
        >
          <List
            dataSource={achievements}
            locale={{ emptyText: 'No achievements yet.' }}
            renderItem={item => (
              <List.Item style={{ padding: '12px 24px' }}>
                <List.Item.Meta
                  avatar={<TrophyOutlined style={{ color: '#ffd700' }} />}
                  title={item.title}
                  description={item.description}
                />
              </List.Item>
            )}
          />
        </Card>
        <Card
          title={<span><RocketOutlined /> Active Quests</span>}
          style={{ flex: 2, minWidth: 320, background: '#222738' }}
          bodyStyle={{ padding: 0 }}
        >
          <List
            dataSource={quests}
            locale={{ emptyText: 'No active quests.' }}
            renderItem={quest => (
              <List.Item style={{ padding: '12px 24px' }}>
                <List.Item.Meta
                  title={
                    <span style={{ fontWeight: 500 }}>{quest.name}</span>
                  }
                  description={quest.summary}
                />
                <Text type="success">{quest.progress}%</Text>
              </List.Item>
            )}
          />
        </Card>
      </div>
    </div>
  );
};

export default Profile;
