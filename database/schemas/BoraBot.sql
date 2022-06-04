CREATE TABLE "Users" (
  "id" bigint PRIMARY KEY,
  "display_name" text,
  "created_at" timestamp
);

CREATE TABLE "DatefakeUsers" (
  "id" SERIAL PRIMARY KEY,
  "user_id" bigint,
  "guild_id" bigint,
  "created_at" timestamp
);

CREATE TABLE "DatefakePartners" (
  "id" SERIAL PRIMARY KEY,
  "datefake_id" int,
  "partner_id" bigint,
  "has_accepted" boolean,
  "created_at" timestamp
);

CREATE TABLE "Guilds" (
  "id" bigint PRIMARY KEY,
  "prefix" text,
  "created_at" timestamp
);

CREATE TABLE "UsersToGuilds" (
  "user_id" bigint,
  "guild_id" bigint,
  PRIMARY KEY ("user_id", "guild_id")
);

CREATE TABLE "MarryUsers" (
  "id" SERIAL,
  "user_id" bigint,
  "married_user" bigint,
  "created_at" timestamp,
  PRIMARY KEY ("id", "user_id")
);

ALTER TABLE "DatefakeUsers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "DatefakeUsers" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "DatefakePartners" ADD FOREIGN KEY ("datefake_id") REFERENCES "DatefakeUsers" ("id");

ALTER TABLE "DatefakePartners" ADD FOREIGN KEY ("partner_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UsersToGuilds" ADD FOREIGN KEY ("guild_id") REFERENCES "Guilds" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "MarryUsers" ADD FOREIGN KEY ("married_user") REFERENCES "Users" ("id");
