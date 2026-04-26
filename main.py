import asyncio
from config import DEBUG
from custom_loger import logger
from parser import Parser


async def main():
    logger.debug = DEBUG
    parser = Parser()
    await parser.run()


if __name__ == "__main__":
    asyncio.run(main())
