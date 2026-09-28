from app import get_ipinfo, get_weather, create_db_and_tables, save_forecast, export_to_markdown
from dotenv import load_dotenv
import os

WEATHER_API_KEY = ""
WEATHER_API_BASE_URL = ""
GEO_API_URL = ""
GEO_API_FALLBACK_CITY = ""
DB_URL = ""
DB_USER = ""
DB_PASSWORD = ""
OUTPUT_FILE = ""


def setup():
    global WEATHER_API_KEY, GEO_API_FALLBACK_CITY, GEO_API_URL
    global DB_PASSWORD, DB_URL, DB_USER, WEATHER_API_BASE_URL, OUTPUT_FILE
    load_dotenv()
    weather_key = os.getenv('WEATHER_API_KEY', '')
    if not weather_key:
        raise Exception("OpenWeather API key not set")
    WEATHER_API_KEY = weather_key

    weather_base_url = os.getenv('WEATHER_API_BASE_URL', '')
    if not weather_base_url:
        raise Exception("OpenWeather API key not set")
    WEATHER_API_BASE_URL = weather_base_url

    weather_fallback_city = os.getenv('GEO_API_FALLBACK_CITY', '')
    if not weather_fallback_city:
        raise Exception("Fallback city not set")
    GEO_API_FALLBACK_CITY = weather_fallback_city

    geo_api_url = os.getenv("GEO_API_URL", "")
    if not geo_api_url:
        raise Exception("Geo API URL not set")
    GEO_API_URL = geo_api_url

    db_url = os.getenv("DB_URL", '')
    if not db_url:
        raise Exception("DB URL not set")
    DB_URL = db_url

    DB_USER = os.getenv("DB_USER", '')
    DB_PASSWORD = os.getenv("DB_PASSWORD", '')

    OUTPUT_FILE = os.getenv("OUTPUT_FILE", "weather_report.md")

    return create_db_and_tables(DB_URL)


def main():
    # Инициализация переменных окружения
    engine = setup()

    # Получение координат
    city, loc = get_ipinfo(GEO_API_URL)
    lat, lon = loc

    # Получение погоды
    weather, weather_city = get_weather(WEATHER_API_BASE_URL, WEATHER_API_KEY,
                                        GEO_API_FALLBACK_CITY, lat, lon)

    if city != weather_city and weather_city:
        city = weather_city

    # Сохранение в БД
    saved_count = save_forecast(engine, city, weather)
    print(f"Город: {city}")
    print(f"Сохранено новых записей: {saved_count}")

    # Выгрузка в Markdown
    total_records = export_to_markdown(engine, city, OUTPUT_FILE)
    print(f"Экспортировано записей: {total_records}")
    print(f"Файл отчёта: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
