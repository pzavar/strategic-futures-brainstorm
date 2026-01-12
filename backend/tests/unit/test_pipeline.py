import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.pipeline import AnalysisPipeline, AnalysisState


@pytest.mark.unit
class TestAnalysisPipeline:
    """Unit tests for analysis pipeline"""
    
    @pytest.fixture
    def mock_research_result(self):
        """Mock research agent result"""
        return {
            "research_questions": ["Question 1?", "Question 2?"],
            "search_results": {
                "Question 1?": [{"title": "Result 1", "content": "Content 1"}],
                "Question 2?": [{"title": "Result 2", "content": "Content 2"}]
            },
            "company_context": "Test Company is a leading technology firm..."
        }
    
    @pytest.fixture
    def mock_scenarios(self):
        """Mock scenario agent result"""
        return [
            {
                "scenario_number": 1,
                "title": "Scenario 1",
                "description": "Description 1",
                "timeline": "2025-2030",
                "key_assumptions": "Assumptions 1",
                "likelihood": 0.25
            },
            {
                "scenario_number": 2,
                "title": "Scenario 2",
                "description": "Description 2",
                "timeline": "2025-2030",
                "key_assumptions": "Assumptions 2",
                "likelihood": 0.25
            }
        ]
    
    @pytest.fixture
    def mock_strategies(self):
        """Mock strategy agent result"""
        return [
            {
                "name": "Strategy 1",
                "description": "Description 1",
                "expected_impact": "Impact 1",
                "key_risks": "Risks 1"
            },
            {
                "name": "Strategy 2",
                "description": "Description 2",
                "expected_impact": "Impact 2",
                "key_risks": "Risks 2"
            }
        ]
    
    @pytest.mark.asyncio
    async def test_pipeline_run_success(self, mock_research_result, mock_scenarios, mock_strategies):
        """Test successful pipeline execution"""
        company_name = "Test Company"
        progress_events = []
        
        async def progress_callback(event_type: str, message: str):
            progress_events.append((event_type, message))
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario, \
             patch('app.agents.pipeline.strategy_agent') as mock_strategy:
            
            mock_research.return_value = mock_research_result
            mock_scenario.return_value = mock_scenarios
            mock_strategy.return_value = mock_strategies
            
            pipeline = AnalysisPipeline(progress_callback=progress_callback)
            result = await pipeline.run(company_name)
            
            # Verify final state
            assert result["company_name"] == company_name
            assert len(result["research_questions"]) == 2
            assert len(result["scenarios"]) == 2
            assert len(result["strategies"]) == 2  # One per scenario
            
            # Verify progress events
            assert len(progress_events) > 0
            event_types = [event[0] for event in progress_events]
            assert "analysis_start" in event_types
            assert "research_start" in event_types
            assert "research_complete" in event_types
            assert "scenarios_start" in event_types
            assert "scenarios_complete" in event_types
            assert "strategies_start" in event_types
            assert "strategies_complete" in event_types
            assert "analysis_complete" in event_types
    
    @pytest.mark.asyncio
    async def test_pipeline_run_without_callback(self, mock_research_result, mock_scenarios, mock_strategies):
        """Test pipeline execution without progress callback"""
        company_name = "Test Company"
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario, \
             patch('app.agents.pipeline.strategy_agent') as mock_strategy:
            
            mock_research.return_value = mock_research_result
            mock_scenario.return_value = mock_scenarios
            mock_strategy.return_value = mock_strategies
            
            pipeline = AnalysisPipeline(progress_callback=None)
            result = await pipeline.run(company_name)
            
            # Should still complete successfully
            assert result["company_name"] == company_name
            assert len(result["scenarios"]) == 2
    
    @pytest.mark.asyncio
    async def test_pipeline_research_error(self, mock_scenarios, mock_strategies):
        """Test pipeline handles research agent errors"""
        company_name = "Test Company"
        progress_events = []
        
        async def progress_callback(event_type: str, message: str):
            progress_events.append((event_type, message))
        
        with patch('app.agents.pipeline.research_agent') as mock_research:
            mock_research.side_effect = Exception("Research error")
            
            pipeline = AnalysisPipeline(progress_callback=progress_callback)
            
            with pytest.raises(Exception):
                await pipeline.run(company_name)
            
            # Should emit error event
            event_types = [event[0] for event in progress_events]
            assert "research_error" in event_types or "analysis_failed" in event_types
    
    @pytest.mark.asyncio
    async def test_pipeline_scenario_error(self, mock_research_result, mock_strategies):
        """Test pipeline handles scenario agent errors"""
        company_name = "Test Company"
        progress_events = []
        
        async def progress_callback(event_type: str, message: str):
            progress_events.append((event_type, message))
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario:
            
            mock_research.return_value = mock_research_result
            mock_scenario.side_effect = Exception("Scenario error")
            
            pipeline = AnalysisPipeline(progress_callback=progress_callback)
            
            with pytest.raises(Exception):
                await pipeline.run(company_name)
            
            # Should have completed research
            event_types = [event[0] for event in progress_events]
            assert "research_complete" in event_types
            assert "scenarios_error" in event_types or "analysis_failed" in event_types
    
    @pytest.mark.asyncio
    async def test_pipeline_strategy_error(self, mock_research_result, mock_scenarios):
        """Test pipeline handles strategy agent errors"""
        company_name = "Test Company"
        progress_events = []
        
        async def progress_callback(event_type: str, message: str):
            progress_events.append((event_type, message))
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario, \
             patch('app.agents.pipeline.strategy_agent') as mock_strategy:
            
            mock_research.return_value = mock_research_result
            mock_scenario.return_value = mock_scenarios
            mock_strategy.side_effect = Exception("Strategy error")
            
            pipeline = AnalysisPipeline(progress_callback=progress_callback)
            
            with pytest.raises(Exception):
                await pipeline.run(company_name)
            
            # Should have completed research and scenarios
            event_types = [event[0] for event in progress_events]
            assert "scenarios_complete" in event_types
            assert "strategies_error" in event_types or "analysis_failed" in event_types
    
    @pytest.mark.asyncio
    async def test_pipeline_strategies_for_multiple_scenarios(self, mock_research_result, mock_strategies):
        """Test pipeline generates strategies for all scenarios"""
        company_name = "Test Company"
        scenarios = [
            {
                "scenario_number": i+1,
                "title": f"Scenario {i+1}",
                "description": f"Description {i+1}",
                "timeline": "2025-2030",
                "key_assumptions": f"Assumptions {i+1}",
                "likelihood": 0.25
            }
            for i in range(4)
        ]
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario, \
             patch('app.agents.pipeline.strategy_agent') as mock_strategy:
            
            mock_research.return_value = mock_research_result
            mock_scenario.return_value = scenarios
            mock_strategy.return_value = mock_strategies
            
            pipeline = AnalysisPipeline(progress_callback=None)
            result = await pipeline.run(company_name)
            
            # Should have strategies for all 4 scenarios
            assert len(result["strategies"]) == 4
            assert mock_strategy.call_count == 4
    
    @pytest.mark.asyncio
    async def test_pipeline_state_progression(self, mock_research_result, mock_scenarios, mock_strategies):
        """Test pipeline state progresses correctly through steps"""
        company_name = "Test Company"
        
        with patch('app.agents.pipeline.research_agent') as mock_research, \
             patch('app.agents.pipeline.scenario_agent') as mock_scenario, \
             patch('app.agents.pipeline.strategy_agent') as mock_strategy:
            
            mock_research.return_value = mock_research_result
            mock_scenario.return_value = mock_scenarios
            mock_strategy.return_value = mock_strategies
            
            pipeline = AnalysisPipeline(progress_callback=None)
            result = await pipeline.run(company_name)
            
            # Verify state progression
            assert result["current_step"] == "strategies"  # Final step
            assert len(result["research_questions"]) > 0
            assert len(result["company_context"]) > 0
            assert len(result["scenarios"]) > 0
            assert len(result["strategies"]) > 0

