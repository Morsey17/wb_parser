import sys
from loguru import logger as logger_
from datetime import datetime

logger_.remove()

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

logger_.add(
    f"logs_{timestamp}.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    encoding="utf-8",
    filter=lambda record: True  # все записи идут в файл
)

logger_.add(
    sys.stdout,
    format="<level>{time:HH:mm:ss} | {level: <8} | {message}</level>",
    colorize=True,
    level="DEBUG",
    filter=lambda record: record["extra"].get("to_console", False)
)

class CustomLogger:
    def __init__(self, debug=True):
        self.debug = debug

    def success(self,value, to_console=None):
        to_console = to_console or self.debug
        logger_.opt(depth=1).bind(to_console=to_console).success(value)

    def info(self,value, to_console=None):
        to_console = to_console or self.debug
        logger_.opt(depth=1).bind(to_console=to_console).info(value)

    def warning(self,value, to_console=None):
        to_console = to_console or self.debug
        logger_.opt(depth=1).bind(to_console=to_console).warning(value)

    def error(self,value, to_console=None):
        to_console = to_console or self.debug
        logger_.opt(depth=1).bind(to_console=to_console).error(value)

logger = CustomLogger()

if __name__ == "__main__":
    logger.debug = True
    logger.info("АЛЁ")
    logger.error("Как дела?")
    logger.debug = False
    logger.success("Wtf bro?")