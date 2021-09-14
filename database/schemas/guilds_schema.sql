CREATE TABLE IF NOT EXISTS guilds (
    --id INTEGER PRIMARY KEY AUTOINCREMENT,
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNIQUE,
    prefix TEXT
    --activity TEXT,
    --activity_timer INTEGER
);