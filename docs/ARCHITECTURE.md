# Market Intelligence Platform - Architecture & Implementation Plan

## Executive Summary

This document outlines the architecture and implementation strategy for a **Personal AI Market Intelligence Platform** built with zero-cost technologies initially, with clear upgrade paths for future paid enhancements.

---

## 1. Product Understanding

### What This Is
A conversational AI-powered market research assistant that helps users:
- Analyze stocks across different time horizons (intraday, swing, positional, long-term)
- Research IPOs
- Monitor portfolios
- Discover opportunities through scanning
- Understand market conditions
- Make informed decisions with evidence-based analysis

### What This Is NOT
- A trading signal generator
- A prediction machine claiming guaranteed returns
- A replacement for human judgment

### Core Philosophy
**Evidence > Prediction**, **Transparency > Black Box**, **Flexibility > One-Size-Fits-All**

---

## 2. Complete Application Components

### Core Modules
1. **AI Conversation Engine** - Query understanding, context management, response generation
2. **Data Ingestion Layer** - Market data, fundamentals, news, IPO information
3. **Analysis Engine** - Technical indicators, fundamental ratios, valuation models
4. **ML Models** - Classification, ranking, anomaly detection, regime identification
5. **Portfolio Manager** - Holdings tracking, P&L, risk analysis
6. **Watchlist Manager** - Custom lists, alerts, monitoring
7. **Scanner/Ranker** - Opportunity discovery across universes
8. **Dashboard** - Market overview, portfolio summary, insights
9. **Alert System** - Meaningful event notifications
10. **Report Generator** - Structured research reports
11. **Backtesting Framework** - Strategy validation

### Supporting Infrastructure
- Database layer (relational + vector)
- Caching system
- Authentication & security
- API layer
- Frontend interface
- Background job scheduler

---

## 3. Technical Feasibility Assessment

### Highly Feasible (Free Resources Available)
✅ Daily OHLCV data (delayed 15-min or end-of-day)
✅ Basic company fundamentals
✅ Technical indicator calculations
✅ Portfolio tracking
✅ Watchlist management
✅ Conversational AI (local LLM or free-tier APIs)
✅ Vector search for semantic queries
✅ Dashboard with aggregated metrics

### Medium Feasibility (Limited Free Tiers)
⚠️ Real-time intraday data (requires paid subscription)
⚠️ Comprehensive news feeds (rate-limited on free tiers)
⚠️ Detailed IPO analytics (manual scraping required)
⚠️ Advanced options/futures data

### Challenging Without Payment
❌ True real-time market data
❌ Extensive historical intraday data
❌ Premium news sources (Bloomberg, Reuters)
❌ Analyst estimates and revisions
❌ Alternative data (satellite, credit card, web traffic)

---

## 4. Free Resource Limitations & Workarounds

| Resource | Free Limitation | Workaround | Paid Upgrade Benefit |
|----------|-----------------|------------|---------------------|
| Market Data | 15-min delay, daily only | Use for research, not trading | Real-time, intraday bars |
| LLM API | Rate limits (Groq free tier) | Local LLM fallback | Higher throughput, better models |
| News API | 100-500 calls/day | Cache aggressively, prioritize | Unlimited calls, more sources |
| Vector DB | Memory constraints | Disk-based storage | Cloud scaling |
| Hosting | Limited compute | Local development, free tiers | Dedicated servers |

---

## 5. Required Data Sources

### MVP Data Requirements
1. **Daily Price Data**: OHLCV for NSE/BSE stocks
2. **Index Data**: NIFTY, SENSEX, sectoral indices
3. **Basic Fundamentals**: Market cap, P/E, EPS, book value
4. **Corporate Actions**: Splits, dividends, bonuses
5. **User Data**: Portfolio holdings, watchlists

### Extended Data (Phase 2+)
6. **Quarterly Results**: Revenue, profit, margins
7. **Balance Sheet Items**: Debt, equity, cash flows
8. **IPO Information**: Issue details, financials, valuation
9. **News/Sentiment**: Company announcements, market news
10. **Macro Indicators**: Interest rates, inflation, currency

### Recommended Free Data Sources
- **yfinance**: Yahoo Finance API (unofficial but reliable)
- **NSEPy**: Historical NSE data (Python library)
- **Alpha Vantage**: Free tier (5 calls/min, 500/day)
- **Tiingo**: Free tier available
- **Screener.in**: Manual export for Indian stocks
- **Company Websites**: Annual reports, presentations

