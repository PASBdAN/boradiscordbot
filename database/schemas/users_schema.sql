CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    userId INTEGER UNIQUE,
    isBot INTEGER,
    nickname TEXT,
    roles JSON
);