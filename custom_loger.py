import loguru
from config import DEBUG

class CustomLogger:
    def __init__(self):
        pass

    @staticmethod
    def success(value, debug=DEBUG):
        if debug:
            loguru.logger.opt(depth=1).success(value)

    @staticmethod
    def info(value, debug=DEBUG):
        if debug:
            loguru.logger.opt(depth=1).info(value)

    @staticmethod
    def warning(value, debug=DEBUG):
        if debug:
            loguru.logger.opt(depth=1).warning(value)

    @staticmethod
    def error(value, debug=DEBUG):
        if debug:
            loguru.logger.opt(depth=1).error(value)


logger = CustomLogger()


if __name__ == "__main__":
    logger.info("Ну чё")
    logger.error("Ашыбка")
    loguru.logger.info("Почему")