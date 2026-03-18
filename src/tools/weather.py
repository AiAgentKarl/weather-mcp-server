"""Weather-Tools — Wetter, Vorhersagen, Luftqualität und Klima."""

from mcp.server.fastmcp import FastMCP

from src.clients.open_meteo import OpenMeteoClient

_client = OpenMeteoClient()

# WMO Wetter-Codes in lesbare Beschreibungen übersetzen
WMO_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
    82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


async def _resolve_location(location: str) -> tuple[float, float, str]:
    """Ort in Koordinaten auflösen. Gibt (lat, lon, display_name) zurück."""
    # Prüfen ob schon Koordinaten übergeben wurden (z.B. "48.8,2.3")
    if "," in location:
        parts = location.split(",")
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lat, lon, f"{lat}, {lon}"
        except ValueError:
            pass

    # Geocoding über Open-Meteo
    results = await _client.geocode(location, count=1)
    if not results:
        raise ValueError(f"Ort '{location}' nicht gefunden")

    r = results[0]
    name = r.get("name", location)
    country = r.get("country", "")
    admin1 = r.get("admin1", "")
    display = f"{name}, {admin1}, {country}" if admin1 else f"{name}, {country}"
    return r["latitude"], r["longitude"], display


def register_weather_tools(mcp: FastMCP):
    """Wetter-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def get_current_weather(location: str) -> dict:
        """Aktuelles Wetter für einen Ort abrufen.

        Gibt Temperatur, Luftfeuchtigkeit, Wind, Niederschlag und
        Wetterbedingungen zurück.

        Args:
            location: Ortsname (z.B. "Berlin", "Tokyo") oder Koordinaten ("48.8,2.3")
        """
        lat, lon, display = await _resolve_location(location)
        data = await _client.get_current_weather(lat, lon)
        current = data.get("current", {})

        weather_code = current.get("weather_code", 0)
        return {
            "location": display,
            "coordinates": {"latitude": lat, "longitude": lon},
            "timezone": data.get("timezone", ""),
            "temperature_c": current.get("temperature_2m"),
            "feels_like_c": current.get("apparent_temperature"),
            "humidity_pct": current.get("relative_humidity_2m"),
            "precipitation_mm": current.get("precipitation"),
            "rain_mm": current.get("rain"),
            "snowfall_cm": current.get("snowfall"),
            "cloud_cover_pct": current.get("cloud_cover"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_direction_deg": current.get("wind_direction_10m"),
            "wind_gusts_kmh": current.get("wind_gusts_10m"),
            "pressure_hpa": current.get("surface_pressure"),
            "is_day": current.get("is_day") == 1,
            "condition": WMO_CODES.get(weather_code, f"Code {weather_code}"),
            "weather_code": weather_code,
        }

    @mcp.tool()
    async def get_weather_forecast(location: str, days: int = 7) -> dict:
        """Wettervorhersage für einen Ort abrufen (bis zu 16 Tage).

        Gibt tägliche Vorhersage mit Min/Max-Temperatur, Niederschlag,
        Wind und UV-Index zurück.

        Args:
            location: Ortsname (z.B. "München") oder Koordinaten
            days: Anzahl Tage (Standard: 7, Maximum: 16)
        """
        lat, lon, display = await _resolve_location(location)
        data = await _client.get_forecast(lat, lon, days)
        daily = data.get("daily", {})

        dates = daily.get("time", [])
        forecast = []
        for i, date in enumerate(dates):
            weather_code = daily.get("weather_code", [0])[i] if i < len(daily.get("weather_code", [])) else 0
            forecast.append({
                "date": date,
                "temp_max_c": daily.get("temperature_2m_max", [None])[i],
                "temp_min_c": daily.get("temperature_2m_min", [None])[i],
                "feels_like_max_c": daily.get("apparent_temperature_max", [None])[i],
                "feels_like_min_c": daily.get("apparent_temperature_min", [None])[i],
                "precipitation_mm": daily.get("precipitation_sum", [None])[i],
                "rain_mm": daily.get("rain_sum", [None])[i],
                "snowfall_cm": daily.get("snowfall_sum", [None])[i],
                "precipitation_prob_pct": daily.get("precipitation_probability_max", [None])[i],
                "wind_max_kmh": daily.get("wind_speed_10m_max", [None])[i],
                "wind_gusts_max_kmh": daily.get("wind_gusts_10m_max", [None])[i],
                "uv_index_max": daily.get("uv_index_max", [None])[i],
                "sunrise": daily.get("sunrise", [None])[i],
                "sunset": daily.get("sunset", [None])[i],
                "condition": WMO_CODES.get(weather_code, f"Code {weather_code}"),
            })

        return {
            "location": display,
            "coordinates": {"latitude": lat, "longitude": lon},
            "timezone": data.get("timezone", ""),
            "forecast": forecast,
        }

    @mcp.tool()
    async def get_air_quality(location: str) -> dict:
        """Aktuelle Luftqualität für einen Ort abrufen.

        Gibt AQI (EU und US), Feinstaub, Ozon und andere
        Schadstoffwerte zurück.

        Args:
            location: Ortsname (z.B. "Stuttgart") oder Koordinaten
        """
        lat, lon, display = await _resolve_location(location)
        data = await _client.get_air_quality(lat, lon)
        current = data.get("current", {})

        eu_aqi = current.get("european_aqi", 0)
        us_aqi = current.get("us_aqi", 0)

        # AQI-Bewertung
        if eu_aqi <= 20:
            quality = "Good"
        elif eu_aqi <= 40:
            quality = "Fair"
        elif eu_aqi <= 60:
            quality = "Moderate"
        elif eu_aqi <= 80:
            quality = "Poor"
        elif eu_aqi <= 100:
            quality = "Very Poor"
        else:
            quality = "Extremely Poor"

        return {
            "location": display,
            "coordinates": {"latitude": lat, "longitude": lon},
            "european_aqi": eu_aqi,
            "us_aqi": us_aqi,
            "quality_label": quality,
            "pollutants": {
                "pm10_ugm3": current.get("pm10"),
                "pm2_5_ugm3": current.get("pm2_5"),
                "ozone_ugm3": current.get("ozone"),
                "nitrogen_dioxide_ugm3": current.get("nitrogen_dioxide"),
                "sulphur_dioxide_ugm3": current.get("sulphur_dioxide"),
                "carbon_monoxide_ugm3": current.get("carbon_monoxide"),
                "dust_ugm3": current.get("dust"),
            },
            "uv_index": current.get("uv_index"),
        }

    @mcp.tool()
    async def get_historical_weather(
        location: str, start_date: str, end_date: str
    ) -> dict:
        """Historische Wetterdaten für einen Zeitraum abrufen.

        Gibt tägliche Daten wie Temperatur, Niederschlag und Wind
        für vergangene Zeiträume zurück. Daten ab 1940 verfügbar.

        Args:
            location: Ortsname (z.B. "Hamburg") oder Koordinaten
            start_date: Startdatum im Format YYYY-MM-DD
            end_date: Enddatum im Format YYYY-MM-DD
        """
        lat, lon, display = await _resolve_location(location)
        data = await _client.get_historical_weather(lat, lon, start_date, end_date)
        daily = data.get("daily", {})

        dates = daily.get("time", [])
        history = []
        for i, date in enumerate(dates):
            weather_code = daily.get("weather_code", [0])[i] if i < len(daily.get("weather_code", [])) else 0
            history.append({
                "date": date,
                "temp_max_c": daily.get("temperature_2m_max", [None])[i],
                "temp_min_c": daily.get("temperature_2m_min", [None])[i],
                "temp_mean_c": daily.get("temperature_2m_mean", [None])[i],
                "precipitation_mm": daily.get("precipitation_sum", [None])[i],
                "rain_mm": daily.get("rain_sum", [None])[i],
                "snowfall_cm": daily.get("snowfall_sum", [None])[i],
                "wind_max_kmh": daily.get("wind_speed_10m_max", [None])[i],
                "condition": WMO_CODES.get(weather_code, f"Code {weather_code}"),
            })

        return {
            "location": display,
            "coordinates": {"latitude": lat, "longitude": lon},
            "period": {"start": start_date, "end": end_date},
            "daily_data": history,
        }

    @mcp.tool()
    async def get_marine_weather(location: str) -> dict:
        """Marine- und Ozean-Wetter für Küstenregionen abrufen.

        Gibt Wellenhöhe, Wellenrichtung, Strömungen und
        7-Tage-Marine-Vorhersage zurück.

        Args:
            location: Küstenort (z.B. "Sylt", "Marseille") oder Koordinaten
        """
        lat, lon, display = await _resolve_location(location)
        data = await _client.get_marine_weather(lat, lon)
        current = data.get("current", {})
        daily = data.get("daily", {})

        # Tägliche Marine-Vorhersage
        dates = daily.get("time", [])
        forecast = []
        for i, date in enumerate(dates):
            forecast.append({
                "date": date,
                "wave_height_max_m": daily.get("wave_height_max", [None])[i],
                "wave_direction_dominant_deg": daily.get("wave_direction_dominant", [None])[i],
                "wave_period_max_s": daily.get("wave_period_max", [None])[i],
                "wind_wave_height_max_m": daily.get("wind_wave_height_max", [None])[i],
                "swell_wave_height_max_m": daily.get("swell_wave_height_max", [None])[i],
            })

        return {
            "location": display,
            "coordinates": {"latitude": lat, "longitude": lon},
            "current": {
                "wave_height_m": current.get("wave_height"),
                "wave_direction_deg": current.get("wave_direction"),
                "wave_period_s": current.get("wave_period"),
                "wind_wave_height_m": current.get("wind_wave_height"),
                "swell_wave_height_m": current.get("swell_wave_height"),
                "ocean_current_velocity_ms": current.get("ocean_current_velocity"),
                "ocean_current_direction_deg": current.get("ocean_current_direction"),
            },
            "daily_forecast": forecast,
        }

    @mcp.tool()
    async def geocode_location(name: str, count: int = 5) -> dict:
        """Ortsname in Koordinaten umwandeln (Geocoding).

        Nützlich um Koordinaten für andere Tools zu erhalten
        oder um mehrdeutige Ortsnamen aufzulösen.

        Args:
            name: Ortsname (z.B. "Paris", "Springfield")
            count: Maximale Anzahl Ergebnisse (Standard: 5)
        """
        results = await _client.geocode(name, count)

        locations = []
        for r in results:
            locations.append({
                "name": r.get("name", ""),
                "country": r.get("country", ""),
                "country_code": r.get("country_code", ""),
                "admin1": r.get("admin1", ""),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
                "elevation_m": r.get("elevation"),
                "population": r.get("population"),
                "timezone": r.get("timezone", ""),
            })

        return {
            "query": name,
            "results_count": len(locations),
            "locations": locations,
        }
