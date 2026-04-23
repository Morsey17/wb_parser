import httpx
import asyncio
import json
import time
import random
from loguru import logger

from config import *
from token_manager import TokenManager


MAX_CONCURRENT_REQUESTS = 2
NUM_PAGES = 5
MAX_ATTEMPTS = 5 # количество попыток получить один запрос

is_fresh_token = False
token = None


def time_decorator(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"Время выполнения функции: {end_time - start_time:.2f} секунд")
        return result
    return wrapper



products = []


def parse_data(data):
    for product in data['products']:
        products.append(product['id'])


async def fetch_wildberries_page(semaphore, client, page):

    async with semaphore:
        PARAMS['page'] = page
        for attempt in range(1, MAX_ATTEMPTS + 1):
            response = await client.get(URL, params=PARAMS)
            assert (response.status_code >= 200 and response.status_code < 300)

            if response.status_code >= 200 and response.status_code < 300:
                logger.success(f"Страница {page} успешно получена")
                data = response.json()
                parse_data(data)
                delay = random.uniform(1, 3)
                await asyncio.sleep(delay)
                return data
            elif response.status == 498:
                global token
                global is_fresh_token
                text = await response.text()
                logger.error(f"Страница {page}: Ошибка 498. Ответ: {text}")
                if is_fresh_token == False:
                    token, is_fresh_token = get_token(fresh_token=True)
            else:
                logger.warning(
                    f"Страница {page}: Статус {response.status}")  # . Попытка {attempt}/{MAX_RETRIES}")

        delay = random.uniform(3, 5)
        await asyncio.sleep(delay)

@time_decorator
async def main():
    global token
    global is_fresh_token
    token, is_fresh_token = await get_token(fresh_token=False)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with httpx.AsyncClient(cookies=COOKIES, headers=HEADERS, follow_redirects=True) as client:
        tasks = [fetch_wildberries_page(semaphore, client, page) for page in range(1, NUM_PAGES + 1)]
        result = await asyncio.gather(*tasks)

    for product in products:
        print(product)

    #result = await fetch_wildberries_httpx()
    #print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        logger.error("Процесс остановлен")
        time.sleep(10)