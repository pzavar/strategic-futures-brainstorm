import pytest
from unittest.mock import AsyncMock, patch
from app.agents.scenario_agent import scenario_agent


@pytest.mark.unit
class TestScenarioAgent:
    """Unit tests for scenario agent"""
    
    @pytest.mark.asyncio
    async def test_scenario_agent_success(self):
        """Test successful scenario generation"""
        company_name = "Test Company"
        company_context = "Test Company is a leading technology firm..."
        
        # Mock Groq response with 4 scenarios
        mock_scenarios_response = """[
            {
                "title": "Incremental Growth Scenario",
                "description": "A scenario of steady growth...",
                "timeline": "2025-2030",
                "key_assumptions": "Stable market conditions",
                "likelihood": 0.3
            },
            {
                "title": "Disruptive Technology Scenario",
                "description": "A scenario with breakthrough technologies...",
                "timeline": "2024-2027",
                "key_assumptions": "Rapid technology adoption",
                "likelihood": 0.25
            },
            {
                "title": "Regulatory Constraint Scenario",
                "description": "A scenario with increased regulation...",
                "timeline": "2025-2028",
                "key_assumptions": "Increased regulation",
                "likelihood": 0.2
            },
            {
                "title": "Market Consolidation Scenario",
                "description": "A scenario of market consolidation...",
                "timeline": "2026-2030",
                "key_assumptions": "Market consolidation",
                "likelihood": 0.25
            }
        ]"""
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_scenarios_response)
            
            result = await scenario_agent(company_name, company_context)
            
            # Verify structure
            assert isinstance(result, list)
            assert len(result) == 4
            
            # Verify each scenario has required fields
            for scenario in result:
                assert "title" in scenario
                assert "description" in scenario
                assert "timeline" in scenario
                assert "key_assumptions" in scenario
                assert "likelihood" in scenario
                assert "scenario_number" in scenario
                assert isinstance(scenario["likelihood"], (int, float))
                assert 0.0 <= scenario["likelihood"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_scenario_agent_with_markdown_code_blocks(self):
        """Test scenario agent handles markdown code blocks"""
        company_name = "Test Company"
        company_context = "Test context"
        
        mock_scenarios_response = """```json
[
    {
        "title": "Scenario 1",
        "description": "Description 1",
        "timeline": "2025-2030",
        "key_assumptions": "Assumptions 1",
        "likelihood": 0.25
    }
]
```"""
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_scenarios_response)
            
            result = await scenario_agent(company_name, company_context)
            
            assert isinstance(result, list)
            assert len(result) >= 1
    
    @pytest.mark.asyncio
    async def test_scenario_agent_less_than_4_scenarios(self):
        """Test scenario agent handles fewer than 4 scenarios"""
        company_name = "Test Company"
        company_context = "Test context"
        
        mock_scenarios_response = """[
            {
                "title": "Scenario 1",
                "description": "Description 1",
                "timeline": "2025-2030",
                "key_assumptions": "Assumptions 1",
                "likelihood": 0.25
            },
            {
                "title": "Scenario 2",
                "description": "Description 2",
                "timeline": "2025-2030",
                "key_assumptions": "Assumptions 2",
                "likelihood": 0.25
            }
        ]"""
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_scenarios_response)
            
            result = await scenario_agent(company_name, company_context)
            
            # Should accept fewer than 4 scenarios
            assert isinstance(result, list)
            assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_scenario_agent_more_than_4_scenarios(self):
        """Test scenario agent truncates to 4 scenarios if more are returned"""
        company_name = "Test Company"
        company_context = "Test context"
        
        # Create 6 scenarios
        scenarios = [
            {
                "title": f"Scenario {i+1}",
                "description": f"Description {i+1}",
                "timeline": "2025-2030",
                "key_assumptions": f"Assumptions {i+1}",
                "likelihood": 0.25
            }
            for i in range(6)
        ]
        
        import json
        mock_scenarios_response = json.dumps(scenarios)
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_scenarios_response)
            
            result = await scenario_agent(company_name, company_context)
            
            # Should truncate to 4
            assert isinstance(result, list)
            assert len(result) == 4
    
    @pytest.mark.asyncio
    async def test_scenario_agent_missing_likelihood(self):
        """Test scenario agent adds default likelihood if missing"""
        company_name = "Test Company"
        company_context = "Test context"
        
        mock_scenarios_response = """[
            {
                "title": "Scenario 1",
                "description": "Description 1",
                "timeline": "2025-2030",
                "key_assumptions": "Assumptions 1"
            }
        ]"""
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(return_value=mock_scenarios_response)
            
            result = await scenario_agent(company_name, company_context)
            
            # Should have default likelihood
            assert result[0]["likelihood"] == 0.25
    
    @pytest.mark.asyncio
    async def test_scenario_agent_error_fallback(self):
        """Test scenario agent falls back to default scenarios on error"""
        company_name = "Test Company"
        company_context = "Test context"
        
        with patch('app.agents.scenario_agent.groq_service') as mock_groq:
            mock_groq.generate = AsyncMock(side_effect=Exception("API Error"))
            
            result = await scenario_agent(company_name, company_context)
            
            # Should have fallback scenarios
            assert isinstance(result, list)
            assert len(result) == 4
            
            # Verify fallback scenarios have required fields
            for scenario in result:
                assert "title" in scenario
                assert "description" in scenario
                assert "timeline" in scenario
                assert "key_assumptions" in scenario
                assert "likelihood" in scenario
                assert "scenario_number" in scenario
                assert company_name in scenario["title"] or "Scenario" in scenario["title"]

