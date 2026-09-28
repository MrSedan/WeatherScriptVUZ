from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db_model import WeatherForecast

HEADERS = ["Дата", "Мин. темп. (°C)", "Макс. темп. (°C)",
           "Описание", "Влажность (%)", "Ветер (м/с)"]

# Получить форматированную строку


def _row_to_cells(record: WeatherForecast) -> List[str]:
    return [
        record.forecast_date.isoformat(),
        f"{record.temp_min:.0f}",
        f"{record.temp_max:.0f}",
        record.description,
        f"{record.humidity:.0f}",
        f"{record.wind_speed:.1f}",
    ]

# Сделать из форматированной строки строку в таблице


def _format_table(rows: List[List[str]]) -> str:
    widths = [
        max(len(HEADERS[i]), *(len(row[i])
            for row in rows)) if rows else len(HEADERS[i])
        for i in range(len(HEADERS))
    ]

    def format_row(cells: List[str]) -> str:
        padded = (cell.ljust(width) for cell, width in zip(cells, widths))
        return "| " + " | ".join(padded) + " |"

    separator = "|" + "|".join("-" * (width + 2) for width in widths) + "|"

    lines = [format_row(HEADERS), separator]
    lines.extend(format_row(row) for row in rows)
    return "\n".join(lines)


def export_to_markdown(engine, city: str, output_path: str) -> int:
    with Session(engine) as session:
        records = session.execute(
            select(WeatherForecast)
            .where(WeatherForecast.city == city)
            .order_by(WeatherForecast.forecast_date)
        ).scalars().all()

    if records:
        period = f"{records[0].forecast_date.isoformat()} -- {records[-1].forecast_date.isoformat()}"
    else:
        period = "нет данных"

    lines = [
        "# Прогноз погоды",
        "",
        f"Автоматически определённая локация: {city}  ",
        f"Период: {period}  ",
        "",
        _format_table([_row_to_cells(record) for record in records]),
        "",
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return len(records)
