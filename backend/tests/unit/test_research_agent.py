import pytest
from unittest.mock import AsyncMock, patch
from app.agents.research_agent import research_agent


@pytest.mark.unit
class TestResearchAgent:
    """Unit tests for research agent"""
    
    @pytest.mark.asyncio
    async def test_research_agent_success(self):
        """Test successful research agent execution"""
        company_name = "Test Company"
        
        # Mock Groq responses
        mock_questions_response = '["What is Test Company\'s business model?", "Who are Test Company\'s competitors?", "What technologies affect Test Company?"]'
        mock_context_response = "Test Company is a leading firm in the technology sector..."
        
        # Mock Tavily search results
        mock_search_results = [
            {
                "title": "Test Result",
                "url": "https://example.com",
                "content": "Test content about the company",
                "score": 0.95
            }
        ]
        
        with patch('app.agents.research_agent.groq_service') as mock_groq, \
             patch('app.agents.research_agent.tavily_service') as mock_tavily:
            
            # Mock Groq service calls
            mock_groq.generate = AsyncMock(side_effect=[
                mock_questions_response,  # First call for questions
                mock_context_response     # Second call for synthesis
            ])
            
            # Mock Tavily service calls
            mock_tavily.search = AsyncMock(return_value=mock_search_results)
            
            result = await research_agent(company_name)
            
            # Verify structure
            assert "research_questions" in result
            assert "search_results" in result
            assert "company_context" in result
            
            # Verify questions
            assert isinstance(result["research_questions"], list)
            assert len(result["research_questions"]) > 0
            
            # Verify search results
            assert isinstance(result["search_results"], dict)
            assert len(result["search_results"]) == len(result["research_questions"])
            
            # Verify context
            assert isinstance(result["company_context"], str)
            assert len(result["company_context"]) > 0
            
            # Verify Groq was called twice (questions + synthesis)
            assert mock_groq.generate.call_count == 2
            
            # Verify Tavily was called for each question
            assert mock_tavily.search.call_count == len(result["research_questions"])
    
    @pytest.mark.asyncio
    async def test_research_agent_with_markdown_code_blocks(self):
        """Test research agent handles markdown code blocks in responses"""
        company_name = "Test Company"
        
        # Mock Groq response with markdown code blocks
        mock_questions_response = '```json\n["Question 1?", "Question 2?"]\n```'
        mock_context_response = "Synthesized context"
        
        with patch('app.agents.research_agent.groq_service') as mock_groq, \
             patch('app.agents.research_agent.tavily_service') as mock_tavily:
            
            mock_groq.generate = AsyncMock(side_effect=[
                mock_questions_response,
                mock_context_response
            ])
            mock_tavily.search = AsyncMock(return_value=[])
            
            result = await research_agent(company_name)
            
            assert isinstance(result["research_questions"], list)
            assert len(result["research_questions"]) == 2
    
    @pytest.mark.asyncio
    async def test_research_agent_groq_error_fallback(self):
        """Test research agent falls back to default questions on Groq error"""
        company_name = "Test Company"
        
        with patch('app.agents.research_agent.groq_service') as mock_groq, \
             patch('app.agents.research_agent.tavily_service') as mock_tavily:
            
            # First call (questions) fails, second call (synthesis) succeeds
            mock_groq.generate = AsyncMock(side_effect=[
                Exception("API Error"),  # Questions generation fails
                "Synthesized context"   # Synthesis succeeds
            ])
            mock_tavily.search = AsyncMock(return_value=[])
            
            result = await research_agent(company_name)
            
            # Should have fallback questions
            assert isinstance(result["research_questions"], list)
            assert len(result["research_questions"]) == 5  # Default fallback has 5 questions
            assert company_name in result["research_questions"][0]
    
    @pytest.mark.asyncio
    async def test_research_agent_tavily_error_handling(self):
        """Test research agent handles Tavily search errors gracefully"""
        company_name = "Test Company"
        
        mock_questions_response = '["Question 1?", "Question 2?"]'
        mock_context_response = "Synthesized context"
        
        with patch('app.agents.research_agent.groq_service') as mock_groq, \
             patch('app.agents.research_agent.tavily_service') as mock_tavily:
            
            mock_groq.generate = AsyncMock(side_effect=[
                mock_questions_response,
                mock_context_response
            ])
            
            # First search succeeds, second fails
            mock_tavily.search = AsyncMock(side_effect=[
                [{"title": "Result 1", "content": "Content"}],
                Exception("Search error")
            ])
            
            result = await research_agent(company_name)
            
            # Should have empty results for failed search
            assert len(result["search_results"]) == 2
            assert len(result["search_results"][result["research_questions"][0]]) > 0
            assert len(result["search_results"][result["research_questions"][1]]) == 0
    
    @pytest.mark.asyncio
    async def test_research_agent_synthesis_error_fallback(self):
        """Test research agent falls back to default context on synthesis error"""
        company_name = "Test Company"
        
        mock_questions_response = '["Question 1?", "Question 2?"]'
        
        with patch('app.agents.research_agent.groq_service') as mock_groq, \
             patch('app.agents.research_agent.tavily_service') as mock_tavily:
            
            mock_groq.generate = AsyncMock(side_effect=[
                mock_questions_response,
                Exception("Synthesis error")
            ])
            mock_tavily.search = AsyncMock(return_value=[])
            
            result = await research_agent(company_name)
            
            # Should have fallback context
            assert isinstance(result["company_context"], str)
            assert company_name in result["company_context"]
            assert "Research completed" in result["company_context"]

