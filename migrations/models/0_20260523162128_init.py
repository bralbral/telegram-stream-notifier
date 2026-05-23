from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channel_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "type" VARCHAR(15) NOT NULL UNIQUE DEFAULT 'YOUTUBE'
);
COMMENT ON COLUMN "channel_types"."type" IS 'YOUTUBE: YOUTUBE\nTWITCH: TWITCH\nKICK: KICK';
CREATE TABLE IF NOT EXISTS "user_roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "role" VARCHAR(15) NOT NULL UNIQUE DEFAULT 'USER'
);
COMMENT ON COLUMN "user_roles"."role" IS 'USER: USER\nADMIN: ADMIN';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL UNIQUE,
    "username" VARCHAR(255),
    "firstname" VARCHAR(255),
    "lastname" VARCHAR(255),
    "role_id" INT NOT NULL REFERENCES "user_roles" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_users_user_id_a795d9" ON "users" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
CREATE INDEX IF NOT EXISTS "idx_users_firstna_c7b30e" ON "users" ("firstname");
CREATE INDEX IF NOT EXISTS "idx_users_lastnam_3a2577" ON "users" ("lastname");
CREATE TABLE IF NOT EXISTS "channels" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "url" VARCHAR(255) NOT NULL UNIQUE,
    "label" VARCHAR(255) NOT NULL,
    "enabled" BOOL NOT NULL,
    "creator_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "type_id" INT NOT NULL REFERENCES "channel_types" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_channels_url_b5ced0" ON "channels" ("url");
CREATE INDEX IF NOT EXISTS "idx_channels_label_9305e7" ON "channels" ("label");
CREATE INDEX IF NOT EXISTS "idx_channels_enabled_927807" ON "channels" ("enabled");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "channel_subscribers" (
    "channels_id" INT NOT NULL REFERENCES "channels" ("id") ON DELETE CASCADE,
    "usermodel_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_channel_sub_channel_c7ddef" ON "channel_subscribers" ("channels_id", "usermodel_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztWllz4jgQ/isuP2Wr2KnAZo7iDQipsAkwBWaPmUy5hC3AFSMxsrwZaor/vpJ8y0cwMQ"
    "lM+YWjW23UX+v4upuf6hqb0Hbe9VYAIWgP+Te1rfxUEVhD9iFT31BUsNlEWi6gYG4LA8Mb"
    "KYRg7lACDMrkC2A7kIlM6BjE2lALIyZFrm1zITbYQAstI5GLrO8u1CleQrqChCm+fmNiC5"
    "nwB3SCr5tHfWFB20xM2TL5bwu5TrcbIRsgeiMG8l+b6wa23TWKBm+2dIVRONpClEuXEEEC"
    "KOSPp8Tl0+ez8z0NPPJmGg3xphizMeECuDaNubsnBgZGHD82G0c4uOS/8nurefXx6tMfH6"
    "4+sSFiJqHk485zL/LdMxQIjDR1J/SAAm+EgDHCzSCQO6sDmsbvmmmotYbZICYtJTBN3/Rd"
    "8EGGNgCyCNtAEIEbLaiK0GU+mGNkb/3AFUCpDYb9qdYZfuaerB3nuy0g6mh9rmkJ6VaSXn"
    "z4jcsx2w7ePgkfovw90G4V/lX5Mh71BYLYoUsifjEap31R+ZyAS7GO8JMOzNgaC6QBMGxk"
    "FFh3Yx4Y2KRlHdg3Daw/+VhciZ0OKDupSU4wveFSFBlUh8Tt6IfdGvzQbYiWdMVPuPfvC8"
    "L2V2fSu+1MLtgoKRYjX9XydLsEfMw3WArA0KAaCNNL//wwhIh7l3HhdjG2IUDZQMasJCjn"
    "zOwksSyArjse3ycOjO5AkyCcDbv9yUVTIMsGWRTGr2TpCsZEL0VhkkbPU5kMPH2wXvNUro"
    "TMRMhxfTnYYhYHYfYWV1kFoHHavHjMJ4CYpDG8wQRaS3QHtwLKAZsUQAbMgM5PF2YOJGGu"
    "cHJrbxcshUAazYKApzCjkDYW85I5BL2tO+1rymh2f6+mFmEF6PnJlsak+4L4BotxXxRj+y"
    "wBYa8z7XWu+6pYkXNgPD4BYuqJpck1uIUlSTg2rVq31pkr23Hn3Mc5JE46PkOAthrmr0dY"
    "3a9OnArCIqavS5l9whkCbcH3U7iZejyvX2AiAvAIt4JYskd4z/bCHAbI1wemvpquCHaXq5"
    "hGl+KTuU6YXE+BLRbPGiCwFDIOya6Rv5HyKxuJzfZsdcM/WRt1iaMucdSZcF3iqAN7pBJH"
    "NqPiKXofuevUfZ0i+K9Z8FD/Hc+0WVegkAxkoGkr/ocHpDHkerdtxXt/QHeD3l1b4a/qfi"
    "FP5PbNfVL7Zn5m3xSJfSo1yGdmsSM1zguSJQDf8uZuwmkFh+I5ynuGdHf3QpJaSGAicpbB"
    "XBLMLZ+ycHZWU5WaqtQ3Wk1V6sAesRvDztlyFciYRTUVyPM485KQic+ZDC8ftMDmIGb3fL"
    "3x/NowC4s4tCySCaMayrArWB7JuE0NpA8kwXbJjkzMou7IhBhW1I6ZsEedYXrVkLoJsTVS"
    "tpuQ5tZvkrueTr/rpalrRn+lCNPSfZaXFgVOrdUi+5PbbSFZXRapiyI3WeQmTEVdlnCdFN"
    "YoosMlp06ROH2KaxU63+J1weJEyXtdsPjF89q6YPGLBjZVsMgml/v1VgLbV+utzKb9SUZj"
    "hYvbCn99QJ3r4WDUVsTbmTVRwhr94Sz0RX9KOV8OWkhNOpBYxiqLk/iaQjICojE1ETkjIv"
    "If20v+Vtm3gBMzOdZ/uyu/l45fweFbowSI/vDzBLB5ebnP6X95mX/8c530d26MKEQZtOnP"
    "6XiUw4UjEwnIGWIOfjUtgzYU23Lot9OEtQBF7nWCGgXgXQw7/8i49u7HXZnz8Ad0y92x1V"
    "8vu/8BVCJwsA=="
)
