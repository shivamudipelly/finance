# 🚀 ONE-COMMAND START - Market AI Platform

## Prerequisites
- Docker Desktop installed (includes Docker Compose)
- 4GB+ free disk space
- Internet connection (for downloading images & AI model)

## Start Everything (Single Command)

```bash
./start.sh
```

That's it! The script will:
1. ✅ Check Docker installation
2. ✅ Stop any existing containers
3. ✅ Download all required images (PostgreSQL, Redis, Ollama, Python, Node.js)
4. ✅ Pull the Llama 3.2 AI model (~2GB, first time only)
5. ✅ Start all 5 services
6. ✅ Display access URLs

## Access Your Platform

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | User interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI (test APIs) |

## Wait For...

On **first run**, wait 2-5 minutes for:
- Docker images to download (~500MB total)
- Llama 3.2 AI model to pull (~2GB)
- Services to initialize

**Sign it's ready:** Frontend shows "System Status: All Green"

## Common Commands

```bash
./start.sh          # Start everything
./stop.sh           # Stop everything
./logs.sh           # View all logs
./logs.sh backend   # View backend logs only
./logs.sh ollama    # View AI model loading progress

# Reset everything (delete all data)
docker compose down -v
./start.sh
```

## First Steps After Starting

1. **Open** http://localhost:3000
2. **Click** "Register" to create account
3. **Login** with your credentials
4. **Try** these questions in chat:
   - "Analyze RELIANCE for long-term investment"
   - "Is TCS good for swing trading?"
   - "What happened in the market today?"

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 3000 or 8000
lsof -i :3000
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### AI Not Responding
Wait longer on first run. Check progress:
```bash
./logs.sh ollama
```
Look for "Pulling llama3.2... complete"

### Market Data Shows "Mock"
Free APIs have rate limits. This is normal. System clearly indicates mock data.
For real data later: Add Alpha Vantage API key (free tier available).

### Want to Start Fresh
```bash
docker compose down -v  # Deletes ALL data
./start.sh              # Rebuilds everything
```

## What's Running

```
┌─────────────────────────────────────────┐
│  Frontend (React)                       │
│  Port: 3000                             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Backend (FastAPI)                      │
│  Port: 8000                             │
└──────┬─────────────┬─────────────┬──────┘
       │             │             │
┌──────▼──────┐ ┌────▼─────┐ ┌────▼────┐
│ PostgreSQL  │ │  Redis   │ │ Ollama  │
│   (DB)      │ │ (Cache)  │ │  (AI)   │
│ Port: 5432  │ │Port: 6379│ │Port:11434│
└─────────────┘ └──────────┘ └─────────┘
```

## Zero Cost Promise

✅ **100% Free Components:**
- React (Frontend) - Open Source
- FastAPI (Backend) - Open Source  
- PostgreSQL (Database) - Open Source
- Redis (Cache) - Open Source
- Ollama + Llama 3.2 (AI) - Free, runs locally
- yfinance (Market Data) - Free API

❌ **No Credit Card Required**
❌ **No API Keys Needed** (optional for upgrades)
❌ **No Subscription Fees**

## Next Phase (Optional Upgrades)

When you want better data/speed:
- Alpha Vantage Premium ($0-50/mo) - Better market data
- Groq API (Pay per use) - Faster AI responses
- TradingView API (Paid) - Real-time data

But **NOT REQUIRED** - platform works fully with free tier!

---

**Questions?** Check README.md for full documentation.

**Built for Indian investors, works globally.**
