from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def from_list(f: Callable[[Any], T], x: Any) -> list[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


@dataclass
class Coord:
    lat: float
    lon: float

    @staticmethod
    def from_dict(obj: Any) -> 'Coord':
        assert isinstance(obj, dict)
        lat = from_float(obj.get("lat"))
        lon = from_float(obj.get("lon"))
        return Coord(lat, lon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = to_float(self.lat)
        result["lon"] = to_float(self.lon)
        return result


@dataclass
class City:
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int

    @staticmethod
    def from_dict(obj: Any) -> 'City':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        coord = Coord.from_dict(obj.get("coord"))
        country = from_str(obj.get("country"))
        population = from_int(obj.get("population"))
        timezone = from_int(obj.get("timezone"))
        sunrise = from_int(obj.get("sunrise"))
        sunset = from_int(obj.get("sunset"))
        return City(id, name, coord, country, population, timezone, sunrise, sunset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["coord"] = to_class(Coord, self.coord)
        result["country"] = from_str(self.country)
        result["population"] = from_int(self.population)
        result["timezone"] = from_int(self.timezone)
        result["sunrise"] = from_int(self.sunrise)
        result["sunset"] = from_int(self.sunset)
        return result


@dataclass
class Clouds:
    all: int

    @staticmethod
    def from_dict(obj: Any) -> 'Clouds':
        assert isinstance(obj, dict)
        all = from_int(obj.get("all"))
        return Clouds(all)

    def to_dict(self) -> dict:
        result: dict = {}
        result["all"] = from_int(self.all)
        return result


@dataclass
class Rain:
    the_3_h: float

    @staticmethod
    def from_dict(obj: Any) -> 'Rain':
        assert isinstance(obj, dict)
        the_3_h = from_float(obj.get("3h"))
        return Rain(the_3_h)

    def to_dict(self) -> dict:
        result: dict = {}
        result["3h"] = to_float(self.the_3_h)
        return result


@dataclass
class Sys:
    pod: str

    @staticmethod
    def from_dict(obj: Any) -> 'Sys':
        assert isinstance(obj, dict)
        pod = from_str(obj.get("pod"))
        return Sys(pod)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pod"] = from_str(self.pod)
        return result


@dataclass
class WeatherElement:
    id: int
    main: str
    description: str
    icon: str

    @staticmethod
    def from_dict(obj: Any) -> 'WeatherElement':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        main = from_str(obj.get("main"))
        description = from_str(obj.get("description"))
        icon = from_str(obj.get("icon"))
        return WeatherElement(id, main, description, icon)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["main"] = from_str(self.main)
        result["description"] = from_str(self.description)
        result["icon"] = from_str(self.icon)
        return result


@dataclass
class Wind:
    speed: float
    deg: int
    gust: float

    @staticmethod
    def from_dict(obj: Any) -> 'Wind':
        assert isinstance(obj, dict)
        speed = from_float(obj.get("speed"))
        deg = from_int(obj.get("deg"))
        gust = from_float(obj.get("gust"))
        return Wind(speed, deg, gust)

    def to_dict(self) -> dict:
        result: dict = {}
        result["speed"] = to_float(self.speed)
        result["deg"] = from_int(self.deg)
        result["gust"] = to_float(self.gust)
        return result


@dataclass
class ListElement:
    dt: int
    main: dict[str, float]
    weather: list[WeatherElement]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    sys: Sys
    dt_txt: str
    rain: Rain | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'ListElement':
        assert isinstance(obj, dict)
        dt = from_int(obj.get("dt"))
        main = from_dict(from_float, obj.get("main"))
        weather = from_list(WeatherElement.from_dict, obj.get("weather"))
        clouds = Clouds.from_dict(obj.get("clouds"))
        wind = Wind.from_dict(obj.get("wind"))
        visibility = from_int(obj.get("visibility"))
        pop = from_float(obj.get("pop"))
        sys = Sys.from_dict(obj.get("sys"))
        dt_txt = from_str(obj.get("dt_txt"))
        rain = from_union([Rain.from_dict, from_none], obj.get("rain"))
        return ListElement(dt, main, weather, clouds, wind, visibility, pop, sys, dt_txt, rain)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dt"] = from_int(self.dt)
        result["main"] = from_dict(to_float, self.main)
        result["weather"] = from_list(
            lambda x: to_class(WeatherElement, x), self.weather)
        result["clouds"] = to_class(Clouds, self.clouds)
        result["wind"] = to_class(Wind, self.wind)
        result["visibility"] = from_int(self.visibility)
        result["pop"] = to_float(self.pop)
        result["sys"] = to_class(Sys, self.sys)
        result["dt_txt"] = from_str(self.dt_txt)
        if self.rain is not None:
            result["rain"] = from_union(
                [lambda x: to_class(Rain, x), from_none], self.rain)
        return result


@dataclass
class Weather:
    cod: int
    message: int
    cnt: int
    list: list[ListElement]
    city: City

    @staticmethod
    def from_dict(obj: Any) -> 'Weather':
        assert isinstance(obj, dict)
        cod = int(from_str(obj.get("cod")))
        message = from_int(obj.get("message"))
        cnt = from_int(obj.get("cnt"))
        list = from_list(ListElement.from_dict, obj.get("list"))
        city = City.from_dict(obj.get("city"))
        return Weather(cod, message, cnt, list, city)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cod"] = from_str(str(self.cod))
        result["message"] = from_int(self.message)
        result["cnt"] = from_int(self.cnt)
        result["list"] = from_list(
            lambda x: to_class(ListElement, x), self.list)
        result["city"] = to_class(City, self.city)
        return result


def weather_from_dict(s: Any) -> Weather:
    return Weather.from_dict(s)


def weather_to_dict(x: Weather) -> Any:
    return to_class(Weather, x)
