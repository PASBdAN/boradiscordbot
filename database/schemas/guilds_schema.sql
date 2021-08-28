CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild TEXT,
    guildId INTEGER,
    channels JSON,
    textChannels JSON,
    channelsCategory JSON,
    members JSON,
    membersCount INTEGER,
    roles JSON,
);