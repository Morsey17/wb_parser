# название куки с токеном
COOKIE_NEED = 'x_wbaas_token'
URL = 'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search'

# Все товары
OUTPUT_PRODUCTS_FILENAME = "products.xlsx"
# Выборка по критериям
OUTPUT_SELECTION_FILENAME = "products_selection.xlsx"

# DEBUG = False -> Отключает логирование в консоль и оставляет только прогресс бар.
DEBUG = False

# Добавляет дополнительные колонки в итоговые таблицы для проверки
ADD_INFO = False

COOKIES = {
    #'wbx-validation-key': '8fc8ab81-fb27-465b-bad6-feef3bd7c1a4',
    #'external-locale': 'ru',
    #'__zzatw-wb': 'MDA0dBA=Fz2+aQ==',
    #'_cp': '1',
    #'_wbauid': '7408296441772550624',
    #'cfidsw-wb': 'ZPp8S1WnfPhTUuWZyAKy3NEd8WPAZ5SdHo5HumTafABFLVmqh+LOa06d+T+9EbQ7zhN3GvInYNCjbKDIH5fRZlyinY3TBvezPp6VZmiKiuJxU3SyaMONoMjOcvClZHqsVnQIilq042NI7xrHHLZ+l2BIrnUrvZZkpRFG',
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
    #'x-userdata': 'AQMBAAIEAAMDAAozQAGENQAAAAA8AAAAAAA',
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
    'query': 'пальто из натуральной шерсти',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}


if __name__ == "__main__":
    import requests
    response = requests.get(
        'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search',
        params=PARAMS,
        cookies=COOKIES,
        headers=HEADERS,
    )
    print(response.json())

"""

import requests

cookies = {
    'wbx-validation-key': '8fc8ab81-fb27-465b-bad6-feef3bd7c1a4',
    'external-locale': 'ru',
    '__zzatw-wb': 'MDA0dBA=Fz2+aQ==',
    '_cp': '1',
    '_wbauid': '7408296441772550624',
    'cfidsw-wb': 'ZPp8S1WnfPhTUuWZyAKy3NEd8WPAZ5SdHo5HumTafABFLVmqh+LOa06d+T+9EbQ7zhN3GvInYNCjbKDIH5fRZlyinY3TBvezPp6VZmiKiuJxU3SyaMONoMjOcvClZHqsVnQIilq042NI7xrHHLZ+l2BIrnUrvZZkpRFG',
    'routeb': '1776949789.845.907.124074|4cbe85fb742f9006ed4b10eaae805e6b',
    'x_wbaas_token': '1.1000.173781d2a26c4ec5876da1f270c28625.MHwxODUuMTUuMzguNDF8TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0NC4wLjAuMCBZYUJyb3dzZXIvMjYuMy4wLjAgU2FmYXJpLzUzNy4zNnwxNzc4MTU5NzMyfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3NzU1NDkzMnwx.MEUCIQD9o7/WbvgQOqNeItj+/Urvj+jZjwFFt/2epkE+m3C5dgIgN6I7q18DQTMVPcATGI+iNsO3GxYQppXrY/uLhvB3FDw=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NzY5NDk3ODksInVzZXIiOiIxMzc5NDI2MTUiLCJzaGFyZF9rZXkiOiI2IiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiNTdiN2EzODdlZGZmNDljYjgxMzJmNTdmNGMxZDY1ZmQiLCJwaG9uZSI6Ijlwajk4a3ZyU0R6UUNPZUptdGwvWUE9PSIsInZhbGlkYXRpb25fa2V5IjoiOWM2MTkxOTk2YThiNzVkZDA0Njk5ZjU1Mzk3YWMwMjMzODNkYWVjMGU5N2ZlYWIzODUyYzE5OWIzNDMyNjJiNSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNzAzMDAzNjEwLCJ2ZXJzaW9uIjoyfQ.CmzPZA1hC6MlL0YKF800yEaDQ52u_xjtnK0bBSzZDRLMdjd-LKQu13_Llwn1Z4LtLLTUiJfG5v3RgMj5k6sbXJOPLifi1xkJEZhjDh5qCoPiSVcEOPDkLX9DxSsOgGKmS7twExhmkNWw9F2ApoFMGI6nRhVnB0I9X0qCz4I65kZ3AEX3MFoWwEDzIiZgs-4-5EeZGDoZohVQmSdY01lrbYy6YMzzUYGerXvyvnI8QsmdM3OK9CX-Gza_OpdKtfyHnNQx9BuiCaYP81KJ5-hhHaT68amVYlmU7mGq4hOpsa2l3ghzg5OvADBRdz0ctHVLJtP8gHcZZ85PDyP6vZSILw',
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
    'x-userdata': 'AQMBAAIEAAMDAAozQAGENQAAAAA8AAAAAAA',
    'x-userid': '137942615',
    # 'cookie': 'wbx-validation-key=8fc8ab81-fb27-465b-bad6-feef3bd7c1a4; external-locale=ru; __zzatw-wb=MDA0dBA=Fz2+aQ==; _cp=1; _wbauid=7408296441772550624; cfidsw-wb=ZPp8S1WnfPhTUuWZyAKy3NEd8WPAZ5SdHo5HumTafABFLVmqh+LOa06d+T+9EbQ7zhN3GvInYNCjbKDIH5fRZlyinY3TBvezPp6VZmiKiuJxU3SyaMONoMjOcvClZHqsVnQIilq042NI7xrHHLZ+l2BIrnUrvZZkpRFG; routeb=1776949789.845.907.124074|4cbe85fb742f9006ed4b10eaae805e6b; x_wbaas_token=1.1000.173781d2a26c4ec5876da1f270c28625.MHwxODUuMTUuMzguNDF8TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0NC4wLjAuMCBZYUJyb3dzZXIvMjYuMy4wLjAgU2FmYXJpLzUzNy4zNnwxNzc4MTU5NzMyfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3NzU1NDkzMnwx.MEUCIQD9o7/WbvgQOqNeItj+/Urvj+jZjwFFt/2epkE+m3C5dgIgN6I7q18DQTMVPcATGI+iNsO3GxYQppXrY/uLhvB3FDw=',
}

params = {
    'ab_testid': 'model_distance_deboost_on',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'hide_vflags': '4294967296',
    'inheritFilters': 'false',
    'lang': 'ru',
    'locale': 'ru',
    'mdg': '106',
    'query': 'пальто из натуральной шерсти',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
    'uclusters': '0',
}

response = requests.get(
    'https://www.wildberries.ru/__internal/search/exactmatch/ru/common/v18/search',
    params=params,
    cookies=cookies,
    headers=headers,
)

"""