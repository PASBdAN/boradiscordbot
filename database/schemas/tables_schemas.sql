CREATE TABLE IF NOT EXISTS "Users" (
  "id" bigint PRIMARY KEY,
  "name" text,
  "nickname" text,
  "created_at" timestamp
);

CREATE TABLE IF NOT EXISTS "Datefake" (
  "id" SERIAL PRIMARY KEY,
  "user_id" bigint,
  "partner_id" bigint,
  "guild_id" bigint,
  "allow_invite" boolean,
  "created_at" timestamp
);

CREATE TABLE IF NOT EXISTS "Guilds" (
  "id" bigint PRIMARY KEY,
  "prefix" text,
  "created_at" timestamp
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
  "created_at" timestamp,
  PRIMARY KEY ("id", "user_id")
);

ALTER TABLE "Datefake" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Datefake" ADD FOREIGN KEY ("partner_id") REFERENCES "Users" ("id");

ALTER TABLE "Datefake" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("married_user") REFERENCES "Users" ("id");
