import httpx
from httpx import RequestError
import asyncio

import json
import aiofiles
import random
import math

import openpyxl
from openpyxl.styles import Font, Alignment

from custom_loger import logger
from tqdm import tqdm, trange

from config import *
from token_manager import TokenManager

# Максимальное количество запросов на страницу
MAX_CONCURRENT_REQUESTS_PAGE = 1
# Максимальное количество запросов на карточку
MAX_CONCURRENT_REQUESTS_CARD = 9
MAX_ATTEMPTS = 5  # количество попыток получить один запрос

DELAY_MIN = 3
DELAY_MAX = 6


# Исключение для остановки всех задач парсера
class ParserStoppedException(Exception):
    pass

class Parser:
    def __init__(self, debug_console=True, save_response=True, output_path="output/"):
        # Элементы массива - спарсенные товары
        self.debug_console = debug_console
        self.save_response = save_response
        self.output_path = output_path
        self.rows_data = []
        # Элементы этого массива - индексы предудыщего массива, которые проходят условие и сохраняются отдельным файлом
        self.rows_index_with_condition = []
        self.stop_event = asyncio.Event()
        self.token = None
        self.progress_bar = None


    async def run(self):
        logger.success("Парсер запущен!", True)
        self.token = TokenManager()
        await self.token.init()
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
                if not total or total <= 0:
                    return

                if not self.debug_console:
                    self.progress_bar = trange(total, ncols=100)
                num_pages = math.ceil(total / 100)
                tasks = [self._get_page_data(semaphore_page, semaphore_card, client, page) for page in
                         range(1, num_pages + 1)]
                await asyncio.gather(*tasks)
            except Exception as e:
                logger.error(f"Фатальная ошибка, конец...\n{e}", True)
            finally:
                if self.progress_bar:
                    self.progress_bar.close()

                # Окончание работы парсера (нужно для сохранения результатов)
                self._save_result(range(len(self.rows_data)), f"{self.output_path}products.xlsx")
                self._save_result(self.rows_index_with_condition, f"{self.output_path}products_selection.xlsx")


    def get_delay(self, attempt):
        return random.uniform(DELAY_MIN, DELAY_MAX) + (attempt - 1) * 3


    def _save_result(self, value_list, filepath: str):

        if not self.rows_data or not value_list:
            logger.warning("Нет данных для записи.")
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
        for idx in value_list:
            ws.append([self.rows_data[idx].get(h, "") for h in headers])

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

        try:
            wb.save(filepath)
            logger.success(f"Результат сохранён в файл по пути: {filepath}", True)
        except:
            logger.error(f"Не удалось сохранить файл по пути {filepath}", True)


    async def _get_total(self, client) -> int:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                PARAMS['page'] = 1
                response = await client.get(URL, params=PARAMS)
                if response.status_code >= 200 and response.status_code < 300:
                    data = response.json()
                    total = int(data.get("total", 0))
                    logger.success(f"Всего количество товароа: {total}")
                    return total
                elif response.status_code == 498:
                    logger.warning(f"{response.status_code}\n{response.text}")
                    await self.token.get_token()
                else:
                    logger.warning(f"{response.status_code}\n{response.text}")
            except RequestError as e:
                logger.warning(f"Ошибка при попытке получить количество всех товаров, попытка {attempt}")
        logger.error(f"Не получилось получить количество товара, это конец...")
        raise ParserStoppedException("Парсинг остановлен")


    # Функция полностью извлекает и данные со страницы, и данные карточек по товарам на странице
    async def _get_page_data(self, semaphore_page, semaphore_card, client, page):
        async with semaphore_page:
            response_page = await self._fetch_page(client, page)
            if not response_page:
                logger.warning(f"Не удалось получить страницу {page}")
                return None
            elif self.save_response:
                filename = f"{self.output_path}data_page_{page}.json"
                async with aiofiles.open(filename, "w", encoding="utf-8") as f:
                    await f.write(json.dumps(response_page, ensure_ascii=False, indent=4))

            products = response_page.get("products", [])

            tasks = []
            for idx, product in enumerate(products):
                tasks.append(self._build_row_data(semaphore_card, client, product, page, idx))

            result = await asyncio.gather(*tasks)

    async def _build_row_data(self, semaphore, client, product: dict, page, idx):
        async with semaphore:

            article_id = product.get("id")
            if not id:
                return None

            # Запрос к card.json
            card_info = await self._fetch_card(client, article_id)

            if self.progress_bar:
                self.progress_bar.update(1)

            if not card_info:
                logger.warning(f"Не удалось получить карточку товара на странице {page} под номером {idx}. Артикул: {article_id}")

            row, is_russian = self.parse_data(article_id, product, card_info, ADD_INFO, page, idx)
            self.rows_data.append(row)
            # Добавляем индекс строки в отдельный массив для сохранения в отдельный файл.
            if row["Цена"] < 1000000 and row["Рейтинг"] >= 4.5 and is_russian:
                self.rows_index_with_condition.append(len(self.rows_data) - 1)

            logger.success(f"Товар на странице {page} под номером {idx} успешно добавлен в таблицу. Артикул: {article_id}")

            return row


    def parse_data(self, article_id, product, card_info, add_info=False, page=0, idx=0) -> [dict, bool]:
        row = {
            "Ссылка на товар": f"https://www.wildberries.ru/catalog/{article_id}/detail.aspx",
            "Артикул": article_id,
            "Название": product.get("name", ""),
            "Цена": self.get_price(product),
            "Описание": card_info.get("description", ""),
            "Ссылки на изображения": self.generate_image_urls(article_id, product.get("pics", 0)),
            "Характеристики": json.dumps(card_info.get("options", []), ensure_ascii=False),
            "Название селлера": product.get("supplier", ""),
            "Ссылка на селлера": f"https://www.wildberries.ru/seller/{product.get('supplierId', '')}",
            "Размеры товара": self.get_size(product),
            "Остатки по товару": product.get("totalQuantity", 0),
            "Рейтинг": product.get("reviewRating", 0),
            "Количество отзывов": product.get("feedbacks", 0),
        }
        is_russian = self.get_country(card_info.get("options", []))
        if add_info:
            row["Страница"] = page
            row["Индекс"] = idx
            row["Россия"] = "Да" if is_russian else "Нет"
        return row, is_russian


    def get_size(self, product):
        sizes_str = ""
        sizes = product.get("sizes", [])
        for i, size in enumerate(sizes):
            value = size.get("name", "")
            if len(value) > 0:
                sizes_str += value
                if i < len(sizes) - 1:
                    sizes_str += ", "
        return sizes_str


    def get_country(self, options):

        for option in options:
            if option.get("name") == "Страна производства":
                #logger.info(option.get("value", ""))
                value_list = ["Россия", "РФ", "Российская Федерация"]
                if option.get("value", "") in value_list:
                    return True
                else:
                    return False
        return False


    def generate_image_urls(self, id, pics_count):
        urls_string = ""
        id_str = str(id)
        add_len = len(id_str) - 5
        vol = f"vol{id_str[:add_len]}"
        part = f"part{id_str[:add_len + 2]}"
        for pic in range(1, pics_count + 1):
            urls_string += f"https://sip-basket-cdn-01.geobasket.ru/{vol}/{part}/{id}/images/big/{pic}.webp"
            if pic <= pics_count:
                urls_string += ", "
        return urls_string
        #return f"https://basket-12.wbbasket.ru/vol1743/part174345/174345729/images/big/20.webp"


    def get_price(self, product: dict) -> int:
        for size in product.get("sizes", []):
            price = size.get("price", {})
            if price.get("product"):
                return price["product"]
        return 0


    async def _fetch_page(self, client, page):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                delay = self.get_delay(attempt)
                await asyncio.sleep(delay)
                PARAMS['page'] = page
                response = await client.get(URL, params=PARAMS)
                if response.status_code >= 200 and response.status_code < 300:
                    try:
                        data = response.json()
                        products = data.get("products", [])
                        if products:
                            logger.success(f"Страница {page} успешно получена")
                            return data
                        else:
                            continue
                    except:
                        continue
                elif response.status_code == 498:
                    text = response.text
                    logger.error(f"Страница {page}: Ошибка 498. Ответ: {text}")
                    await self.token.get_token()
                else:
                    logger.warning(f"Страница {page}: Статус {response.status_code}")
                    logger.warning(response.text)
            except RequestError as e:
                pass
                #logger.warning(f"Ошибка при попытке получить страницу {page}, попытка {attempt}")
        raise ParserStoppedException("Парсинг остановлен")

    async def _fetch_card(self, client, article_id):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                card_url = self.build_card_url(article_id)
                delay = self.get_delay(attempt)
                await asyncio.sleep(delay)
                response = await client.get(card_url)
                if response.status_code >= 100 and response.status_code < 300:
                    data = response.json()
                    return data
            except RequestError as e:
                pass

        #logger.error(f"Не удалось получить карту с артикулом {article_id}.")
        return {}

    def build_card_url(self, article_id):
        id_str = str(article_id)
        # Вспомогительная переменная. Значения vol и part зависят от длины артикула
        add_len = len(id_str) - 5
        vol = f"vol{id_str[:add_len]}"
        part = f"part{id_str[:add_len+2]}"
        url = f"https://sip-basket-cdn-01.geobasket.ru/{vol}/{part}/{article_id}/info/ru/card.json"
        "https://sip-basket-cdn-01.geobasket.ru/6940/694038/694038423/info/ru/card.json"
        return url

