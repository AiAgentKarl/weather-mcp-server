"""Weather MCP Server — Globale Wetter-, Vorhersage- und Klimadaten."""

from mcp.server.fastmcp import FastMCP

from src.tools.weather import register_weather_tools

mcp = FastMCP(
    "Weather MCP Server",
    instructions=(
        "Provides global weather data, forecasts, air quality, "
        "historical weather, and marine conditions via Open-Meteo. "
        "All data is free and requires no API keys."
    ),
)

register_weather_tools(mcp)


def main():
    """Server starten."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
