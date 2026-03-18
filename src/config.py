"""Konfiguration — Open-Meteo braucht keine API-Keys."""

from pydantic import BaseModel


class Settings(BaseModel):
    """Zentrale Konfiguration für Weather MCP Server."""

    # Open-Meteo APIs (alle kostenlos, kein Key nötig)
    weather_base_url: str = "https://api.open-meteo.com/v1"
    geocoding_base_url: str = "https://geocoding-api.open-meteo.com/v1"
    air_quality_base_url: str = "https://air-quality-api.open-meteo.com/v1"
    archive_base_url: str = "https://archive-api.open-meteo.com/v1"
    marine_base_url: str = "https://marine-api.open-meteo.com/v1"

    # HTTP-Client Defaults
    http_timeout: float = 30.0


# Globale Settings-Instanz
settings = Settings()
