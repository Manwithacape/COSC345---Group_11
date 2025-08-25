-- Create a test user if not exists
INSERT INTO users (user_id, name, preferences, created_at)
SELECT 1, 'Test User', '{}', NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE user_id = 1
);