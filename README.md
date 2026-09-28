# Погода

Скрипт на Python: автоматически определяет местоположение по IP,
получает прогноз погоды на сегодня и ближайшие 3 дня из OpenWeatherMap,
агрегирует 3-часовые интервалы в дневные сводки, сохраняет их в SQLite и
выгружает результат в Markdown-отчёт.

**Технологии и API:**

- Python 3.13
- [requests](https://pypi.org/project/requests/) — HTTP-запросы к внешним API
- [SQLAlchemy](https://www.sqlalchemy.org/) (2.x, ORM) — хранение данных в SQLite
- [python-dotenv](https://pypi.org/project/python-dotenv/) — конфигурация через переменные окружения
- [ipinfo.io](https://ipinfo.io/json) — определение города и координат по IP
- [OpenWeatherMap](https://openweathermap.org/api/forecast5) — прогноз погоды (эндпоинт `forecast`)

## Установка

```bash
git clone https://github.com/MrSedan/WeatherScriptVUZ.git
cd lab1

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Настройка

1. Скопируйте шаблон конфигурации и заполните его своими значениями:

   ```bash
   cp .env.example .env
   ```

2. Зарегистрируйтесь на [openweathermap.org](https://openweathermap.org/api) и получите
   бесплатный API-ключ, затем укажите его в `WEATHER_API_KEY`.

3. Заполните остальные параметры в `.env`:

   | Переменная | Назначение |
   |---|---|
   | `WEATHER_API_KEY` | ключ OpenWeatherMap |
   | `WEATHER_API_BASE_URL` | базовый URL API погоды (`https://api.openweathermap.org`) |
   | `GEO_API_URL` | URL гео-API (`https://ipinfo.io/json`) |
   | `GEO_API_FALLBACK_CITY` | город по умолчанию, если гео-API недоступен |
   | `DB_URL` | строка подключения к БД (например, `sqlite:///db.db`) |
   | `DB_USER`, `DB_PASSWORD` | параметры подключения к БД (для SQLite не требуются) |
   | `OUTPUT_FILE` | путь к выходному Markdown-файлу |

## Запуск

```bash
python main.py
```

Скрипт определит город, получит прогноз, сохранит новые записи в БД и
выгрузит отчёт в Markdown-файл.

## Структура проекта

```
lab1/
├── main.py              # точка входа: конфигурация, оркестрация шагов, консольный отчёт
├── app/
│   ├── geo_locator.py   # определение города и координат через IP Geolocation API
│   ├── weather_client.py# запрос прогноза к OpenWeatherMap, группировка по дням и агрегация
│   ├── weather_dto.py   # dataclass-модели для разбора ответа OpenWeatherMap
│   ├── db_model.py      # SQLAlchemy-модель WeatherForecast, создание таблиц, сохранение без дублей
│   └── export.py        # выгрузка сохранённого прогноза из БД в Markdown-отчёт
├── requirements.txt
├── .env.example
└── .gitignore
```

## Пример вывода

Консоль:

```
Город: Kirov
Сохранено новых записей: 4
Экспортировано записей: 4
Файл отчёта: weather_report.md
```

Фрагмент `weather_report.md`:

```markdown
# Прогноз погоды

Автоматически определённая локация: Kirov
Период: 2026-09-28 -- 2026-10-01

| Дата       | Мин. темп. (°C) | Макс. темп. (°C) | Описание | Влажность (%) | Ветер (м/с) |
|------------|-----------------|------------------|----------|---------------|-------------|
| 2026-09-28 | 10              | 16               | пасмурно | 79            | 1.7         |
| 2026-09-29 | 9               | 17               | пасмурно | 81            | 2.4         |
```
