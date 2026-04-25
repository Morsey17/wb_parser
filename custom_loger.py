import sys
from loguru import logger as logger_
from config import DEBUG

# 1. Удаляем стандартный вывод в консоль, который loguru добавляет по умолчанию
logger_.remove()

# 2. Добавляем запись в файл (всегда, независимо от DEBUG)
logger_.add(
    "logs.log",               # имя файла
    rotation="10 MB",         # опционально: ротация при достижении 10 МБ
    retention="7 days",       # опционально: хранить логи 7 дней
    level="DEBUG",            # пишем всё от DEBUG и выше
    encoding="utf-8"
)

# 3. Добавляем вывод в консоль только если DEBUG = True
if DEBUG:
    logger_.add(
        sys.stdout,
        level="DEBUG",
        format="{time} | {level} | {message}",  # кастомный формат, можно любой
        colorize=True          # цветной вывод в консоль
    )

# 4. Твой класс-обёртка теперь просто передаёт вызовы в loguru без проверки DEBUG
class CustomLogger:
    @staticmethod
    def success(value, debug=False):
        logger_.opt(depth=1).success(value)

    @staticmethod
    def info(value, debug=False):
        logger_.opt(depth=1).info(value)

    @staticmethod
    def warning(value, debug=False):
        logger_.opt(depth=1).warning(value)

    @staticmethod
    def error(value, debug=False):
        logger_.opt(depth=1).error(value)

logger = CustomLogger()