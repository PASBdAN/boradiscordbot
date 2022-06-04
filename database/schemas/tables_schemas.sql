CREATE TABLE IF NOT EXISTS "Users"(
  "id" bigint PRIMARY KEY,
  "display_name" text,
  "roll_count" INT DEFAULT 0,
  "roll_timestamp" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "DatefakeUsers" (
  -- "id" SERIAL PRIMARY KEY,
  "user_id" bigint PRIMARY KEY,
  "guild_id" bigint,
  "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "DatefakePartners" (
  "id" SERIAL PRIMARY KEY,
  "datefake_id" bigint,
  "partner_id" bigint,
  "has_accepted" boolean,
  "has_refused" boolean,
  "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Guilds" (
  "id" bigint PRIMARY KEY,
  "prefix" text,
  "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "UsersToGuilds" (
  "user_id" bigint,
  "guild_id" bigint,
  PRIMARY KEY ("user_id", "guild_id")
);

CREATE TABLE IF NOT EXISTS "MarryUsers" (
  "id" SERIAL,
  "user_id" bigint,
  "married_user" bigint,
  "created_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id", "user_id")
);

ALTER TABLE "DatefakeUsers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "DatefakeUsers" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "DatefakePartners" ADD FOREIGN KEY ("datefake_id") REFERENCES "DatefakeUsers" ("user_id");

ALTER TABLE "DatefakePartners" ADD FOREIGN KEY ("partner_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("married_user") REFERENCES "Users" ("id");


-- ADDING NEW COLUMNS:

-- ALTER TABLE "Users" ADD COLUMN IF NOT EXISTS "roll_count" INT DEFAULT 0;
-- ALTER TABLE "Users" ADD COLUMN IF NOT EXISTS "roll_timestamp" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
COMMIT;
