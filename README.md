# Market Intelligence Platform

A personal AI-powered market intelligence and decision-support web application.

## Overview

This platform serves as your personal AI market analyst, helping you:
- Analyze stocks across different time horizons (intraday, swing, positional, long-term)
- Research IPOs
- Monitor portfolios and watchlists
- Discover opportunities through intelligent scanning
- Understand market conditions with evidence-based analysis

## Architecture

```
Frontend (React + TypeScript) ←→ Backend (FastAPI/Python) ←→ PostgreSQL + Redis
                                          ↓
                                    AI Services (Ollama/Groq)
                                          ↓
                                    Market Data (yfinance)
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- Ollama (optional, for local LLM)

### Option 1: Using Docker Compose (Recommended)

1. **Start infrastructure services:**
```bash
docker-compose up -d postgres redis
```

2. **Copy environment file:**
```bash
cd backend
cp .env.example .env
# Edit .env with your settings
```

3. **Install dependencies and run backend:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access API docs:** http://localhost:8000/docs

### Option 2: Full Local Development

1. **Start databases:**
```bash
docker-compose up -d postgres redis
```

2. **Setup backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

3. **Setup frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Configuration

### Environment Variables

Key variables in `backend/.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/market_intelligence

# Security
SECRET_KEY=your-secret-key-min-32-characters

# LLM Settings
LLM_PROVIDER=ollama  # or "groq"
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Groq API (free tier available at https://console.groq.com)
GROQ_API_KEY=your-groq-api-key

# Data Sources
YFINANCE_ENABLED=true
```

### LLM Options

**Option 1: Ollama (Local, Free)**
```bash
# Install Ollama: https://ollama.ai
ollama pull llama3.2
```

**Option 2: Groq API (Free Tier)**
- Get API key: https://console.groq.com
- Add to `.env`: `GROQ_API_KEY=your-key`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Portfolio
- `POST /api/portfolio/portfolios` - Create portfolio
- `GET /api/portfolio/portfolios` - List portfolios
- `POST /api/portfolio/portfolios/{id}/holdings` - Add holding
- `GET /api/portfolio/portfolios/{id}/summary` - Portfolio summary

### Watchlist
- `POST /api/portfolio/watchlists` - Create watchlist
- `GET /api/portfolio/watchlists` - List watchlists
- `POST /api/portfolio/watchlists/{id}/items` - Add to watchlist

### Stocks
- `GET /api/stocks/search?q=query` - Search stocks
- `GET /api/stocks/{symbol}/quote` - Current quote
- `GET /api/stocks/{symbol}/fundamentals` - Fundamental data
- `GET /api/stocks/{symbol}/prices` - Historical prices

### AI Chat
- `POST /api/ai/chat` - Send message, get AI response
- `POST /api/ai/analyze` - Get detailed stock analysis
- `GET /api/ai/conversations` - List conversations

## Features

### MVP (Current)
✅ User authentication
✅ Portfolio management
✅ Watchlist management
✅ Stock data retrieval (via yfinance)
✅ AI chat interface
✅ Stock analysis with time-horizon awareness
✅ Conversation history

### Coming Soon
⏳ IPO analysis
⏳ Advanced scanning
⏳ Technical indicators dashboard
⏳ Alert system
⏳ News integration
⏳ Backtesting framework

## Data Sources

### Free Tier (Current)
- **yfinance**: Daily OHLCV data (15-min delayed)
- **Common Indian stocks**: Pre-configured list
- **Local LLM**: Ollama with Llama 3.2

### Limitations
- No real-time data (15-min minimum delay)
- Limited historical depth
- Basic fundamental data only
- No options/futures data

## Development

### Project Structure
```
/workspace
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/             # React app (to be implemented)
├── docs/
│   └── ARCHITECTURE.md   # Detailed architecture
├── docker-compose.yml
└── Dockerfile
```

### Running Tests
```bash
cd backend
pytest
```

### Code Quality
```bash
cd backend
ruff check .
black .
```

## Security Notes

1. **Change the default SECRET_KEY** in production
2. **Use HTTPS** in production (Let's Encrypt)
3. **Never commit .env files** to version control
4. **API keys** should be stored securely
5. **Rate limiting** is implemented for API protection

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart if needed
docker-compose restart postgres
```

### Ollama Connection Error
```bash
# Check if Ollama is running
ollama list

# Pull model if needed
ollama pull llama3.2
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Roadmap

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed roadmap including:
- Phase 1-7 development plan
- Technology decisions
- Risk assessment
- Upgrade paths for paid features

## License

MIT License - See LICENSE file for details

## Disclaimer

This application is for **educational and research purposes only**. 

- Not intended as registered investment advice
- Past performance does not guarantee future results
- Always do your own research before making investment decisions
- The AI may make mistakes - verify important information
