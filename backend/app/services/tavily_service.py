import httpx
import asyncio
from typing import List, Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TavilyService:
    """Service for interacting with Tavily Search API"""
    
    BASE_URL = "https://api.tavily.com"
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Content-Type": "application/json"
            },
            timeout=60.0  # Increase timeout to 60 seconds
        )
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced"
    ) -> List[Dict[str, Any]]:
        """
        Search the web using Tavily API
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            search_depth: "basic" or "advanced"
            
        Returns:
            List of search results with title, url, content, score
        """
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth
        }
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = await self.client.post("/search", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("results", [])
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    logger.warning(f"Tavily rate limited, attempt {attempt + 1}/{self.MAX_RETRIES}")
                    if attempt < self.MAX_RETRIES - 1:
                        await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                        continue
                elif e.response.status_code >= 500:  # Server error
                    if attempt < self.MAX_RETRIES - 1:
                        logger.warning(f"Tavily server error, retrying in {self.RETRY_DELAY * (2 ** attempt)}s")
                        await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                        continue
                logger.error(f"Tavily API error: {e.response.status_code} - {e.response.text}")
                raise
            except asyncio.CancelledError as e:
                logger.error(f"Tavily API request cancelled (timeout?): {e}", exc_info=True)
                raise
            except httpx.TimeoutException as e:
                logger.error(f"Tavily API timeout after {self.client.timeout}s: {e}", exc_info=True)
                if attempt < self.MAX_RETRIES - 1:
                    logger.info(f"Retrying Tavily search (attempt {attempt + 2}/{self.MAX_RETRIES})")
                    await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                    continue
                raise
            except Exception as e:
                logger.error(f"Error calling Tavily API: {type(e).__name__}: {str(e)}", exc_info=True)
                if attempt < self.MAX_RETRIES - 1:
                    logger.info(f"Retrying Tavily search (attempt {attempt + 2}/{self.MAX_RETRIES})")
                    await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                    continue
                raise
        
        raise Exception("Failed to search after all retries")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance
tavily_service = TavilyService()

