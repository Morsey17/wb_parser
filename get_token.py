import time
import os
import asyncio
from seleniumbase import Driver
from loguru import logger

from typing import Optional

import config

COOKIE_NEED = 'x_wbaas_token'
URL = config.URL
USER_AGENT = config.HEADERS['user-agent']
MAX_ATTEMPTS = 3
FILENAME = "token.secret"

lock = asyncio.Lock()

#class TokenManager:
#    def __init__(self):

"""class WebdriverCookies:
    def __init__(self, user_agent: str = None, url: str = None, cookie_need: str = None):
        # Если параметры не переданы, берем из config.py
        self.user_agent = USER_AGENT
        self.url = URL
        self.cookie_need = COOKIE_NEED
"""

def get_fresh_token() -> Optional[str]:
    """
    Запускает браузер и извлекает токен x_wbaas_token.
    """
    driver = Driver(
        uc=True,        # Undetected Chrome - обход защиты
        headed=False,   # Без графического интерфейса
        headless=True,  # В фоновом режиме
        agent=USER_AGENT,
    )
    try:
        logger.info(f"Открываем {URL} с User-Agent: {USER_AGENT[:50]}...")
        driver.open(URL)

        # Даем время на установку всех кук (3 попытки с интервалом 5 сек)
        for i in range(MAX_ATTEMPTS):
            cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
            logger.debug(f"Попытка {i + 1}")

            for cookie in cookies.get("cookies", []):
                if cookie.get("name") == COOKIE_NEED:
                    token = cookie.get("value")
                    logger.success(f"Токен успешно получен")
                    logger.info(f"Токен: {token}...")
                    try:
                        with open(FILENAME, 'w', encoding='utf-8') as f:
                            f.write(token)
                        logger.success(f"Токен сохранен в {FILENAME}")
                    except Exception as e:
                        logger.error(f"Ошибка записи в {FILENAME}: {e}")
                    return token

            # Если токен еще не появился, ждем
            if i < MAX_ATTEMPTS - 1:
                time.sleep(5)

        logger.error(f"Не удалось получить токен после всех попыток")
        return None

    except Exception as e:
        logger.error(f"Ошибка при получении токена: {e}")
        return None
    finally:
        driver.quit()
        logger.debug("Браузер закрыт")


def get_token_from_file() -> Optional[str]:
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'r', encoding='utf-8') as f:
                token = f.read().strip()
                logger.success(f"Токен загружен из {FILENAME}")
                return token
        except Exception as e:
            logger.error(f"Ошибка чтения {FILENAME}: {e}")
            return None # Будет сгенерирован новый токен



async def get_token(fresh_token: bool) -> (Optional[str], bool):
    async with lock:

        if not fresh_token:
            token = await asyncio.to_thread(get_token_from_file)
            if token:
                config.COOKIES[COOKIE_NEED] = token
                return token, False
            else:
                # Если не получилось взять токен из файла, создаём новый
                fresh_token = True

        if fresh_token:
            # try:
            # Запускаем синхронную функцию обновления в отдельном потоке
            # new_token = await asyncio.to_thread(self._sync_refresh_token)
            # self._token = new_token
            token = await asyncio.to_thread(get_fresh_token)
            if token:
                config.COOKIES[COOKIE_NEED] = token
                return token, True

        logger.error("Не удалось получить токен")
        raise RuntimeError("Не удалось получить токен")



# Для тестирования модуля напрямую
if __name__ == "__main__":
    token = get_token(fresh_token=True)
    if token:
        print(f"\nТокен получен:\n{token}")
    else:
        print("\nОшибка получения токена")