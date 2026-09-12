"""
Data fetching service for market data.
Uses robust MarketDataFetcher with multiple sources and fallbacks.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.schemas import DailyPriceResponse, StockQuote, StockFundamentals

# Import our robust fetcher
try:
    from data_fetcher import MarketDataFetcher
    fetcher = MarketDataFetcher()
except Exception as e:
    print(f"Warning: Could not import MarketDataFetcher: {e}")
    fetcher = None


class MarketDataService:
    """Service for fetching market data from external sources."""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl: int = 300  # 5 minutes for quotes
    
    async def get_historical_prices(
        self, 
        symbol: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        period: str = "1mo"
    ) -> List[DailyPriceResponse]:
        """Fetch historical daily prices."""
        if not fetcher:
            return []
        
        try:
            # Use our robust fetcher
            history = fetcher.get_history(symbol, period=period, use_mock=True)
            
            # If fetcher returns None, generate mock data directly
            if not history:
                from data_fetcher import MockDataGenerator
                history = MockDataGenerator.generate_history(symbol, days=30)
            
            prices = []
            for row in history:
                prices.append(DailyPriceResponse(
                    symbol=symbol,
                    date=row['date'],
                    open=row.get('open'),
                    high=row.get('high'),
                    low=row.get('low'),
                    close=row.get('close'),
                    volume=row.get('volume'),
                    adjusted_close=row.get('close')
                ))
            
            return prices
            
        except Exception as e:
            print(f"Error fetching historical prices for {symbol}: {e}")
            # Last resort fallback - generate mock data
            try:
                from data_fetcher import MockDataGenerator
                history = MockDataGenerator.generate_history(symbol, days=30)
                prices = []
                for row in history:
                    prices.append(DailyPriceResponse(
                        symbol=symbol,
                        date=row['date'],
                        open=row.get('open'),
                        high=row.get('high'),
                        low=row.get('low'),
                        close=row.get('close'),
                        volume=row.get('volume'),
                        adjusted_close=row.get('close')
                    ))
                return prices
            except:
                return []
    
    async def get_current_quote(self, symbol: str) -> Optional[StockQuote]:
        """Fetch current stock quote (delayed)."""
        if not fetcher:
            return None
        
        try:
            # Use our robust fetcher with fallback to mock data
            quote = fetcher.get_quote(symbol, use_mock=True)
            
            if not quote:
                return None
            
            return StockQuote(
                symbol=quote.get('symbol', symbol),
                price=quote.get('price', 0),
                change=quote.get('change', 0),
                change_percent=quote.get('change_percent', 0),
                volume=quote.get('volume'),
                timestamp=datetime.fromisoformat(quote.get('timestamp', datetime.now().isoformat())),
                source=quote.get('source', 'unknown'),
                is_mock=quote.get('is_mock', False)
            )
            
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return None
    
    async def get_fundamentals(self, symbol: str) -> Optional[StockFundamentals]:
        """Fetch fundamental data for a stock."""
        if not fetcher:
            return None
        
        try:
            company_info = fetcher.get_company_info(symbol, use_mock=True)
            
            if not company_info:
                return None
            
            return StockFundamentals(
                symbol=symbol,
                market_cap=company_info.get('market_cap'),
                pe_ratio=company_info.get('pe_ratio'),
                eps=None,  # Would need earnings data
                book_value=None,
                debt_to_equity=company_info.get('debt_to_equity'),
                roe=company_info.get('roe'),
                revenue_growth=company_info.get('revenue_growth'),
                profit_margin=company_info.get('profit_margin')
            )
            
        except Exception as e:
            print(f"Error fetching fundamentals for {symbol}: {e}")
            return None
    
    async def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get basic company information."""
        if not fetcher:
            return None
        
        try:
            company_info = fetcher.get_company_info(symbol, use_mock=True)
            return company_info
            
        except Exception as e:
            print(f"Error fetching company info for {symbol}: {e}")
            return None
    
    async def search_stocks(self, query: str) -> List[Dict[str, str]]:
        """Search for stocks by symbol or name."""
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
            'TATAMOTORS': 'Tata Motors',
            'ULTRACEMCO': 'UltraTech Cement',
        }
        
        query_upper = query.upper()
        for symbol, name in common_stocks.items():
            if query_upper in symbol or query_upper in name.upper():
                results.append({'symbol': symbol, 'name': name})
        
        return results[:10]  # Limit to 10 results


# Singleton instance
market_data_service = MarketDataService()
