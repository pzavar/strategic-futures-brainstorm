import pytest
from unittest.mock import AsyncMock, patch
from app.services.groq_service import GroqService

@pytest.mark.unit
class TestGroqService:
    """Unit tests for Groq service"""
    
    @pytest.fixture
    def groq_service(self):
        """Create a GroqService instance"""
        with patch('app.services.groq_service.settings') as mock_settings:
            mock_settings.GROQ_API_KEY = "test_key"
            service = GroqService()
            yield service
    
    @pytest.mark.asyncio
    async def test_generate_success(self, groq_service):
        """Test successful text generation"""
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Generated response text"
                }
            }]
        }
        
        with patch.object(groq_service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = lambda: None
            
            result = await groq_service.generate("Test prompt")
            
            assert result == "Generated response text"
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_with_system_prompt(self, groq_service):
        """Test generation with system prompt"""
        mock_response = {
            "choices": [{
                "message": {
                    "content": "System response"
                }
            }]
        }
        
        with patch.object(groq_service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = lambda: None
            
            result = await groq_service.generate(
                "Test prompt",
                system_prompt="System instruction"
            )
            
            assert result == "System response"
            call_args = mock_post.call_args
            assert "system" in str(call_args)
    
    @pytest.mark.asyncio
    async def test_generate_rate_limit_retry(self, groq_service):
        """Test retry logic on rate limit"""
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Success after retry"
                }
            }]
        }
        
        with patch.object(groq_service.client, 'post', new_callable=AsyncMock) as mock_post:
            # First call: rate limit (429)
            # Second call: success (200)
            from httpx import HTTPStatusError
            import httpx
            
            rate_limit_response = httpx.Response(429, json={})
            success_response = httpx.Response(200, json=mock_response)
            success_response.json = lambda: mock_response
            
            mock_post.side_effect = [
                HTTPStatusError("Rate limited", request=None, response=rate_limit_response),
                type('obj', (object,), {
                    'status_code': 200,
                    'json': lambda: mock_response,
                    'raise_for_status': lambda: None
                })()
            ]
            
            with patch('asyncio.sleep', new_callable=AsyncMock):
                result = await groq_service.generate("Test prompt")
                
                assert result == "Success after retry"
                assert mock_post.call_count == 2

