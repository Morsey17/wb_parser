# Название куки с токеном для антибот защиты.
from openpyxl.pivot.cache import Query

COOKIE_NEED = 'x_wbaas_token'
# Файл с токеном для антибот защиты на ВБ. Создаётся автоматически, если не был найден.
TOKEN_FILENAME = "token.secret"
# URL-адерс, на который будут посылаться основные запросы.
URL = 'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search'
# Собственно сам запрос
QUERY = 'пальто из натуральной шерсти'

# Максимальное количество попыток одного запроса
MAX_ATTEMPTS = 5

# Минимальная задержка между одним и тем же запросом
DELAY_MIN = 3
# Максимальная задержка между одним и тем же запросом при первой попытке (дальше  может быть и больще)
DELAY_MAX = 6

# Максимальное количество запросов на страницу (небольшая недоработка и лучше не трогать, всегда ставляя = 1)
MAX_CONCURRENT_REQUESTS_PAGE = 1
# Максимальное количество запросов на карточку (из наблюдений лучшее значение = 9)
MAX_CONCURRENT_REQUESTS_CARD = 9

# Включает/отключает логирование в консоль и оставляет только прогресс бар.
DEBUG_CONSOLE = True
# Сохранять логи в файлы (для отладки)
SAVE_LOGS = True
# Сохранять ответы запросов в файлы (для отладки)
SAVE_RESPONSE = True

# Добавляет дополнительные колонки в итоговые таблицы для проверки
ADD_INFO = False


# Ошибка для остановки парсера при определённых условиях
class ParserStoppedException(Exception):
    pass


COOKIES = {
    # 'wbx-validation-key': '8fc8ab81-fb27-465b-bad6-feef3bd7c1a4',
    # 'external-locale': 'ru',
    # '__zzatw-wb': 'MDA0dBA=Fz2+aQ==',
    # '_cp': '1',
    # '_wbauid': '7408296441772550624',
    # 'cfidsw-wb': 'ZPp8S1WnfPhTUuWZyAKy3NEd8WPAZ5SdHo5HumTafABFLVmqh+LOa06d+T+9EbQ7zhN3GvInYNCjbKDIH5fRZlyinY3TBvezPp6VZmiKiuJxU3SyaMONoMjOcvClZHqsVnQIilq042NI7xrHHLZ+l2BIrnUrvZZkpRFG',
    'x_wbaas_token': '1.1000.173781d2a26c4ec5876da1f270c28625.MHwxODUuMTUuMzguNDF8TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0NC4wLjAuMCBZYUJyb3dzZXIvMjYuMy4wLjAgU2FmYXJpLzUzNy4zNnwxNzc4MTU5NzMyfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3NzU1NDkzMnwx.MEUCIQD9o7/WbvgQOqNeItj+/Urvj+jZjwFFt/2epkE+m3C5dgIgN6I7q18DQTMVPcATGI+iNsO3GxYQppXrY/uLhvB3FDw=',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'no-cache',
    'deviceid': 'site_a7c9a5465c3b4a0984fa1f5df494e5fe',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "YaBrowser";v="26.3", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 YaBrowser/26.3.0.0 Safari/537.36',
    'x-queryid': 'qid740829644177255062420260423132110',
    'x-requested-with': 'XMLHttpRequest',
    'x-spa-version': '14.6.4',
    # 'x-userdata': 'AQMBAAIEAAMDAAozQAGENQAAAAA8AAAAAAA',
    'x-userid': '0',
}

PARAMS = {
    'ab_testid': 'model_distance_deboost_on',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'hide_vflags': '4294967296',
    'lang': 'ru',
    'page': '1',
    'query': QUERY,
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}

if __name__ == "__main__":
    import requests

    response = requests.get(
        url=URL,
        params=PARAMS,
        cookies=COOKIES,
        headers=HEADERS,
    )
    print(response.json())
