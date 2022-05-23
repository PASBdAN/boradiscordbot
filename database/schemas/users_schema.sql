CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    name TEXT,
    nickname TEXT,
    datefake BOOLEAN,
    allow_invite BOOLEAN,
    partner_id BIGINT,
    datefake_join_date DATE,
    datefake_leave_date DATE
);