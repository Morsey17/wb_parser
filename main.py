import asyncio
import time
from loguru import logger
from parser import Parser


async def main():
    parser = Parser()
    await parser.run()


if __name__ == "__main__":
    asyncio.run(main())
