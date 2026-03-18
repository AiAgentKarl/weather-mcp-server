"""Open-Meteo API Client — kostenlose globale Wetter- und Klimadaten."""

import httpx

from src.config import settings


class OpenMeteoClient:
    """Async-Client für alle Open-Meteo APIs."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.http_timeout)

    # --- Geocoding ---

    async def geocode(self, name: str, count: int = 5) -> list[dict]:
        """Ortsname in Koordinaten umwandeln."""
        url = f"{settings.geocoding_base_url}/search"
        params = {"name": name, "count": count, "language": "en", "format": "json"}
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])

    # --- Aktuelles Wetter ---

    async def get_current_weather(self, lat: float, lon: float) -> dict:
        """Aktuelles Wetter für Koordinaten abrufen."""
        url = f"{settings.weather_base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join([
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "precipitation", "rain", "snowfall", "cloud_cover",
                "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
                "weather_code", "surface_pressure", "is_day",
            ]),
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Vorhersage ---

    async def get_forecast(self, lat: float, lon: float, days: int = 7) -> dict:
        """Wettervorhersage für bis zu 16 Tage."""
        url = f"{settings.weather_base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ",".join([
                "temperature_2m_max", "temperature_2m_min",
                "apparent_temperature_max", "apparent_temperature_min",
                "precipitation_sum", "rain_sum", "snowfall_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max", "wind_gusts_10m_max",
                "weather_code", "sunrise", "sunset",
                "uv_index_max",
            ]),
            "forecast_days": min(days, 16),
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Stündliche Vorhersage ---

    async def get_hourly_forecast(self, lat: float, lon: float, hours: int = 24) -> dict:
        """Stündliche Vorhersage."""
        url = f"{settings.weather_base_url}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ",".join([
                "temperature_2m", "relative_humidity_2m", "precipitation_probability",
                "precipitation", "weather_code", "cloud_cover",
                "wind_speed_10m", "wind_direction_10m",
            ]),
            "forecast_hours": min(hours, 384),
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Luftqualität ---

    async def get_air_quality(self, lat: float, lon: float) -> dict:
        """Aktuelle Luftqualitätsdaten abrufen."""
        url = f"{settings.air_quality_base_url}/air-quality"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join([
                "european_aqi", "us_aqi",
                "pm10", "pm2_5", "carbon_monoxide",
                "nitrogen_dioxide", "sulphur_dioxide", "ozone",
                "dust", "uv_index",
            ]),
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Historisches Wetter ---

    async def get_historical_weather(
        self, lat: float, lon: float, start_date: str, end_date: str
    ) -> dict:
        """Historische Wetterdaten abrufen (Format: YYYY-MM-DD)."""
        url = f"{settings.archive_base_url}/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join([
                "temperature_2m_max", "temperature_2m_min",
                "temperature_2m_mean", "precipitation_sum",
                "rain_sum", "snowfall_sum",
                "wind_speed_10m_max",
                "weather_code",
            ]),
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Marine/Ozean-Wetter ---

    async def get_marine_weather(self, lat: float, lon: float) -> dict:
        """Marine- und Ozean-Wetterdaten abrufen."""
        url = f"{settings.marine_base_url}/marine"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ",".join([
                "wave_height", "wave_direction", "wave_period",
                "wind_wave_height", "wind_wave_direction",
                "swell_wave_height", "swell_wave_direction",
                "ocean_current_velocity", "ocean_current_direction",
            ]),
            "daily": ",".join([
                "wave_height_max", "wave_direction_dominant",
                "wave_period_max", "wind_wave_height_max",
                "swell_wave_height_max",
            ]),
            "forecast_days": 7,
            "timezone": "auto",
        }
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        """HTTP-Client schließen."""
        await self._client.aclose()
