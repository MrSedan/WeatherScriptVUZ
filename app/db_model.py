from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import String, DateTime, Date, Float, create_engine, func, select
from sqlalchemy.exc import ArgumentError, IntegrityError, OperationalError, SQLAlchemyError
from datetime import date, datetime
from typing import Dict


class Base(DeclarativeBase):
    pass


class WeatherForecast(Base):
    __tablename__ = 'weather_forecast'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String())
    forecast_date: Mapped[date] = mapped_column(Date())
    temp_min: Mapped[float] = mapped_column(Float())
    temp_max: Mapped[float] = mapped_column(Float())
    humidity: Mapped[float] = mapped_column(Float())
    wind_speed: Mapped[float] = mapped_column(Float())
    description: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())


def save_forecast(engine, city: str, days: Dict[str, Dict]) -> int:
    saved = 0
    try:
        with Session(engine) as session:
            for day_str, values in days.items():
                forecast_date = date.fromisoformat(day_str)
                exists = session.execute(
                    select(WeatherForecast.id).where(
                        WeatherForecast.city == city,
                        WeatherForecast.forecast_date == forecast_date,
                    )
                ).first()
                if exists is not None:
                    continue
                session.add(WeatherForecast(
                    city=city,
                    forecast_date=forecast_date,
                    temp_min=values["min_temp"],
                    temp_max=values["max_temp"],
                    humidity=values["humidity"],
                    wind_speed=values["max_wind"],
                    description=values["description"],
                ))
                saved += 1
            session.commit()
    except IntegrityError as e:
        raise Exception(f"Нарушение целостности данных при сохранении прогноза: {e}")
    except OperationalError as e:
        raise Exception(f"Ошибка подключения к БД при сохранении прогноза: {e}")
    except SQLAlchemyError as e:
        raise Exception(f"Ошибка БД при сохранении прогноза: {e}")
    return saved


def create_db_and_tables(db_url):
    try:
        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(engine)
    except ArgumentError as e:
        raise Exception(f"Некорректный DB_URL: {e}")
    except OperationalError as e:
        raise Exception(f"Не удалось подключиться к БД: {e}")
    except SQLAlchemyError as e:
        raise Exception(f"Ошибка БД при создании таблиц: {e}")
    return engine
