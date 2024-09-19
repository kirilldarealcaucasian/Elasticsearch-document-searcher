from logging import getLogger, StreamHandler, Formatter, DEBUG


__all__ = (
    "logger",
)

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class CustomFormatter(Formatter):
    def format(self, record):
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = record.levelname
        message = record.getMessage()
        path = record.pathname
        line = record.lineno

        white_text = "\033[97m"
        reset_text = "\033[0m"

        return f"{white_text}{timestamp} [{level}] {path}[line:{line}]: {message}{reset_text}"


# setup logger
log_handler = StreamHandler()
log_handler.setFormatter(fmt=CustomFormatter())
logger.addHandler(hdlr=log_handler)


