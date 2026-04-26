"""
Хотелось иметь возможность переключать вывод логов в консоль и в файл и чтоб для этого использовались
одни и те же функции. Поэтому создал кастомный логгер на основе loguru как обёртку.

"""
import sys
from loguru import logger as logger_


class CustomLogger:
    def __init__(self):
        self.to_console = True
        self.to_file = False
        self.output_path = ""

    # Дополнительная инциализация нужна для того, чтобы пробросить важные параметры из модуля main,
    # но сам logger уже был объявлен до этого момента.
    def init(self, to_console=True, to_file=False, output_path="output_path/"):
        self.to_console = to_console
        self.to_file = to_file
        self.output_path = output_path
        logger_.remove()
        if to_file:
            logger_.add(
                f"{output_path}logs.log",
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

    def success(self, value, to_console=None):
        to_console = to_console or self.to_console
        logger_.opt(depth=1).bind(to_console=to_console).success(value)

    def info(self, value, to_console=None):
        to_console = to_console or self.to_console
        logger_.opt(depth=1).bind(to_console=to_console).info(value)

    def warning(self, value, to_console=None):
        to_console = to_console or self.to_console
        logger_.opt(depth=1).bind(to_console=to_console).warning(value)

    def error(self, value, to_console=None):
        to_console = to_console or self.to_console
        logger_.opt(depth=1).bind(to_console=to_console).error(value)

    def debug(self, value, to_console=None):
        to_console = to_console or self.to_console
        logger_.opt(depth=1).bind(to_console=to_console).error(value)


logger = CustomLogger()

if __name__ == "__main__":
    logger.init(True, False, "")
    logger.info("АЛЁ")
    logger.error("Как дела?")
    logger.debug = False
    logger.success("Wtf bro?")
