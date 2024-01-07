import logging
import sys

from core.app_config import config

# TODO: implement normal logger..
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(config.LOGLEVEL.upper()))
logger.addHandler(logging.StreamHandler(sys.stdout))
