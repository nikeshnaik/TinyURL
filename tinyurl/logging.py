import logging
import os
from logging.config import dictConfig

import yaml

from settings import Settings

if not os.path.exists(Settings.LOG_CONFIG):
    raise FileNotFoundError("Log Config File Not Found")

log_config = yaml.load(open(Settings.LOG_CONFIG, "r"), Loader=yaml.FullLoader)
dictConfig(log_config)

turl_logger = logging.getLogger(Settings.TINY_URL_ENV)
