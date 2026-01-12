import pytest
from unittest.mock import AsyncMock, patch
from app.services.tavily_service import TavilyService

@pytest.mark.unit
class TestTavilyService:
    """Unit tests for Tavily service"""
    
    @pytest.fixture
    def tavily_service(self):
        """Create a TavilyService instance"""
        with patch('app.services.tavily_service.settings') as mock_settings:
            mock_settings.TAVILY_API_KEY = "test_key"
            service = TavilyService()
            yield service
    
    @pytest.mark.asyncio
    async def test_search_success(self, tavily_service):
        """Test successful search"""
        mock_response = {
            "results": [
                {
                    "title": "Test Result",
                    "url": "https://example.com",
                    "content": "Test content",
                    "score": 0.95
                }
            ]
        }
        
        with patch.object(tavily_service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = lambda: None
            
            results = await tavily_service.search("test query")
            
            assert len(results) == 1
            assert results[0]["title"] == "Test Result"
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_with_max_results(self, tavily_service):
        """Test search with custom max_results"""
        mock_response = {
            "results": [
                {"title": f"Result {i}", "url": f"https://example.com/{i}", "content": "Content", "score": 0.9}
                for i in range(3)
            ]
        }
        
        with patch.object(tavily_service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = lambda: None
            
            results = await tavily_service.search("test query", max_results=3)
            
            assert len(results) == 3
            call_args = mock_post.call_args
            assert call_args[1]["json"]["max_results"] == 3
    
    @pytest.mark.asyncio
    async def test_search_empty_results(self, tavily_service):
        """Test search with no results"""
        mock_response = {"results": []}
        
        with patch.object(tavily_service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = lambda: None
            
            results = await tavily_service.search("test query")
            
            assert len(results) == 0

