import time
import os
import asyncio
from seleniumbase import Driver
from loguru import logger
from typing import Optional

from config import *

# Количество попыток получить токен
MAX_ATTEMPTS = 3
# Путь к файлу со старым токеном, чтобы каждый раз не создавать новый
TOKEN_FILENAME = "token.secret"

#lock = asyncio.Lock()


class TokenManager:
    def __init__(self):
        self.cookie_need = COOKIE_NEED
        self.url = URL_TO_PAGE
        self.user_agent = HEADERS['user-agent']
        self.token = None
        self._get_token_from_file()
        if not self.token:
            self.get_fresh_token()


    def get_fresh_token(self):
        # Запускает браузер и извлекает токен x_wbaas_token.
        driver = Driver(
            uc=True,        # Undetected Chrome - обход защиты
            headed=False,   # Без графического интерфейса
            headless=True,  # В фоновом режиме
            agent=self.user_agent,
        )
        try:
            logger.info(f"Открываем {self.url} с User-Agent: {self.user_agent[:50]}...")
            driver.open(self.url)

            # Даем время на установку всех кук (3 попытки с интервалом 5 сек)
            for i in range(MAX_ATTEMPTS):
                cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
                logger.debug(f"Попытка {i + 1}")

                for cookie in cookies.get("cookies", []):
                    if cookie.get("name") == COOKIE_NEED:
                        self.token = cookie.get("value")
                        logger.success(f"Токен успешно получен")
                        logger.info(f"Токен: {self.token}...")
                        self._save_token_to_file()

                # Если токен еще не появился, ждем
                if i < MAX_ATTEMPTS - 1:
                    time.sleep(5)

            logger.error(f"Не удалось получить токен после всех попыток")

        except Exception as e:
            logger.error(f"Ошибка при получении токена: {e}")
        finally:
            driver.quit()
            logger.debug("Браузер закрыт")


    def _save_token_to_file(self):
        try:
            with open(TOKEN_FILENAME, 'w', encoding='utf-8') as f:
                f.write(self.token)
            logger.success(f"Токен сохранен в {TOKEN_FILENAME}")
        except Exception as e:
            logger.error(f"Ошибка записи в {TOKEN_FILENAME}: {e}")


    def _get_token_from_file(self):
        if os.path.exists(TOKEN_FILENAME):
            try:
                with open(TOKEN_FILENAME, 'r', encoding='utf-8') as f:
                    self.token = f.read().strip()
                    logger.success(f"Токен загружен из {TOKEN_FILENAME}")
            except Exception as e:
                logger.error(f"Ошибка чтения {TOKEN_FILENAME}: {e}")


    """
    async def get_token(self):
        async with asyncio.Lock() as lock:
            if self.token == False:
                token = await asyncio.to_thread(self._get_token_from_file)
                if token:
                    COOKIES[self.cookie_need] = token
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
    """



# Для тестирования модуля напрямую
if __name__ == "__main__":
    token = TokenManager()
    token.get_fresh_token()
    if token.token:
        print(f"\nТокен получен:\n{token.token}")
    else:
        print("\nОшибка получения токена")