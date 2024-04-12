import logging
import os


DIR_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
logging.basicConfig(level="INFO", format="%(processName)s %(threadName)s %(message)s")
log = logging.info
