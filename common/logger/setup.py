from logging import Formatter, StreamHandler, getLogger

from common.config import settings

__all__ = ("logger",)

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


class CustomFormatter(Formatter):
    def format(self, record):
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = record.levelname
        message = record.getMessage()
        path = record.pathname
        line = record.lineno
        exc_text = record.exc_text
        exc_info = record.exc_info
        extras = ", ".join(
            f"{k}={v}"
            for k, v in record.__dict__.items()
            if k
            not in [
                "args",
                "levelname",
                "levelno",
                "lineno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "msg",
                "exc_text",
                "name",
                "process",
                "processName",
                "thread",
                "threadName",
                "stack_info",
                "func_name",
                "created",
                "msecs",
                "relativeCreated",
                "funcName",
            ]
        )

        blue_text = "\033[94m"
        reset_color = "\033[0m"

        return f"""{blue_text}{timestamp} [{level}] {path}[line:{line}]: {message}{reset_color} {exc_text if exc_text else ''} {exc_info if exc_info else ''} {'extra: ' + extras if extras else ''}"""  # noqa


# setup logger
log_handler = StreamHandler()
log_handler.setFormatter(fmt=CustomFormatter())
logger.addHandler(hdlr=log_handler)
