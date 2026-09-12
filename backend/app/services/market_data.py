"""
Data fetching service for market data.
Uses yfinance as primary free data source.
"""
import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.schemas.schemas import DailyPriceResponse, StockQuote, StockFundamentals


class MarketDataService:
    """Service for fetching market data from external sources."""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl: int = 300  # 5 minutes for quotes
    
    def _get_yfinance_symbol(self, symbol: str, exchange: str = "NS") -> str:
        """Convert symbol to yfinance format with exchange suffix."""
        # For Indian stocks: RELIANCE -> RELIANCE.NS
        # For US stocks: AAPL stays AAPL
        if not any(c in symbol for c in ['.', ':']):
            return f"{symbol}.{exchange}"
        return symbol
    
    async def get_historical_prices(
        self, 
        symbol: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period: str = "1y"
    ) -> List[DailyPriceResponse]:
        """Fetch historical daily prices."""
        yf_symbol = self._get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            
            if start_date and end_date:
                df = ticker.history(start=start_date, end=end_date)
            else:
                df = ticker.history(period=period)
            
            if df.empty:
                return []
            
            prices = []
            for date, row in df.iterrows():
                prices.append(DailyPriceResponse(
                    symbol=symbol,
                    date=date.date(),
                    open=float(row.get('Open', 0)) if pd.notna(row.get('Open')) else None,
                    high=float(row.get('High', 0)) if pd.notna(row.get('High')) else None,
                    low=float(row.get('Low', 0)) if pd.notna(row.get('Low')) else None,
                    close=float(row.get('Close', 0)) if pd.notna(row.get('Close')) else None,
                    volume=int(row.get('Volume', 0)) if pd.notna(row.get('Volume')) else None,
                    adjusted_close=float(row.get('Close', 0)) if pd.notna(row.get('Close')) else None
                ))
            
            return prices
            
        except Exception as e:
            print(f"Error fetching historical prices for {symbol}: {e}")
            return []
    
    async def get_current_quote(self, symbol: str) -> Optional[StockQuote]:
        """Fetch current stock quote (delayed)."""
        yf_symbol = self._get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.fast_info
            
            if not info or 'lastPrice' not in dir(info):
                # Fallback to history
                hist = ticker.history(period='1d')
                if hist.empty:
                    return None
                last_price = float(hist['Close'].iloc[-1])
            else:
                last_price = float(info.lastPrice)
            
            # Get previous close for change calculation
            hist = ticker.history(period='2d')
            prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else last_price
            change = last_price - prev_close
            change_percent = (change / prev_close * 100) if prev_close else 0
            
            return StockQuote(
                symbol=symbol,
                price=last_price,
                change=round(change, 2),
                change_percent=round(change_percent, 2),
                volume=int(hist['Volume'].iloc[-1]) if not hist.empty else None,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return None
    
    async def get_fundamentals(self, symbol: str) -> Optional[StockFundamentals]:
        """Fetch fundamental data for a stock."""
        yf_symbol = self._get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            if not info:
                return None
            
            return StockFundamentals(
                symbol=symbol,
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE') or info.get('forwardPE'),
                eps=info.get('trailingEps'),
                book_value=info.get('bookValue'),
                debt_to_equity=info.get('debtToEquity'),
                roe=info.get('returnOnEquity'),
                revenue_growth=info.get('revenueGrowth'),
                profit_margin=info.get('profitMargins')
            )
            
        except Exception as e:
            print(f"Error fetching fundamentals for {symbol}: {e}")
            return None
    
    async def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get basic company information."""
        yf_symbol = self._get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            if not info:
                return None
            
            return {
                'symbol': symbol,
                'name': info.get('shortName') or info.get('longName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'description': info.get('longBusinessSummary'),
                'website': info.get('website'),
                'country': info.get('country'),
                'employees': info.get('fullTimeEmployees')
            }
            
        except Exception as e:
            print(f"Error fetching company info for {symbol}: {e}")
            return None
    
    async def search_stocks(self, query: str) -> List[Dict[str, str]]:
        """Search for stocks by symbol or name."""
        # yfinance doesn't have a great search API, so we'll use a simple approach
        # In production, you'd use a proper search API
        results = []
        
        # Common Indian stocks for demo
        common_stocks = {
            'RELIANCE': 'Reliance Industries',
            'TCS': 'Tata Consultancy Services',
            'INFY': 'Infosys',
            'HDFCBANK': 'HDFC Bank',
            'ICICIBANK': 'ICICI Bank',
            'SBIN': 'State Bank of India',
            'BHARTIARTL': 'Bharti Airtel',
            'ITC': 'ITC Limited',
            'KOTAKBANK': 'Kotak Mahindra Bank',
            'LT': 'Larsen & Toubro',
            'AXISBANK': 'Axis Bank',
            'ASIANPAINT': 'Asian Paints',
            'MARUTI': 'Maruti Suzuki',
            'BAJFINANCE': 'Bajaj Finance',
            'HCLTECH': 'HCL Technologies',
            'WIPRO': 'Wipro',
            'TITAN': 'Titan Company',
            'SUNPHARMA': 'Sun Pharmaceutical',
            'NESTLEIND': 'Nestle India',
        }
        
        query_upper = query.upper()
        for symbol, name in common_stocks.items():
            if query_upper in symbol or query_upper in name.upper():
                results.append({'symbol': symbol, 'name': name})
        
        return results[:10]  # Limit to 10 results


# Singleton instance
market_data_service = MarketDataService()
