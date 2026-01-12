import pytest
from unittest.mock import AsyncMock, patch
from app.agents.strategy_agent import strategy_agent


@pytest.mark.unit
class TestStrategyAgent:
    """Unit tests for strategy agent"""
    
    @pytest.mark.asyncio
    async def test_strategy_agent_success(self):
        """Test successful strategy generation"""
        company_name = "Test Company"
        company_context = "Test Company is a leading technology firm..."
        scenario = {
            "title": "Incremental Growth Scenario",
            "description": "A scenario of steady growth...",
            "timeline": "2025-2030",
            "key_assumptions": "Stable market conditions"
        }
        
        # Mock Groq response with 2 strategies
        mock_strategies_response = """[
            {
                "name": "Digital Transformation Strategy",
                "description": "A comprehensive strategy to transform...",
                "expected_impact": "This strategy would increase efficiency...",
                "key_risks": "Key risks include implementation challenges..."
            },
            {
                "name": "Market Expansion Strategy",
                "description": "A strategy to expand into new markets...",
                "expected_impact": "This strategy would increase market share...",
                "key_risks": "Key risks include market entry barriers..."
            }
        ]"""
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_strategies_response)
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            # Verify structure
            assert isinstance(result, list)
            assert 2 <= len(result) <= 3
            
            # Verify each strategy has required fields
            for strategy in result:
                assert "name" in strategy
                assert "description" in strategy
                assert "expected_impact" in strategy
                assert "key_risks" in strategy
                assert isinstance(strategy["name"], str)
                assert len(strategy["name"]) > 0
    
    @pytest.mark.asyncio
    async def test_strategy_agent_with_markdown_code_blocks(self):
        """Test strategy agent handles markdown code blocks"""
        company_name = "Test Company"
        company_context = "Test context"
        scenario = {
            "title": "Test Scenario",
            "description": "Test description",
            "timeline": "2025-2030",
            "key_assumptions": "Test assumptions"
        }
        
        mock_strategies_response = """```json
[
    {
        "name": "Strategy 1",
        "description": "Description 1",
        "expected_impact": "Impact 1",
        "key_risks": "Risks 1"
    }
]
```"""
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_strategies_response)
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            assert isinstance(result, list)
            assert len(result) >= 1
    
    @pytest.mark.asyncio
    async def test_strategy_agent_less_than_2_strategies(self):
        """Test strategy agent handles fewer than 2 strategies"""
        company_name = "Test Company"
        company_context = "Test context"
        scenario = {
            "title": "Test Scenario",
            "description": "Test description",
            "timeline": "2025-2030",
            "key_assumptions": "Test assumptions"
        }
        
        mock_strategies_response = """[
            {
                "name": "Strategy 1",
                "description": "Description 1",
                "expected_impact": "Impact 1",
                "key_risks": "Risks 1"
            }
        ]"""
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_strategies_response)
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            # Should accept fewer than 2 strategies
            assert isinstance(result, list)
            assert len(result) == 1
    
    @pytest.mark.asyncio
    async def test_strategy_agent_more_than_3_strategies(self):
        """Test strategy agent truncates to 3 strategies if more are returned"""
        company_name = "Test Company"
        company_context = "Test context"
        scenario = {
            "title": "Test Scenario",
            "description": "Test description",
            "timeline": "2025-2030",
            "key_assumptions": "Test assumptions"
        }
        
        # Create 5 strategies
        strategies = [
            {
                "name": f"Strategy {i+1}",
                "description": f"Description {i+1}",
                "expected_impact": f"Impact {i+1}",
                "key_risks": f"Risks {i+1}"
            }
            for i in range(5)
        ]
        
        import json
        mock_strategies_response = json.dumps(strategies)
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_strategies_response)
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            # Should truncate to 3
            assert isinstance(result, list)
            assert len(result) == 3
    
    @pytest.mark.asyncio
    async def test_strategy_agent_error_fallback(self):
        """Test strategy agent falls back to default strategies on error"""
        company_name = "Test Company"
        company_context = "Test context"
        scenario = {
            "title": "Test Scenario",
            "description": "Test description",
            "timeline": "2025-2030",
            "key_assumptions": "Test assumptions"
        }
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(side_effect=Exception("API Error"))
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            # Should have fallback strategies
            assert isinstance(result, list)
            assert len(result) == 2
            
            # Verify fallback strategies have required fields
            for strategy in result:
                assert "name" in strategy
                assert "description" in strategy
                assert "expected_impact" in strategy
                assert "key_risks" in strategy
                assert scenario["title"] in strategy["name"] or "Strategy" in strategy["name"]
    
    @pytest.mark.asyncio
    async def test_strategy_agent_with_missing_scenario_fields(self):
        """Test strategy agent handles missing scenario fields gracefully"""
        company_name = "Test Company"
        company_context = "Test context"
        scenario = {
            "title": "Test Scenario"
            # Missing other fields
        }
        
        mock_strategies_response = """[
            {
                "name": "Strategy 1",
                "description": "Description 1",
                "expected_impact": "Impact 1",
                "key_risks": "Risks 1"
            }
        ]"""
        
        with patch('app.agents.strategy_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_strategies_response)
            
            result = await strategy_agent(company_name, company_context, scenario)
            
            # Should still work with missing fields
            assert isinstance(result, list)
            assert len(result) >= 1

