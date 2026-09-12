export interface User {
  id: string;
  email: string;
  full_name?: string;
  created_at: string;
}

export interface Stock {
  ticker: string;
  name: string;
  sector?: string;
  industry?: string;
  market_cap?: number;
  current_price?: number;
  change_percent?: number;
  source?: string;
  is_mock?: boolean;
}

export interface StockHistory {
  ticker: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  source?: string;
  is_mock?: boolean;
}

export interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface PortfolioStock {
  id: string;
  portfolio_id: string;
  stock_ticker: string;
  quantity: number;
  avg_price: number;
  current_price?: number;
  invested_value: number;
  current_value?: number;
  pnl?: number;
  pnl_percent?: number;
  stock?: Stock;
}

export interface Watchlist {
  id: string;
  user_id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface WatchlistStock {
  id: string;
  watchlist_id: string;
  stock_ticker: string;
  added_at: string;
  notes?: string;
  stock?: Stock;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: {
    intent?: string;
    timeframe?: string;
    tickers?: string[];
    evidence?: string[];
    risks?: string[];
    conclusion?: string;
    is_mock_data?: boolean;
  };
}

export interface AIAnalysis {
  intent: string;
  timeframe: string;
  tickers: string[];
  analysis: string;
  evidence: string[];
  risks: string[];
  conclusion: string;
  confidence?: number;
  is_mock_data?: boolean;
}

export interface MarketOverview {
  indices: Array<{
    name: string;
    value: number;
    change: number;
    change_percent: number;
  }>;
  sectors: Array<{
    name: string;
    change_percent: number;
  }>;
  market_breadth?: {
    advances: number;
    declines: number;
    unchanged: number;
  };
}

export interface IPOInfo {
  company_name: string;
  issue_size: number;
  price_band_low: number;
  price_band_high: number;
  open_date: string;
  close_date: string;
  listing_date: string;
  fresh_issue: number;
  ofs: number;
  pe_ratio?: number;
  industry_pe?: number;
  subscription_status?: string;
}
