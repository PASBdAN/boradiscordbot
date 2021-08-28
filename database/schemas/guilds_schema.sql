CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild TEXT,
    guild_id BIGINT UNIQUE,
    prefix TEXT,
    channels JSON,
    text_channels JSON,
    channels_category JSON,
    members JSON,
    members_count INTEGER,
    roles JSON
);