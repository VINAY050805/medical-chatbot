from loguru import logger
import sys

# Remove default logger
logger.remove()

# Console Logger
logger.add(

    sys.stdout,

    level="INFO",

    colorize=True,

    backtrace=False,

    diagnose=False,

    format=(
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{message}</cyan>"
    )

)