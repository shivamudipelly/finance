# 🚀 Market AI Platform - Personal Intelligence System

**One-Command Setup • Zero Cost • Fully Private**

## Quick Start (Single Command)

```bash
./start.sh
```

That's it! Open http://localhost:3000 in your browser.

## What You Get

| Component | Technology | Cost |
|-----------|------------|------|
| Frontend | React 19 + TypeScript | Free |
| Backend | FastAPI + Python | Free |
| Database | PostgreSQL | Free |
| Cache | Redis | Free |
| AI Engine | Ollama + Llama 3.2 | Free (runs locally) |
| Market Data | yfinance + fallbacks | Free |

## Features

### AI Chat Interface
- Ask anything about stocks, IPOs, markets
- Evidence-based analysis (not predictions)
- Multi-timeframe awareness (intraday to long-term)
- Understands intent: swing trading vs investing

### Portfolio Management
- Track your holdings
- P&L calculation
- Risk analysis
- Concentration warnings

### Watchlists
- Multiple watchlists (Long-term, Swing, IPO)
- Real-time monitoring
- Alert triggers

### Market Dashboard
- Index overview
- Top gainers/losers
- Market breadth
- AI insights

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│    Backend   │────▶│   Ollama    │
│  (React)    │     │  (FastAPI)   │     │  (Llama 3)  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐  ┌────────┐  ┌──────────┐
         │ Postgres│  │ Redis  │  │ yfinance │
         │  (DB)   │  │(Cache) │  │ (Data)   │
         └────────┘  └────────┘  └──────────┘
```

## Commands

| Command | Description |
|---------|-------------|
| `./start.sh` | Start everything |
| `./stop.sh` | Stop all services |
| `./logs.sh` | View all logs |
| `./logs.sh backend` | View backend logs only |
| `docker compose down -v` | Reset ALL data |

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432 (user/password)
- **Redis**: localhost:6379

## First Run Notes

1. **AI Model Download**: On first start, Ollama downloads Llama 3.2 (~2GB). Takes 2-5 minutes.
2. **Market Data**: Uses free APIs. If rate-limited, falls back to realistic mock data (clearly indicated).
3. **Persistence**: All data stored in Docker volumes (survives restarts).

## Example Usage

### Register & Login
1. Open http://localhost:3000
2. Click "Register"
3. Create account (any email/password)
4. Login

### Ask AI Questions
Try these in the chat:
- "Analyze RELIANCE for long-term investment"
- "Is TCS good for swing trading this week?"
- "What happened in the market today?"
- "Compare HDFC Bank and ICICI Bank"
- "Find fundamentally strong companies that fell recently"

### Add Portfolio
1. Go to Portfolio tab
2. Add stock: Symbol, Quantity, Avg Price
3. View P&L and analysis

### Create Watchlist
1. Go to Watchlist tab
2. Create new watchlist
3. Add stocks to monitor

## Troubleshooting

### Port Already in Use
If port 3000 or 8000 is busy:
```bash
# Check what's using the port
lsof -i :3000
# Kill the process or change port in docker-compose.yml
```

### AI Not Responding
Wait 2-5 minutes on first run for model download. Check logs:
```bash
./logs.sh ollama
```

### Market Data Issues
Free APIs have rate limits. System uses mock data as fallback (clearly marked). For better data:
- Add Alpha Vantage API key (free tier)
- Wait for rate limit reset (1 minute)

### Reset Everything
```bash
docker compose down -v
./start.sh
```

## Limitations (Free Tier)

| Feature | Free | Paid Upgrade |
|---------|------|--------------|
| Market Data | Delayed/Mock | Real-time |
| Intraday Data | Limited | Full access |
| News API | Basic | Comprehensive |
| AI Speed | Local (slower) | Cloud API (fast) |
| Rate Limits | Yes | Higher limits |

## Security Notes

- Default password: Change in production
- API keys: Store in `.env` file (not committed)
- HTTPS: Add reverse proxy for production
- Authentication: JWT tokens (30 min expiry)

## Development

### Modify Backend
Edit files in `/workspace/backend/` - auto-reloads

### Modify Frontend
Edit files in `/workspace/frontend/` - auto-reloads

### View Logs
```bash
./logs.sh backend
./logs.sh frontend
```

## Future Upgrades (Optional)

When you want to invest money:

1. **Better Data**: Alpha Vantage Premium ($50/mo)
2. **Faster AI**: Groq API ($0.10/million tokens)
3. **Real-time**: TradingView API (paid)
4. **News**: NewsAPI Pro ($50/mo)
5. **IPO Data**: Chittorgarh/Prime Database (paid)

## Philosophy

This is NOT a buy/sell signal machine. It's a **research assistant** that:
- Gathers evidence
- Shows multiple perspectives
- Highlights risks
- Never claims certainty
- Helps YOU make decisions

## License

MIT License - Build your own version!

---

**Built with ❤️ for independent investors**