---

## 6. AI Capabilities - What's Actually Useful

### High Value Applications
🎯 **Query Understanding**: Classify intent (IPO analysis vs swing trade vs long-term)
🎯 **Context Management**: Remember previous conversations about specific stocks
🎯 **Report Generation**: Structure analysis into readable formats
🎯 **Evidence Synthesis**: Combine multiple data sources into coherent narrative
🎯 **Uncertainty Communication**: Express confidence levels appropriately

### Medium Value Applications
🔶 **Sentiment Analysis**: News tone classification
🔶 **Anomaly Detection**: Unusual volume, price movements
🔶 **Regime Classification**: Bull/bear/sideways market identification
🔶 **Stock Ranking**: Multi-factor scoring for scanners

### Low Value / Overhyped
❌ **Price Prediction**: Deep learning for next-day returns (poor signal-to-noise)
❌ **Automated Trading**: ML-generated trade signals without human oversight
❌ **Complex Pattern Recognition**: CNN for chart patterns (marginal edge)

### Recommended Approach
Use **simple statistical models** where possible, reserve **LLMs for language tasks**, avoid **over-engineering predictions**.

---

## 7. Recommended Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Chat UI     │ │ Dashboard   │ │ Portfolio   │            │
│  │ Interface   │ │ Views       │ │ Management  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   API GATEWAY (FastAPI)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Auth        │ │ Rate Limit  │ │ Request     │            │
│  │ Middleware  │ │ Middleware  │ │ Validation  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ AI Service    │   │ Data Service  │   │ User Service  │
│               │   │               │   │               │
│ - Intent      │   │ - Market Data │   │ - Portfolio   │
│ - Context     │   │ - Fundamentals│   │ - Watchlist   │
│ - Generation  │   │ - Indicators  │   │ - Alerts      │
│ - Reasoning   │   │ - Scanning    │   │ - Preferences │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ LLM Backend   │   │ PostgreSQL    │   │ ChromaDB      │
│ (Ollama/      │   │               │   │ (Vector Store)│
│  Groq API)    │   │ - Users       │   │               │
│               │   │ - Holdings    │   │ - Embeddings  │
│               │   │ - Watchlists  │   │ - Semantic    │
│               │   │ - Prices      │   │   Search      │
│               │   │ - Fundamentals│   │               │
└───────────────┘   └───────────────┘   └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │ Redis Cache   │
                    │               │
                    │ - API Rates   │
                    │ - Session     │
                    │ - Computed    │
                    │   Metrics     │
                    └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │ External APIs │
                    │               │
                    │ - yfinance    │
                    │ - AlphaVantage│
                    │ - News APIs   │
                    └───────────────┘
