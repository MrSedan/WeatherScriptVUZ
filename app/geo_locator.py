import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_ipinfo(geo_api_url: str):
    try:
        r = requests.get(geo_api_url)
        r.raise_for_status()
        data = r.json()
    except HTTPError as http_error:
        raise Exception(f"Ошибка HTTP: {http_error}")
    except ConnectionError as conn_error:
        raise Exception(f"Ошибка подключения: {conn_error}")
    except Timeout as time_error:
        raise Exception(f"Ошибка таймаута: {time_error}")
    except RequestException as req_error:
        raise Exception(f"Ошибка запроса: {req_error}")
    except Exception as e:
        raise Exception(f"Непредвиденная ошибка: {e}")

    city: str = data['city']
    loc: list = data["loc"].split(',')
    if len(loc) != 2:
        raise Exception('Bad request')
    return city, loc
