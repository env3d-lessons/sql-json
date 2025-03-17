-- Drop the users table if it exists
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL
);

-- Insert original data (adjust as needed)
INSERT INTO users (data) VALUES 
('{"username": "alice", "posts": ["Hello world!", "SQLite is great!", "Storing Python dicts as text!"]}'),
('{"username": "bob", "posts": ["My first post", "Learning SQL today"]}'),
('{"username": "charlie", "posts": ["Just joined!", "Excited to be here!", "Exploring databases", "This is fun!"]}');