```

### Architecture Principles
1. **Modularity**: Each service independently testable and replaceable
2. **Separation of Concerns**: Clear boundaries between AI, data, and user logic
3. **Caching First**: Minimize external API calls with aggressive caching
4. **Async Where Possible**: Non-blocking I/O for data fetching
5. **Graceful Degradation**: System works even if one component fails

---

## 8. Technology Stack Recommendations

### Frontend
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | React 18 + TypeScript | Type safety, large ecosystem, component reusability |
| Styling | TailwindCSS | Rapid prototyping, utility-first, no CSS files |
| State | Zustand | Simpler than Redux, sufficient for this scale |
| Charts | Recharts | React-native, good enough for MVP |
| HTTP Client | TanStack Query | Caching, retries, background refetch |
| Build Tool | Vite | Fast HMR, modern bundling |

### Backend
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Framework | FastAPI | Async support, auto docs, type hints |
| Language | Python 3.11+ | ML ecosystem, data libraries |
| ORM | SQLAlchemy + Alembic | Mature, migrations, async support |
| Validation | Pydantic | Built into FastAPI, type validation |
| Auth | JWT + bcrypt | Stateless, secure password hashing |

### Database
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Primary DB | PostgreSQL | Relational data, JSON support, free |
| Vector DB | ChromaDB | Lightweight, embeddable, no server needed |
| Cache | Redis | Fast key-value, pub/sub for alerts |

### AI/ML
| Component | Technology | Rationale |
|-----------|------------|-----------|
| LLM Runtime | Ollama | Local execution, free, multiple model support |
| LLM API Fallback | Groq | Free tier, fast inference, Llama models |
| Embeddings | sentence-transformers | Local, fast, good quality |
| ML Library | scikit-learn | Simple models, well-documented |
| Numerical | NumPy + pandas | Standard data manipulation |

### Infrastructure
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Containerization | Docker | Reproducible environments |
| Orchestration | Docker Compose | Local development, simple deployment |
| Task Queue | Celery + Redis | Background jobs for data updates |
| Monitoring | Prometheus + Grafana | Free, self-hosted metrics |

### Development Tools
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Testing | pytest + pytest-asyncio | Python standard, async support |
| Linting | ruff + black | Fast, modern Python tooling |
| Type Checking | mypy | Catch type errors early |
| Git Hooks | pre-commit | Enforce code quality |

---

## 9. Minimum Viable Product (MVP)

### Must-Have Features
1. ✅ User authentication (register/login)
2. ✅ AI chat interface with query understanding
3. ✅ Stock lookup with basic data display
4. ✅ Portfolio creation and management
5. ✅ Watchlist creation and monitoring
6. ✅ Daily price data integration
7. ✅ Basic fundamental data
8. ✅ Technical indicators (MA, RSI, MACD)
9. ✅ Simple dashboard with market overview
10. ✅ Evidence-based response generation
11. ✅ Time-horizon aware analysis
12. ✅ Local LLM integration (Ollama)

### MVP Success Criteria
- User can ask "Analyze RELIANCE for long-term investment" and get structured response
- User can create portfolio and see P&L
- User can create watchlist and see price changes
- System distinguishes between intraday vs long-term queries
- All data is clearly labeled (delayed, EOD, etc.)
- Zero recurring cost to operate

### MVP Out of Scope
- Real-time data
- IPO analysis
- Advanced scanning
- Backtesting interface
- Mobile app
- Alerts system
- News integration

---

## 10. Phased Development Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Project setup and architecture
- Database schema design
- User authentication
- Basic data ingestion (yfinance)
- Simple stock lookup API
- Frontend skeleton

### Phase 2: AI Core (Weeks 5-8)
- LLM integration (Ollama + Groq fallback)
- Query intent classification
- Context management
- Response generation templates
- Evidence synthesis logic
- Chat interface

### Phase 3: Portfolio & Watchlist (Weeks 9-12)
- Portfolio CRUD operations
- Watchlist management
- P&L calculations
- Basic risk metrics
- Dashboard views
- Data refresh jobs

### Phase 4: Analysis Engine (Weeks 13-16)
- Technical indicators library
- Fundamental ratio calculations
- Valuation models
- Multi-timeframe analysis
- Report generation
- Explainability features

### Phase 5: Scanner & Discovery (Weeks 17-20)
- Stock screening logic
- Ranking algorithms
- Opportunity detection
- Filter customization
- Results presentation

### Phase 6: IPO & Extended Features (Weeks 21-24)
- IPO data collection
- IPO analysis framework
- News integration
- Sentiment analysis
- Alert system
- Advanced dashboard

### Phase 7: Polish & Scale (Weeks 25-28)
- Performance optimization
- Caching improvements
- Error handling
- User feedback integration
- Documentation
- Deployment automation

---

## 11. Major Risks & Limitations

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| yfinance API breaks | Medium | High | Multiple data source fallbacks |
| LLM hallucinates data | High | Medium | Strict grounding, cite sources |
| Rate limits exceeded | Medium | Medium | Aggressive caching, queue system |
| Local LLM too slow | Medium | Medium | Groq API fallback, smaller models |
| Database performance | Low | Medium | Indexing, query optimization |

### Business/Usage Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| User misinterprets advice | Medium | High | Clear disclaimers, uncertainty communication |
| Regulatory concerns | Low | High | Not providing registered investment advice |
| Data privacy breach | Low | High | Encryption, minimal data collection |
| Feature creep | High | Medium | Strict MVP scope, phased approach |

### Data Quality Issues
- **Delayed Data**: Clearly label all timestamps
- **Missing Fundamentals**: Show "data unavailable" rather than guess
- **Corporate Actions**: Adjust historical prices properly
- **Survivorship Bias**: Acknowledge delisted companies missing

### Known Limitations (Free Tier)
1. No real-time data (15-min minimum delay)
2. Limited historical depth (varies by source)
3. No options/futures data
4. Basic news coverage only
5. Single-user focus initially
6. Manual IPO data entry

---

## 12. Complexity Estimation

### Development Effort (Single Developer)
| Component | Estimated Days | Complexity |
|-----------|---------------|------------|
| Backend Setup | 3 | Low |
| Frontend Setup | 3 | Low |
| Database Design | 2 | Medium |
| Authentication | 2 | Low |
| Data Ingestion | 5 | Medium |
| AI Integration | 7 | High |
| Portfolio Module | 4 | Medium |
| Watchlist Module | 3 | Low |
| Analysis Engine | 6 | High |
| Dashboard | 5 | Medium |
| Scanner | 5 | High |
| Testing | 5 | Medium |
| Documentation | 3 | Low |
| **Total MVP** | **~53 days** | |

### With Two Developers
- Parallel development possible
- Estimated: 30-35 days for MVP

### Ongoing Maintenance
- Data pipeline monitoring: 2-4 hours/week
- Bug fixes: Variable
- Feature updates: Based on roadmap

---

## 13. Final Proposed System Architecture

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Chat       │  │  Dashboard   │  │  Portfolio   │          │
│  │   Screen     │  │   Overview   │  │  Management  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Watchlist   │  │   Scanner    │  │   Reports    │          │
│  │   Viewer     │  │   Results    │  │   Viewer     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REACT FRONTEND                              │
│  - Component Library                                             │
│  - State Management (Zustand)                                    │
│  - API Client (TanStack Query)                                   │
│  - Chart Components (Recharts)                                   │
│  - Authentication Context                                        │
└─────────────────────────────────────────────────────────────────┘
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    ROUTERS                                │   │
│  │  /auth  /stocks  /portfolio  /watchlist  /ai  /scan      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SERVICES LAYER                           │   │
│  │  AuthService  StockService  PortfolioService              │   │
│  │  AIService  ScanService  AnalysisService                  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 ANALYSIS ENGINE                           │   │
│  │  - Technical Indicators  - Fundamental Ratios             │   │
│  │  - Valuation Models      - Scoring Algorithms             │   │
│  │  - Time-horizon Logic    - Risk Metrics                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   AI ORCHESTRATOR                         │   │
│  │  - Intent Classification  - Context Management            │   │
│  │  - Prompt Engineering     - Response Synthesis            │   │
│  │  - Evidence Grounding     - Uncertainty Calibration       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  DATA FETCHERS                            │   │
│  │  - yfinance  - AlphaVantage  - NSEPy  - Web Scrapers     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  PostgreSQL   │   │   ChromaDB    │   │    Redis      │
│               │   │               │   │               │
│  - users      │   │  - embeddings │   │  - cache      │
│  - sessions   │   │  - documents  │   │  - sessions   │
│  - portfolios │   │  - vectors    │   │  - rate limit │
│  - watchlists │   │               │   │  - pub/sub    │
│  - prices     │   │               │   │               │
│  - fundamentals│  │               │   │               │
│  - corporate_actions│              │   │               │
└───────────────┘   └───────────────┘   └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │  LLM Backend  │
                    │               │
                    │  ┌─────────┐  │
                    │  │ Ollama  │  │◄── Local (Free)
                    │  │(Llama 3)│  │
                    │  └─────────┘  │
                    │       OR      │
                    │  ┌─────────┐  │
                    │  │ Groq    │  │◄── API (Free Tier)
                    │  │  API    │  │
                    │  └─────────┘  │
                    └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │ External Data │
                    │               │
                    │  - yfinance   │
                    │  - NSEPy      │
                    │  - Screener   │
                    │  - News APIs  │
                    └───────────────┘
```

