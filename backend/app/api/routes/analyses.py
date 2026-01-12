from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import logging
import sys
import traceback
from datetime import datetime

from app.core.database import get_db
from app.models.analysis import Analysis, AnalysisStatus
from app.models.scenario import Scenario
from app.models.strategy import Strategy
from app.models.search_query import SearchQuery
# Import AnalysisPipeline lazily to avoid dependency issues at module import time
# AnalysisPipeline = None  # Will be imported when needed

router = APIRouter(prefix="/api/analyses", tags=["analyses"])

logger = logging.getLogger(__name__)

# Store active analysis jobs and their progress callbacks
active_analyses: Dict[int, Dict[str, Any]] = {}


class AnalysisCreate(BaseModel):
    company_name: str


class AnalysisResponse(BaseModel):
    id: int
    company_name: str
    status: str
    company_context: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScenarioResponse(BaseModel):
    id: int
    scenario_number: int
    title: str
    description: str
    timeline: Optional[str] = None
    key_assumptions: Optional[str] = None
    likelihood: Optional[float] = None

    class Config:
        from_attributes = True


class StrategyResponse(BaseModel):
    id: int
    name: str
    description: str
    expected_impact: Optional[str] = None
    key_risks: Optional[str] = None

    class Config:
        from_attributes = True


class AnalysisDetailResponse(BaseModel):
    id: int
    company_name: str
    status: str
    company_context: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    scenarios: List[ScenarioResponse] = []
    strategies: Dict[str, List[StrategyResponse]] = {}

    class Config:
        from_attributes = True


