import os
from config import config_by_name

env_case = os.getenv("ENV_CASE")

dict_config = config_by_name[env_case].__dict__

def run():
    globals.update(dict_config)