### Data Flow Examples

#### Example 1: Stock Analysis Query
```
User: "Analyze TCS for 3-year investment"
    │
    ▼
Frontend sends POST /api/ai/chat {message: "..."}
    │
    ▼
Backend AIService receives request
    │
    ├─► IntentClassifier → "LONG_TERM_ANALYSIS"
    │
    ├─► EntityExtractor → {"stock": "TCS", "horizon": "3Y"}
    │
    ├─► ContextManager → Retrieve previous TCS discussions
    │
    ├─► DataFetcher → Get TCS fundamentals, prices, ratios
    │
    ├─► AnalysisEngine → Calculate growth, valuation, quality scores
    │
    ├─► LLM Orchestrator → Build prompt with evidence
    │       │
    │       ├─► Ollama/Groq → Generate response
    │       │
    │       ▼
    │   Structured response with sections:
    │   - Business Overview
    │   - Financial Performance
    │   - Valuation Assessment
    │   - Growth Drivers
    │   - Risks
    │   - Conclusion (with confidence level)
    │
    ▼
Response cached in Redis
    │
    ▼
Frontend displays formatted analysis
```

#### Example 2: Portfolio Update
```
User adds holding: "RELIANCE, 50 shares @ ₹2400"
    │
    ▼
Frontend sends POST /api/portfolio/holdings
    │
    ▼
Backend validates user auth
    │
    ▼
PortfolioService creates holding record
    │
    ├─► Fetches current price from cache/API
    │
    ├─► Calculates current value, P&L
    │
    ├─► Updates portfolio totals
    │
    ├─► Triggers background job for detailed analysis
    │
    ▼
Response with updated portfolio summary
    │
    ▼
Frontend updates portfolio view
```

### Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. TRANSPORT SECURITY                                      │
│     - HTTPS everywhere (Let's Encrypt for production)       │
│     - TLS 1.3 minimum                                       │
│     - HSTS headers                                          │
│                                                             │
│  2. AUTHENTICATION                                          │
│     - JWT tokens (short-lived access + refresh tokens)      │
│     - bcrypt password hashing (cost factor 12)              │
│     - Rate limiting on auth endpoints                       │
│     - Account lockout after failed attempts                 │
│                                                             │
│  3. AUTHORIZATION                                           │
│     - Role-based access control (user/admin)                │
│     - Resource ownership validation                         │
│     - SQL injection prevention (ORM parameterization)       │
│                                                             │
│  4. DATA PROTECTION                                         │
│     - Passwords never stored in plaintext                   │
│     - API keys in environment variables                     │
│     - Sensitive data encrypted at rest (optional)           │
│     - CORS properly configured                              │
│                                                             │
│  5. INPUT VALIDATION                                        │
│     - Pydantic models for all inputs                        │
│     - XSS prevention (React escapes by default)             │
│     - CSRF protection                                       │
│     - File upload restrictions                              │
│                                                             │
│  6. RATE LIMITING                                           │
│     - Per-endpoint limits via Redis                         │
│     - User-based quotas                                     │
│     - IP-based fallback                                     │
│                                                             │
│  7. LOGGING & MONITORING                                    │
│     - Audit logs for sensitive actions                      │
│     - No sensitive data in logs                             │
│     - Anomaly detection for unusual access                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema (Core Tables)

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Portfolios
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) DEFAULT 'Main Portfolio',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Holdings
CREATE TABLE holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES portfolios(id),
    symbol VARCHAR(50) NOT NULL,
    quantity DECIMAL NOT NULL,
    avg_price DECIMAL NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Watchlists
CREATE TABLE watchlists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Watchlist Items
CREATE TABLE watchlist_items (
    watchlist_id UUID REFERENCES watchlists(id),
    symbol VARCHAR(50) NOT NULL,
    added_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    PRIMARY KEY (watchlist_id, symbol)
);

-- Daily Prices
CREATE TABLE daily_prices (
    symbol VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL,
    high DECIMAL,
    low DECIMAL,
    close DECIMAL,
    volume BIGINT,
    adjusted_close DECIMAL,
    PRIMARY KEY (symbol, date)
);

-- Fundamentals (snapshot per quarter)
CREATE TABLE fundamentals (
    symbol VARCHAR(50) NOT NULL,
    report_date DATE NOT NULL,
    filing_date DATE,
    revenue DECIMAL,
    net_income DECIMAL,
    eps DECIMAL,
    book_value DECIMAL,
    total_debt DECIMAL,
    cash_and_equivalents DECIMAL,
    operating_cash_flow DECIMAL,
    shares_outstanding BIGINT,
    PRIMARY KEY (symbol, report_date)
);

-- Conversation History
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    metadata JSONB, -- Store intent, entities, sources
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_holdings_portfolio ON holdings(portfolio_id);
CREATE INDEX idx_watchlist_items_user ON watchlists(user_id);
CREATE INDEX idx_daily_prices_symbol_date ON daily_prices(symbol, date DESC);
CREATE INDEX idx_fundamentals_symbol_date ON fundamentals(symbol, report_date DESC);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
```

---

## Next Steps

With this architecture approved, I will proceed to implement the MVP following this plan:

1. **Initialize project structure** with all directories
2. **Set up backend** with FastAPI, database models, and authentication
3. **Implement data fetchers** using yfinance and NSEPy
4. **Build AI service** with Ollama integration and Groq fallback
5. **Create frontend** with React, chat interface, and dashboard
6. **Integrate components** and test end-to-end flows
7. **Add documentation** and deployment scripts

Shall I begin implementation?
