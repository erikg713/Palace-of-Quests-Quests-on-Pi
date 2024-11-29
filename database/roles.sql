CREATE ROLE gameuser LOGIN PASSWORD 'your_secure_password';
GRANT CONNECT ON DATABASE piquest_db TO gameuser;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO gameuser;

-- Create gameuser role with login
CREATE ROLE gameuser LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE piquest_db TO gameuser;

-- Grant role access only to necessary tables
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO gameuser;

CREATE ROLE gameuser LOGIN PASSWORD 'your_secure_password';
GRANT CONNECT ON DATABASE palaceofquests_db TO gameuser;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO gameuser;
