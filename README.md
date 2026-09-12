# Market AI - Personal Market Intelligence Platform

Your personal AI-powered market research assistant for analyzing stocks, IPOs, portfolios, and market opportunities.

## Features

### AI Chat Interface
- Ask natural language questions about stocks, markets, IPOs
- Get evidence-based analysis with clear reasoning
- Support for multiple timeframes (intraday, swing, long-term)
- Transparent risk assessment and conclusions

### Portfolio Management
- Track your stock holdings
- Real-time P&L calculation
- Portfolio performance analytics
- Add/remove stocks easily

### Watchlists
- Create multiple watchlists (Long-term, Swing, IPO, etc.)
- Track stocks you're interested in
- Quick access to monitored stocks

### Market Dashboard
- Indian market indices (NIFTY, BANK NIFTY, SENSEX)
- Top gainers and losers
- Market breadth and sentiment
- AI-powered market insights

## Technology Stack

### Backend
- **Python** with FastAPI
- **PostgreSQL** for data storage
- **Redis** for caching
- **yfinance** for market data (free)
- Multi-source data fetching with fallbacks

### Frontend
- **React 19** with TypeScript
- **TailwindCSS** for styling
- **Zustand** for state management
- **React Query** for data fetching
- **Lucide React** for icons

### AI
- **Ollama** with Llama 3.2 (local, free)
- Intent classification for query understanding
- Evidence-based reasoning engine

## Zero-Cost Architecture

This platform is built to work with **zero recurring cost**:

✅ Free market data via yfinance (with mock fallback)  
✅ Local AI inference with Ollama  
✅ Open-source database (PostgreSQL)  
✅ Free caching (Redis)  
✅ No paid APIs required  

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- (Optional) Ollama for local AI

### Installation

1. **Start the platform:**
```bash
./start.sh
```

2. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Docker Services
```bash
docker-compose up -d
```

## Usage Examples

### AI Chat Questions
- "Analyze TCS for a 3-year investment"
- "Is this a good time for swing trading?"
- "What's happening in the Indian market today?"
- "Find fundamentally strong companies that have fallen"
- "Should I apply for this IPO?"
- "Analyze my portfolio risk"

### Portfolio Management
1. Go to Portfolio page
2. Click "Add Stock"
3. Enter symbol (e.g., RELIANCE.NS), quantity, and average price
4. View real-time P&L

### Watchlists
1. Go to Watchlist page
2. Create a new watchlist (e.g., "Long-term Investments")
3. Add stocks by symbol
4. Monitor your selected stocks

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

### Stocks
- `GET /api/v1/stocks/search?q=query` - Search stocks
- `GET /api/v1/stocks/{symbol}/quote` - Get stock quote
- `GET /api/v1/stocks/{symbol}/history` - Get historical data
- `GET /api/v1/stocks/{symbol}/details` - Get stock details

### Portfolio
- `GET /api/v1/portfolio` - Get holdings
- `POST /api/v1/portfolio/add` - Add stock
- `DELETE /api/v1/portfolio/remove/{id}` - Remove stock

### Watchlist
- `GET /api/v1/watchlist` - Get watchlists
- `POST /api/v1/watchlist/create` - Create watchlist
- `POST /api/v1/watchlist/{id}/add` - Add stock to watchlist
- `DELETE /api/v1/watchlist/{id}/remove/{stockId}` - Remove stock

### AI Chat
- `POST /api/v1/chat/analyze` - Analyze query

## Data Sources

### Free Tier (Default)
- **yfinance**: Daily stock prices, fundamentals
- **Mock Data**: Fallback when APIs are rate-limited
- **Local AI**: Ollama with Llama 3.2

### Upgrade Options (Paid)
- **Alpha Vantage**: More reliable API calls
- **Groq API**: Faster cloud-based AI inference
- **Premium News APIs**: Real-time news sentiment

## Limitations

⚠️ **Data Delays**: Free data may be delayed by 15 minutes  
⚠️ **Rate Limits**: yfinance has request limits (handled by caching)  
⚠️ **Mock Data**: System uses realistic mock data when APIs fail  
⚠️ **No Predictions**: AI provides analysis, not guaranteed predictions  

## Security

- JWT-based authentication
- Password hashing with bcrypt
- API key protection (never exposed in frontend)
- Secure database connections

## Roadmap

### Phase 1 (Current) ✅
- Basic AI chat interface
- Portfolio management
- Watchlist functionality
- Market dashboard
- Free data sources

### Phase 2 (Planned)
- IPO analysis module
- Advanced screening/scanning
- Alert system
- Research report generation

### Phase 3 (Future)
- Backtesting framework
- Advanced ML models
- Global market integration
- Mobile responsive design

## Disclaimer

This platform is for **educational and research purposes only**. 

- Not financial advice
- Do your own research before investing
- Past performance doesn't guarantee future results
- AI analysis is based on available data and has limitations

## License

MIT License - Free for personal use

## Support

For issues or questions, please check:
- API Documentation: http://localhost:8000/docs
- Backend logs: Check terminal output
- Frontend console: Browser DevTools