def progress_callback_factory(analysis_id: int, event_queue: Optional[asyncio.Queue] = None):
    """Factory for creating progress callbacks that dynamically check for event queue"""
    async def callback(event_type: str, message: str):
        try:
            # Dynamically get the event queue in case it was created after the callback
            # This handles the race condition where SSE stream connects after task starts
            queue = event_queue
            if not queue and analysis_id in active_analyses:
                queue = active_analyses[analysis_id].get("event_queue")
            
            if queue:
                await queue.put({
                    "event": event_type,
                    "data": {
                        "message": message,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
                msg_preview = (message or "")[:50] if message else ""
                logger.debug(f"[CALLBACK {analysis_id}] Sent event: {event_type} - {msg_preview}")
            else:
                msg_preview = (message or "")[:50] if message else ""
                logger.debug(f"[CALLBACK {analysis_id}] No event queue available for event: {event_type} - {msg_preview}")
        except Exception as e:
            logger.error(f"[CALLBACK {analysis_id}] Error in progress callback: {e}", exc_info=True)
    return callback


async def run_analysis_task(
    analysis_id: int,
    company_name: str
):
    """Background task to run the analysis pipeline"""
    logger.info(f"[ANALYSIS {analysis_id}] Starting analysis task for company: {company_name}")
    # Get fresh database session for background task
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"[ANALYSIS {analysis_id}] ERROR: Analysis not found in database")
            return
        
        logger.info(f"[ANALYSIS {analysis_id}] Found analysis, current status: {analysis.status}")
        # Update status to processing
        analysis.status = AnalysisStatus.PROCESSING  # type: ignore
        db.commit()
        logger.info(f"[ANALYSIS {analysis_id}] Status updated to PROCESSING")
        
        # Get event queue for this analysis (may be None if SSE hasn't connected yet)
        event_queue = active_analyses.get(analysis_id, {}).get("event_queue")
        if event_queue:
            logger.info(f"[ANALYSIS {analysis_id}] Event queue found, SSE will be available")
            # Send initial processing event
            try:
                await event_queue.put({
                    "event": "status",
                    "data": {
                        "status": "processing",
                        "message": "Analysis started, initializing pipeline...",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
            except Exception as e:
                logger.warning(f"[ANALYSIS {analysis_id}] Failed to send initial status event: {e}")
        else:
            logger.info(f"[ANALYSIS {analysis_id}] No event queue yet (SSE may connect later), callback will check dynamically")
        
        # Import AnalysisPipeline lazily to avoid dependency issues
        logger.info(f"[ANALYSIS {analysis_id}] Importing AnalysisPipeline...")
        try:
            from app.agents.pipeline import AnalysisPipeline
            logger.info(f"[ANALYSIS {analysis_id}] AnalysisPipeline imported successfully")
        except Exception as e:
            logger.error(f"[ANALYSIS {analysis_id}] CRITICAL: Failed to import AnalysisPipeline: {str(e)}", exc_info=True)
            analysis.status = AnalysisStatus.FAILED  # type: ignore
            db.commit()
            return
        
        # Create pipeline with progress callback (always create callback, it will check for queue dynamically)
        logger.info(f"[ANALYSIS {analysis_id}] Creating pipeline instance...")
        try:
            # Always create callback - it will dynamically check for event queue
            # This handles race condition where SSE connects after task starts
            pipeline = AnalysisPipeline(
                progress_callback=progress_callback_factory(analysis_id, event_queue)  # type: ignore
            )
            logger.info(f"[ANALYSIS {analysis_id}] Pipeline instance created successfully with progress callback")
        except Exception as e:
            logger.error(f"[ANALYSIS {analysis_id}] CRITICAL: Failed to create pipeline: {str(e)}", exc_info=True)
            analysis.status = AnalysisStatus.FAILED  # type: ignore
            db.commit()
            return
        
        # Run the pipeline
        logger.info(f"[ANALYSIS {analysis_id}] Starting pipeline execution...")
        try:
            result = await pipeline.run(company_name)
            logger.info(f"[ANALYSIS {analysis_id}] Pipeline execution completed successfully")
        except Exception as e:
            logger.error(f"[ANALYSIS {analysis_id}] CRITICAL: Pipeline execution failed: {str(e)}", exc_info=True)
            raise  # Re-raise to be caught by outer exception handler
        
        # Validate result
        if not result:
            raise ValueError("Pipeline returned None or empty result")
        if "company_context" not in result:
            logger.warning(f"[ANALYSIS {analysis_id}] WARNING: Result missing company_context")
        
        logger.info(f"[ANALYSIS {analysis_id}] Saving results to database...")
        # Save results to database
        analysis.company_context = result.get("company_context", "")  # type: ignore
        analysis.status = AnalysisStatus.COMPLETED  # type: ignore
        
        # Save search queries
        search_queries_count = 0
        for question, results in result.get("search_results", {}).items():
            search_query = SearchQuery(
                analysis_id=analysis_id,
                query=question,
                results=results
            )
            db.add(search_query)
            search_queries_count += 1
        logger.info(f"[ANALYSIS {analysis_id}] Saved {search_queries_count} search queries")
        
        # Save scenarios
        scenarios_count = 0
        strategies_count = 0
        for scenario_data in result.get("scenarios", []):
            scenario = Scenario(
                analysis_id=analysis_id,
                scenario_number=scenario_data.get("scenario_number", 0),
                title=scenario_data.get("title", ""),
                description=scenario_data.get("description", ""),
                timeline=scenario_data.get("timeline"),
                key_assumptions=scenario_data.get("key_assumptions"),
                likelihood=scenario_data.get("likelihood")
            )
            db.add(scenario)
            db.flush()  # Get scenario.id
            scenarios_count += 1
            
            # Save strategies for this scenario
            scenario_key = scenario_data.get("title", f"scenario_{scenario.scenario_number}")
            strategies_data = result.get("strategies", {}).get(scenario_key, [])
            
            for strategy_data in strategies_data:
                strategy = Strategy(
                    scenario_id=scenario.id,
                    name=strategy_data.get("name", ""),
                    description=strategy_data.get("description", ""),
                    expected_impact=strategy_data.get("expected_impact"),
                    key_risks=strategy_data.get("key_risks")
                )
                db.add(strategy)
                strategies_count += 1
        
        logger.info(f"[ANALYSIS {analysis_id}] Saved {scenarios_count} scenarios and {strategies_count} strategies")
        
        db.commit()
        logger.info(f"[ANALYSIS {analysis_id}] Database commit successful")
        
        # Send completion event
        if event_queue:
            try:
                await event_queue.put({
                    "event": "analysis_complete",
                    "data": {
                        "message": "Analysis completed successfully",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
                logger.info(f"[ANALYSIS {analysis_id}] Completion event sent to SSE queue")
            except Exception as e:
                logger.warning(f"[ANALYSIS {analysis_id}] Failed to send completion event: {e}")
        
        logger.info(f"[ANALYSIS {analysis_id}] ✓ Analysis completed successfully")
        
    except asyncio.CancelledError as e:
        logger.error(f"[ANALYSIS {analysis_id}] ✗ TASK CANCELLED (likely timeout): {e}", exc_info=True)
        # Update status to failed
        try:
            db.rollback()
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED  # type: ignore
                db.commit()
                logger.info(f"[ANALYSIS {analysis_id}] Status updated to FAILED due to cancellation")
        except Exception as db_error:
            logger.error(f"[ANALYSIS {analysis_id}] Failed to update status after cancellation: {db_error}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"[ANALYSIS {analysis_id}] ✗ CRITICAL ERROR in analysis task: {type(e).__name__}: {str(e)}", exc_info=True)
        
        # Update status to failed
        try:
            # Refresh the analysis object
            db.rollback()  # Rollback any pending changes
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED  # type: ignore
                db.commit()
                logger.info(f"[ANALYSIS {analysis_id}] Status updated to FAILED in database")
            else:
                logger.error(f"[ANALYSIS {analysis_id}] Could not find analysis to update status")
        except Exception as db_error:
            logger.error(f"[ANALYSIS {analysis_id}] CRITICAL: Failed to update analysis status to FAILED: {db_error}", exc_info=True)
        
        # Send failure event
        try:
            event_queue = active_analyses.get(analysis_id, {}).get("event_queue")
            if event_queue:
                await event_queue.put({
                    "event": "analysis_failed",
                    "data": {
                        "message": f"Analysis failed: {str(e)}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
                logger.info(f"[ANALYSIS {analysis_id}] Failure event sent to SSE queue")
        except Exception as sse_error:
            logger.warning(f"[ANALYSIS {analysis_id}] Failed to send failure event to SSE: {sse_error}")
        
        # Re-raise to be caught by task wrapper
        raise
    finally:
        try:
            db.close()
            logger.debug(f"[ANALYSIS {analysis_id}] Database session closed")
        except Exception as e:
            logger.error(f"[ANALYSIS {analysis_id}] Error closing database session: {e}")


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_data: AnalysisCreate,
    db: Session = Depends(get_db)
):
    """Create a new analysis and start background processing"""
    logger.info(f"[CREATE] Received request to create analysis for company: {analysis_data.company_name}")
    
    try:
        # Create analysis record
        logger.info(f"[CREATE] Creating analysis record in database...")
        analysis = Analysis(
            company_name=analysis_data.company_name,
            status=AnalysisStatus.PENDING
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        logger.info(f"[CREATE] Analysis record created with ID: {analysis.id}")
        
        # Create event queue for SSE
        logger.info(f"[CREATE] Creating event queue for SSE...")
        event_queue = asyncio.Queue()
        active_analyses[analysis.id] = {  # type: ignore
            "event_queue": event_queue,
            "analysis": analysis
        }
        logger.info(f"[CREATE] Event queue created and stored in active_analyses")
    
        # Start background task using asyncio.create_task for proper async handling
        # Add error callback to catch any unhandled exceptions
        async def task_wrapper():
            try:
                await run_analysis_task(analysis.id, analysis_data.company_name)  # type: ignore
            except asyncio.CancelledError as e:
                logger.error(f"[CREATE] ✗ TASK CANCELLED for analysis {analysis.id}: {e}", exc_info=True)
                logger.error(f"[CREATE] Full traceback:\n{traceback.format_exc()}")
                # Try to update status in database
                try:
                    from app.core.database import SessionLocal
                    task_db = SessionLocal()
                    try:
                        task_analysis = task_db.query(Analysis).filter(Analysis.id == analysis.id).first()
                        if task_analysis:
                            task_analysis.status = AnalysisStatus.FAILED  # type: ignore
                            task_db.commit()
                            logger.info(f"[CREATE] Updated analysis {analysis.id} status to FAILED after cancellation")
                    finally:
                        task_db.close()
                except Exception as db_err:
                    logger.error(f"[CREATE] Failed to update analysis status after cancellation: {db_err}", exc_info=True)
            except Exception as e:
                logger.error(f"[CREATE] ✗ CRITICAL: Unhandled exception in analysis task {analysis.id}: {type(e).__name__}: {str(e)}", exc_info=True)
                logger.error(f"[CREATE] Full traceback:\n{traceback.format_exc()}")
                # Try to update status in database
                try:
                    from app.core.database import SessionLocal
                    task_db = SessionLocal()
                    try:
                        task_analysis = task_db.query(Analysis).filter(Analysis.id == analysis.id).first()
                        if task_analysis:
                            task_analysis.status = AnalysisStatus.FAILED  # type: ignore
                            task_db.commit()
                            logger.info(f"[CREATE] Updated analysis {analysis.id} status to FAILED after unhandled exception")
                    finally:
                        task_db.close()
                except Exception as db_err:
                    logger.error(f"[CREATE] Failed to update analysis status after unhandled exception: {db_err}", exc_info=True)
            except BaseException as e:
                logger.critical(f"[CREATE] ✗ CRITICAL BASE EXCEPTION in analysis task {analysis.id}: {type(e).__name__}: {str(e)}", exc_info=True)
                logger.critical(f"[CREATE] Full traceback:\n{traceback.format_exc()}")
                # Try to update status in database
                try:
                    from app.core.database import SessionLocal
                    task_db = SessionLocal()
                    try:
                        task_analysis = task_db.query(Analysis).filter(Analysis.id == analysis.id).first()
                        if task_analysis:
                            task_analysis.status = AnalysisStatus.FAILED  # type: ignore
                            task_db.commit()
                            logger.info(f"[CREATE] Updated analysis {analysis.id} status to FAILED after base exception")
                    finally:
                        task_db.close()
                except Exception as db_err:
                    logger.error(f"[CREATE] Failed to update analysis status after base exception: {db_err}", exc_info=True)
        
        logger.info(f"[CREATE] Creating background task...")
        try:
            task = asyncio.create_task(task_wrapper())
            # Add done callback to log completion/failure
            def task_done_callback(fut):
                try:
                    fut.result()  # This will raise if the task failed
                    logger.info(f"[CREATE] Background task for analysis {analysis.id} completed successfully")
                except Exception as e:
                    logger.error(f"[CREATE] Background task for analysis {analysis.id} failed: {e}", exc_info=True)
            
            task.add_done_callback(task_done_callback)
            logger.info(f"[CREATE] ✓ Started background task for analysis {analysis.id}, company: {analysis_data.company_name}")
        except Exception as e:
            logger.error(f"[CREATE] CRITICAL: Failed to create background task for analysis {analysis.id}: {e}", exc_info=True)
            # Update analysis status to failed
            analysis.status = AnalysisStatus.FAILED  # type: ignore
            db.commit()
        
        logger.info(f"[CREATE] Returning analysis response with ID: {analysis.id}")
        return analysis
        
    except Exception as e:
        logger.error(f"[CREATE] CRITICAL ERROR in create_analysis endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create analysis: {str(e)}"
        )


@router.get("", response_model=List[AnalysisResponse])
async def list_analyses(
    db: Session = Depends(get_db)
):
    """List all analyses"""
    logger.info("[LIST] Received request to list all analyses")
    try:
        analyses = db.query(Analysis).order_by(desc(Analysis.created_at)).all()
        logger.info(f"[LIST] Found {len(analyses)} analyses in database")
        for a in analyses:
            logger.info(f"[LIST]   - ID: {a.id}, Company: {a.company_name}, Status: {a.status}")
        return analyses
    except Exception as e:
        logger.error(f"[LIST] ERROR listing analyses: {type(e).__name__}: {str(e)}", exc_info=True)
        raise


@router.get("/{analysis_id}", response_model=AnalysisDetailResponse)
async def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get analysis details with scenarios and strategies"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Get scenarios
    scenarios = db.query(Scenario).filter(
        Scenario.analysis_id == analysis_id
    ).order_by(Scenario.scenario_number).all()
    
    # Get strategies grouped by scenario
    strategies_dict = {}
    for scenario in scenarios:
        strategies = db.query(Strategy).filter(
            Strategy.scenario_id == scenario.id
        ).all()
        strategies_dict[scenario.title] = strategies
    
    return {
        "id": analysis.id,
        "company_name": analysis.company_name,
        "status": analysis.status.value,
        "company_context": analysis.company_context,
        "created_at": analysis.created_at,
        "updated_at": analysis.updated_at,
        "scenarios": scenarios,
        "strategies": strategies_dict
    }


@router.get("/{analysis_id}/stream")
async def stream_analysis_progress(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """SSE endpoint for real-time analysis progress"""
    # Verify analysis exists
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Get or create event queue
    if analysis_id not in active_analyses:
        event_queue = asyncio.Queue()
        active_analyses[analysis_id] = {
            "event_queue": event_queue,
            "analysis": analysis
        }
    else:
        event_queue = active_analyses[analysis_id]["event_queue"]
    
    async def event_generator():
        """Generate SSE events"""
        try:
            logger.debug(f"[STREAM {analysis_id}] Starting event generator, analysis status: {analysis.status.value}")
            
            # Send initial status
            yield f"event: status\n"
            yield f"data: {json.dumps({'status': analysis.status.value, 'message': 'Connected'})}\n\n"
            
            # If analysis is already completed or failed, send completion event immediately
            if analysis.status == AnalysisStatus.COMPLETED:  # type: ignore
                logger.debug(f"[STREAM {analysis_id}] Analysis already completed, sending immediate completion event")
                yield f"event: analysis_complete\n"
                yield f"data: {json.dumps({'message': 'Analysis completed successfully', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                return
            elif analysis.status == AnalysisStatus.FAILED:  # type: ignore
                logger.debug(f"[STREAM {analysis_id}] Analysis already failed, sending immediate failure event")
                yield f"event: analysis_failed\n"
                yield f"data: {json.dumps({'message': 'Analysis failed', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                return
            
            # Stream events from queue
            logger.debug(f"[STREAM {analysis_id}] Analysis in progress, streaming events from queue...")
            last_status_check = datetime.utcnow()
            consecutive_timeouts = 0
            while True:
                try:
                    # Wait for event with timeout (reduced to 3 seconds for more responsive status checks)
                    event_data = await asyncio.wait_for(event_queue.get(), timeout=3.0)
                    consecutive_timeouts = 0  # Reset timeout counter on successful event
                    
                    event_type = event_data.get("event", "message")
                    data = event_data.get("data", {})
                    
                    msg_preview = (data.get('message', '') or '')[:50]
                    logger.debug(f"[STREAM {analysis_id}] Sending event: {event_type} - {msg_preview}")
                    yield f"event: {event_type}\n"
                    yield f"data: {json.dumps(data)}\n\n"
                    
                    # Stop on completion or failure
                    if event_type in ["analysis_complete", "analysis_failed"]:
                        logger.debug(f"[STREAM {analysis_id}] Received {event_type}, closing stream")
                        break
                        
                except asyncio.TimeoutError:
                    consecutive_timeouts += 1
                    # Send keepalive and check if analysis status changed
                    try:
                        # Refresh analysis status from database periodically (every 2 seconds)
                        now = datetime.utcnow()
                        if (now - last_status_check).total_seconds() >= 2.0:
                            db.refresh(analysis)
                            last_status_check = now
                            
                            logger.debug(f"[STREAM {analysis_id}] Status check: {analysis.status.value}, consecutive timeouts: {consecutive_timeouts}")
                            
                            # Send status update if it changed
                            if analysis.status == AnalysisStatus.PROCESSING:  # type: ignore
                                yield f"event: status\n"
                                yield f"data: {json.dumps({'status': 'processing', 'message': 'Analysis in progress...'})}\n\n"
                            elif analysis.status == AnalysisStatus.COMPLETED:  # type: ignore
                                logger.debug(f"[STREAM {analysis_id}] Analysis completed (detected via status check), sending completion event")
                                yield f"event: analysis_complete\n"
                                yield f"data: {json.dumps({'message': 'Analysis completed successfully', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                                break
                            elif analysis.status == AnalysisStatus.FAILED:  # type: ignore
                                logger.debug(f"[STREAM {analysis_id}] Analysis failed (detected via status check), sending failure event")
                                yield f"event: analysis_failed\n"
                                yield f"data: {json.dumps({'message': 'Analysis failed', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                                break
                        
                        yield f": keepalive\n\n"
                    except Exception as refresh_error:
                        logger.warning(f"[STREAM {analysis_id}] Error refreshing analysis status: {refresh_error}", exc_info=True)
                        yield f": keepalive\n\n"
                    
        except Exception as e:
            logger.error(f"[STREAM {analysis_id}] Error in event generator: {type(e).__name__}: {str(e)}", exc_info=True)
            yield f"event: error\n"
            yield f"data: {json.dumps({'message': str(e)})}\n\n"
        finally:
            # Only cleanup if analysis is completed or failed
            # Don't cleanup if client disconnects while analysis is still running
            try:
                db.refresh(analysis)
                if analysis.status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
                    if analysis_id in active_analyses:
                        del active_analyses[analysis_id]
                        logger.debug(f"[STREAM {analysis_id}] Cleaned up active_analyses entry (analysis {analysis.status.value})")
                else:
                    logger.debug(f"[STREAM {analysis_id}] Keeping active_analyses entry (analysis still {analysis.status.value})")
            except Exception as cleanup_error:
                logger.warning(f"[STREAM {analysis_id}] Error during cleanup: {cleanup_error}")
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/{analysis_id}/status", response_model=AnalysisResponse)
async def get_analysis_status(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """Get current analysis status (polling fallback)"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return analysis

