CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    user_id BIGINT UNIQUE,
    is_bot INTEGER,
    nickname TEXT,
    roles JSON
);