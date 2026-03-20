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


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
