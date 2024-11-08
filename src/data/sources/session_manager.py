from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
from pathlib import Path
import yfinance as yf
from typing import Optional
import os

class YFinanceSessionManager:
    """
    Manages the YFinance API session with caching and rate limiting.
    Implements singleton pattern to ensure only one session is created.
    """
    _instance = None
    _session = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YFinanceSessionManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._session is None:
            self._initialize_session()
    
    def _initialize_session(self):
        """Initialize the session with caching and rate limiting"""
        # Create cache directory if it doesn't exist
        cache_dir = Path.home() / '.cache' / 'mining_analysis'
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "yfinance.cache"
        
        # Custom session class with caching and rate limiting
        class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
            pass
        
        # Create session with rate limiting and caching
        self._session = CachedLimiterSession(
            limiter=Limiter(
                RequestRate(2, Duration.SECOND * 5),  # max 2 requests per 5 seconds
                RequestRate(10, Duration.MINUTE)      # max 10 requests per minute
            ),
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(str(cache_file)),
            expire_after=Duration.HOUR * 12  # Cache expires after 12 hours
        )
        
        # Set custom user agent
        self._session.headers['User-agent'] = 'mining-analysis-tool/1.0'
    
    def get_session(self) -> Session:
        """Get the cached and rate-limited session"""
        return self._session
    
    def get_ticker(self, symbol: str) -> Optional[yf.Ticker]:
        """
        Get a YFinance Ticker object with the managed session.
        
        Args:
            symbol (str): The stock symbol to get data for
            
        Returns:
            Optional[yf.Ticker]: Ticker object or None if creation fails
        """
        try:
            return yf.Ticker(symbol, session=self._session)
        except Exception as e:
            print(f"Error creating ticker for {symbol}: {e}")
            return None
    
    def clear_cache(self):
        """Clear the cache"""
        if self._session:
            self._session.cache.clear()