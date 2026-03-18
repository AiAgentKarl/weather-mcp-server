# Weather MCP Server 🌤️

MCP Server for global weather, forecasts, air quality, and climate data. Powered by [Open-Meteo](https://open-meteo.com/) — **completely free, no API key required**.

## Features

- **Current Weather** — Temperature, humidity, wind, precipitation for any location
- **Forecasts** — Up to 16-day daily forecasts with precipitation probability
- **Air Quality** — EU/US AQI, PM2.5, PM10, ozone, NO₂ and more
- **Historical Weather** — Daily weather data going back to 1940
- **Marine Weather** — Wave height, swell, ocean currents for coastal areas
- **Geocoding** — Convert city names to coordinates

## Installation

```bash
pip install weather-mcp-server
```

## Usage with Claude Code

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": ["weather-mcp-server"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `get_current_weather` | Current weather conditions for any location |
| `get_weather_forecast` | Daily forecast up to 16 days |
| `get_air_quality` | Air quality index and pollutant levels |
| `get_historical_weather` | Historical daily weather data (since 1940) |
| `get_marine_weather` | Wave height, swell, ocean currents |
| `geocode_location` | Convert city names to coordinates |

## Examples

```
"What's the weather in Berlin?"
"Give me a 10-day forecast for Tokyo"
"How was the weather in New York on Christmas 2023?"
"What's the air quality in Beijing?"
"Wave conditions at Sylt for surfing?"
```

## Data Source

All data provided by [Open-Meteo](https://open-meteo.com/) — free for non-commercial use.

## License

MIT
