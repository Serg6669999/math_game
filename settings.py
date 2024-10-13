import logging
import os


DIR_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATS_FILE = f"{DIR_ROOT}/math_game/storage/stats/stats.csv"
logging.basicConfig(level="INFO", format="%(module)s %(lineno)d %(processName)s %(threadName)s %(message)s")
log = logging.info
