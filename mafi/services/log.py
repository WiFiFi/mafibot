import logging
import sys
from config.service_config import LOGGING_LEVEL


_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(
    logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s')
)

logger = logging.getLogger('mafi')
logger.addHandler(_handler)
logger.setLevel(LOGGING_LEVEL)