import asyncio
import os
from datetime import datetime

from parser import Parser
from config import *
from custom_loger import logger


async def main():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"output_{timestamp}/"
    os.makedirs(output_path, exist_ok=True)
    logger.init(DEBUG_CONSOLE, SAVE_LOGS, output_path)
    parser = Parser(DEBUG_CONSOLE, SAVE_RESPONSE, output_path)
    await parser.run()


if __name__ == "__main__":
    asyncio.run(main())
