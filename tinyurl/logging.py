import logging
import os
from logging.config import dictConfig

import yaml
from dotenv import load_dotenv

path = "./log_config.yaml"

if not os.path.exists(path):
    raise FileNotFoundError("Log Config File Not Found")

log_config = yaml.load(open(path, "r"), Loader=yaml.FullLoader)
dictConfig(log_config)
load_dotenv()

env = os.environ.get("TINYURL_ENV", "local")
print(env)
turl_logger = logging.getLogger(env)
