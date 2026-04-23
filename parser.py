import httpx
from httpx import RequestError
import asyncio

import json
import time
import random
import math

import openpyxl
from openpyxl.styles import Font, Alignment

from loguru import logger

from config import *
from script_test import build_card_url
from token_manager import TokenManager

# Максимальное количество запросов на страницу
MAX_CONCURRENT_REQUESTS_PAGE = 1
# Максимальное количество запросов на карточку
MAX_CONCURRENT_REQUESTS_CARD = 9
MAX_ATTEMPTS = 5  # количество попыток получить один запрос

DELAY_MIN = 3
DELAY_MAX = 5


# Исключение для остановки всех задач парсера
class ParserStoppedException(Exception):
    pass


class Parser:
    def __init__(self):
        self.token = TokenManager()
        self.rows_data = []
        self.stop_event = asyncio.Event()

    async def run(self):
        logger.success("Ехала")
        semaphore_page = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS_PAGE)
        semaphore_card = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS_CARD)
        async with httpx.AsyncClient(
                cookies=COOKIES,
                headers=HEADERS,
                follow_redirects=True,
                timeout=20.0,
        ) as client:
            try:
                total = await self._get_total(client)
                num_pages = math.ceil(total / 100)
                tasks = [self._get_page_data(semaphore_page, semaphore_card, client, page) for page in
                         range(1, num_pages + 1)]
                await asyncio.gather(*tasks)
            except Exception as e:
                logger.error(f"Ошибка: {e}")
            finally:
                self._save_result()
        pass


    def _save_result(self):

        if not self.rows_data:
            print("Нет данных для записи.")
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Товары"

        # Заголовки
        headers = list(self.rows_data[0].keys())
        ws.append(headers)
        # Стиль для заголовков
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Данные
        for row_data in self.rows_data:
            ws.append([row_data.get(h, "") for h in headers])

        # Автоподбор ширины столбцов (простой вариант)
        for col in ws.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_len = max(max_len, len(str(cell.value)))
                except:
                    pass
            adjusted_width = min(max_len + 2, 50)
            ws.column_dimensions[col_letter].width = adjusted_width

        wb.save(OUTPUT_FILENAME)
        logger.success(f"Готово! Файл сохранён: {OUTPUT_FILENAME}")


    async def _get_total(self, client) -> int:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                PARAMS['page'] = 1
                response = await client.get(URL, params=PARAMS)
                if response.status_code >= 200 and response.status_code < 300:
                    data = response.json()
                    total = int(data.get("total", 0))
                    return total
                elif response.status_code == 498:
                    logger.warning(f"{response.status_code}\n{response.text}")
                    await self.token.get_token()
                else:
                    logger.warning(f"{response.status_code}\n{response.text}")
            except RequestError as e:
                logger.warning(f"Ошибка при попытке получить количество всех товаров, попытка {attempt},\nОшибка: {e}")
        raise ParserStoppedException("Парсинг остановлен")


    # Функция полностью извлекает и данные со страницы, и данные карточек по товарам на странице
    async def _get_page_data(self, semaphore_page, semaphore_card, client, page):
        async with semaphore_page:
            response_page = await self._fetch_page(client, page)
            if not response_page:
                return None

            products = response_page.get("products", [])

            tasks = []
            for idx, product in enumerate(products):
                tasks.append(self._build_row(semaphore_card, client, product, page, idx))

            result = await asyncio.gather(*tasks)

    async def _build_row(self, semaphore, client, product, page, idx):
        async with semaphore:

            id = product.get("id")
            if not id:
                return None

            # Запрос к card.json
            # card_url = self.build_card_url(id)
            response = await self._fetch_card(client, id)
            if not response:
                logger.success(f"Товар на странице {page} под номером {idx} не удалось добавить в таблицу.")
                return None

            row = {
                "Ссылка на товар": "-",
                "Артикул": id,
                "Название": "-",
                "Цена": 0,
                "Описание": "-",
                "Ссылки на изображения": "-",
                "Характеристики": "-",
                "Название селлера": "-",
                "Ссылка на селлера": "-",
                "Размеры товара": "-",
                "Остатки по товару": 0,
                "Рейтинг": 0,
                "Количество отзывов": 0,
            }

            if ADD_INFO:
                row["Страница"] = page
                row["Индекс"] = idx
                row["Страна"] = ""

            self.rows_data.append(row)
            logger.success(f"Товар на странице {page} под номером {idx} успешно добавлен в таблицу.")

            return row


    async def _fetch_page(self, client, page):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                delay = random.uniform(DELAY_MIN, DELAY_MAX) + attempt * 2 - 1
                await asyncio.sleep(delay)
                PARAMS['page'] = page
                response = await client.get(URL, params=PARAMS)
                if response.status_code >= 200 and response.status_code < 300:
                    logger.success(f"Страница {page} успешно получена")
                    data = response.json()
                    return data
                elif response.status_code == 498:
                    text = response.text
                    logger.error(f"Страница {page}: Ошибка 498. Ответ: {text}")
                    await self.token.get_token()
                else:
                    logger.warning(f"Страница {page}: Статус {response.status_code}")
                    logger.warning(response.text)
            except RequestError as e:
                logger.warning(f"Ошибка при попытке получить страницу {page}, попытка {attempt},\nОшибка: {e}")
        raise ParserStoppedException("Парсинг остановлен")

    async def _fetch_card(self, client, id):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                card_url = self.build_card_url(id)
                delay = random.uniform(DELAY_MIN, DELAY_MAX) + attempt * 2 - 1
                await asyncio.sleep(delay)
                response = await client.get(card_url)
                if response.status_code >= 200 and response.status_code < 300:
                    data = response.json()
                    return data
                else:
                    logger.success(f"Артикул под номером {id} не обработан.")
                    #logger.warning(response.text)
            except RequestError as e:
                logger.warning(f"Ошибка при попытке получить карту с артикулом {id}, попытка {attempt},\nОшибка: {e}")
        return None

    def build_card_url(self, id):
        id_str = str(id)
        vol = f"vol{id_str[:4]}"
        part = f"part{id_str[:6]}"
        return f"https://sip-basket-cdn-01.geobasket.ru/{vol}/{part}/{id}/info/ru/card.json"
        # Ещё один вариант адреса, но вроде если не работает первый, то и этот тоже не сработает.
        # "https://basket-40.wbbasket.ru/vol1166/part116648/11664879/info/ru/card.json"

