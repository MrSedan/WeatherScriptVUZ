import requests
from requests.exceptions import HTTPError, ConnectionError, RequestException, Timeout
from .weather_dto import Weather, ListElement
from typing import List, Dict
from statistics import mean
from collections import Counter


def group_days(data: List[ListElement]):
    days: Dict[str, List[ListElement]] = dict()
    i = 0
    while 1:
        if len(data) <= i:
            break
        item = data[i]
        date = item.dt_txt.split(" ")[0]
        if date not in days:
            if len(days.keys()) == 4:
                break
            days[date] = [item]
        else:
            days[date].append(item)
        i += 1

    return days


def get_description(items: List[ListElement]):
    noon_point = next((p for p in items if "12:00:00" in p.dt_txt), None)
    if noon_point:
        description = noon_point.weather[0].description
    else:
        all_descriptions = [p.weather[0].description for p in items]

        most_freq = Counter(all_descriptions).most_common(1)[0][0]
        description = most_freq
    return description


def aggregate_days(days: Dict[str, List[ListElement]]):
    result = {key: dict() for key in days.keys()}
    for day, list_items in days.items():
        result[day]["min_temp"] = min(item.main['temp_min']
                                      for item in list_items)
        result[day]["max_temp"] = max(item.main['temp_max']
                                      for item in list_items)
        result[day]["humidity"] = mean(
            item.main['humidity'] for item in list_items)
        result[day]["max_wind"] = max(item.wind.speed for item in list_items)
        result[day]["description"] = get_description(list_items)
    return result


def get_weather(weather_base_url, weather_api_key, weather_fallback_city, lat='', lon=''):
    fallback_mode = lat == lon == ''
    try:
        r = requests.get(
            f"{weather_base_url}/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric&lang=ru" if not fallback_mode else f"{weather_base_url}/data/2.5/forecast?q={weather_fallback_city}&appid={weather_api_key}&units=metric&lang=ru")
        r.raise_for_status()
        data = Weather.from_dict(r.json())
        cod = data.cod
        if cod == 401:
            raise Exception("Неверный ключ API")
        elif cod == 404 and not fallback_mode:
            return get_weather(weather_base_url, weather_api_key, weather_fallback_city), weather_fallback_city
        elif cod == 404:
            raise Exception("Город не найден")
        elif cod == 429:
            raise Exception("Превышение лимита запросов")
        groupped = group_days(data.list)
        return aggregate_days(groupped), weather_fallback_city if fallback_mode else ''
    except HTTPError as http_error:
        raise Exception(f"Ошибка HTTP: {http_error}")
    except ConnectionError as conn_error:
        raise Exception(f"Ошибка подключения: {conn_error}")
    except Timeout as time_error:
        raise Exception(f"Ошибка таймаута: {time_error}")
    except RequestException as req_error:
        raise Exception(f"Ошибка запроса: {req_error}")
    except Exception as e:
        raise Exception(f"Ошибка: {e}")
