import os
from abc import ABC
from typing import List, Type

class ProductionConfig(ABC):
    CONFIG_NAME = "production"
    VRCHAT_AUTH = os.getenv('VRCHAT_AUTH')
    NOUNCE = os.getenv('NOUNCE')
    BOT_KEY = os.getenv('BOT_KEY')
    DISCORD_KEY = os.getenv('DISCORD_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')

class DevelopmentConfig(ABC):
    CONFIG_NAME = "development"
    try:
        from local_secrets import secret_dict
    except ImportError:
        secret_dict = {x:None for x in ["CONFIG_NAME","VRCHAT_AUTH","NOUCE","BOT_KEY","DISCORD_KEY","DATABASE_LOCAL"]}
    VRCHAT_AUTH = secret_dict["VRCHAT_AUTH"]
    NOUNCE = secret_dict["NOUNCE"]
    BOT_KEY = secret_dict["BOT_KEY"]
    DISCORD_KEY = secret_dict["DISCORD_KEY"]
    DATABASE_URL = secret_dict["DATABASE_LOCAL"]

EXPORT_CONFIGS: List[Type[ABC]] = {
    ProductionConfig,
    DevelopmentConfig
}

config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}