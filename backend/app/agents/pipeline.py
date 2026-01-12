from typing import TypedDict, List, Dict, Any, Optional, Callable
from langgraph.graph import StateGraph, END
import asyncio
import logging
from app.agents.research_agent import research_agent
from app.agents.scenario_agent import scenario_agent
from app.agents.strategy_agent import strategy_agent

logger = logging.getLogger(__name__)


class AnalysisState(TypedDict):
    company_name: str
    research_questions: List[str]
    search_results: Dict[str, Any]
    company_context: str
    scenarios: List[Dict[str, Any]]
    strategies: Dict[str, List[Dict[str, Any]]]
    current_step: str
    progress_message: str


class AnalysisPipeline:
    """LangGraph pipeline for strategic futures analysis"""
    
    def __init__(self, progress_callback: Optional[Callable[[str, str], None]] = None):
        """
        Initialize the pipeline
        
        Args:
            progress_callback: Optional callback function(event_type, message) for progress updates
        """
        self.progress_callback = progress_callback
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AnalysisState)
        
        # Add nodes
        workflow.add_node("research", self._research_node)
        workflow.add_node("scenarios", self._scenarios_node)
        workflow.add_node("strategies", self._strategies_node)
        
        # Define edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "scenarios")
        workflow.add_edge("scenarios", "strategies")
        workflow.add_edge("strategies", END)
        
        return workflow.compile()
    
    async def _emit_progress(self, event_type: str, message: str):
        """Emit progress event if callback is set"""
        msg_preview = (message or "")[:50] if message else ""
        logger.debug(f"[PIPELINE] Emitting progress event: {event_type} - {msg_preview}")
        if self.progress_callback:
            try:
                # Callback is now async, so await it
                if asyncio.iscoroutinefunction(self.progress_callback):
                    await self.progress_callback(event_type, message)
                else:
                    self.progress_callback(event_type, message)
            except Exception as e:
                logger.error(f"[PIPELINE] Error in progress callback: {e}", exc_info=True)
    
    async def _research_node(self, state: AnalysisState) -> AnalysisState:
        """Research node: Generate questions and search"""
        company_name = state["company_name"]
        logger.debug(f"[PIPELINE] Starting research node for: {company_name}")
        await self._emit_progress("research_start", "Starting research phase...")
        
        try:
            logger.debug(f"[PIPELINE] Calling research_agent for: {company_name}")
            research_result = await research_agent(company_name)
            logger.debug(f"[PIPELINE] Research agent completed, got {len(research_result.get('research_questions', []))} questions")
            
            state["research_questions"] = research_result["research_questions"]
            state["search_results"] = research_result["search_results"]
            state["company_context"] = research_result["company_context"]
            state["current_step"] = "research"
            state["progress_message"] = "Research completed"
            
            await self._emit_progress("research_complete", "Research phase completed")
            logger.debug(f"[PIPELINE] Research node completed successfully")
        except Exception as e:
            logger.error(f"[PIPELINE] CRITICAL: Error in research node: {type(e).__name__}: {str(e)}", exc_info=True)
            state["progress_message"] = f"Research error: {str(e)}"
            await self._emit_progress("research_error", f"Research error: {str(e)}")
            raise
        
        return state
    
    async def _scenarios_node(self, state: AnalysisState) -> AnalysisState:
        """Scenarios node: Generate future scenarios"""
        company_name = state["company_name"]
        logger.debug(f"[PIPELINE] Starting scenarios node for: {company_name}")
        await self._emit_progress("scenarios_start", "Generating future scenarios...")
        
        try:
            logger.debug(f"[PIPELINE] Calling scenario_agent for: {company_name}")
            scenarios = await scenario_agent(
                company_name,
                state["company_context"]
            )
            logger.debug(f"[PIPELINE] Scenario agent completed, generated {len(scenarios)} scenarios")
            
            state["scenarios"] = scenarios
            state["current_step"] = "scenarios"
            state["progress_message"] = f"Generated {len(scenarios)} scenarios"
            
            await self._emit_progress("scenarios_complete", f"Generated {len(scenarios)} scenarios")
            logger.debug(f"[PIPELINE] Scenarios node completed successfully")
        except Exception as e:
            logger.error(f"[PIPELINE] CRITICAL: Error in scenarios node: {type(e).__name__}: {str(e)}", exc_info=True)
            state["progress_message"] = f"Scenarios error: {str(e)}"
            await self._emit_progress("scenarios_error", f"Scenarios error: {str(e)}")
            raise
        
        return state
    
    async def _strategies_node(self, state: AnalysisState) -> AnalysisState:
        """Strategies node: Generate strategies for each scenario"""
        company_name = state["company_name"]
        num_scenarios = len(state["scenarios"])
        logger.debug(f"[PIPELINE] Starting strategies node for: {company_name}, {num_scenarios} scenarios")
        await self._emit_progress("strategies_start", "Generating strategic recommendations...")
        
        try:
            strategies_dict = {}
            
            for i, scenario in enumerate(state["scenarios"]):
                scenario_title = scenario.get("title", f"scenario_{i+1}")
                logger.debug(f"[PIPELINE] Processing scenario {i+1}/{num_scenarios}: {scenario_title}")
                await self._emit_progress(
                    "strategy_progress",
                    f"Generating strategies for scenario {i+1}/{num_scenarios}..."
                )
                
                strategies = await strategy_agent(
                    company_name,
                    state["company_context"],
                    scenario
                )
                logger.debug(f"[PIPELINE] Generated {len(strategies)} strategies for scenario {i+1}")
                
                # Use scenario title or number as key
                scenario_key = scenario.get("title", f"scenario_{scenario.get('scenario_number', i+1)}")
                strategies_dict[scenario_key] = strategies
            
            state["strategies"] = strategies_dict
            state["current_step"] = "strategies"
            state["progress_message"] = "All strategies generated"
            
            await self._emit_progress("strategies_complete", "All strategic recommendations completed")
            logger.debug(f"[PIPELINE] Strategies node completed successfully, total strategies: {sum(len(s) for s in strategies_dict.values())}")
        except Exception as e:
            logger.error(f"[PIPELINE] CRITICAL: Error in strategies node: {type(e).__name__}: {str(e)}", exc_info=True)
            state["progress_message"] = f"Strategies error: {str(e)}"
            await self._emit_progress("strategies_error", f"Strategies error: {str(e)}")
            raise
        
        return state
    
    async def run(self, company_name: str) -> AnalysisState:
        """
        Run the analysis pipeline
        
        Args:
            company_name: Name of the company to analyze
            
        Returns:
            Final analysis state
        """
        initial_state: AnalysisState = {
            "company_name": company_name,
            "research_questions": [],
            "search_results": {},
            "company_context": "",
            "scenarios": [],
            "strategies": {},
            "current_step": "initializing",
            "progress_message": "Starting analysis..."
        }
        
        try:
            logger.info(f"[PIPELINE] Starting pipeline execution for: {company_name}")
            await self._emit_progress("analysis_start", f"Starting analysis for {company_name}")
            
            # Run the graph
            logger.debug(f"[PIPELINE] Invoking LangGraph workflow...")
            final_state = await self.graph.ainvoke(initial_state)
            logger.debug(f"[PIPELINE] LangGraph workflow completed successfully")
            
            await self._emit_progress("analysis_complete", "Analysis completed successfully")
            logger.info(f"[PIPELINE] Pipeline execution completed successfully for: {company_name}")
            return final_state
            
        except Exception as e:
            logger.error(f"[PIPELINE] CRITICAL: Pipeline execution failed for {company_name}: {type(e).__name__}: {str(e)}", exc_info=True)
            await self._emit_progress("analysis_failed", f"Analysis failed: {str(e)}")
            raise

