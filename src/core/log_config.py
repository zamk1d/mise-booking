import logging

from src.core.config import settings


RESET = "\033[0m"
DIM = "\033[2m"
BLUE = "\033[34m"

LEVEL_COLORS = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[35m",
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")

        color = LEVEL_COLORS.get(record.levelno, RESET)
        level = f"{color}{record.levelname:<8}{RESET}"

        logger_name = f"{BLUE}{record.name}{RESET}"

        return (
            f"{DIM}{timestamp}{RESET} | "
            f"{level} | "
            f"{logger_name} | "
            f"{record.getMessage()}"
        )


def setup_logging() -> None:
    level = logging.DEBUG if settings.debug else logging.INFO

    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.debug else logging.WARNING
    )

    logging.getLogger(__name__).info(
        "Logging configured (level=%s)",
        logging.getLevelName(level),
    )