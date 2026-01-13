from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# Import analyses lazily to avoid dependency issues at startup
# analyses will be imported when needed
import logging
import logging.handlers
from pathlib import Path
import time

# Set up logging configuration
# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

# Master log file path - never deleted
master_log_path = log_dir / "app_master.log"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(name)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        # Console handler
        logging.StreamHandler(),
        # File handler - append to master log (never delete)
        logging.handlers.RotatingFileHandler(
            master_log_path,
            maxBytes=10*1024*1024,  # 10MB per file
            backupCount=100,  # Keep 100 backup files
            encoding='utf-8'
        )
    ]
)

logger = logging.getLogger(__name__)
logger.info("="*80)
logger.info("Strategic Futures AI - Application Started")
logger.info(f"Master log file: {master_log_path}")
logger.info("="*80)

# Test database connection on startup
try:
    from app.core.database import engine
    with engine.connect() as conn:
        logger.info("Database connection successful")
        logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'}")
except Exception as e:
    logger.error(f"Database connection failed: {str(e)}", exc_info=True)
    logger.warning("Application will continue, but database operations may fail")

app = FastAPI(
    title="Strategic Futures AI API",
    description="API for strategic futures analysis using LangGraph and AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request error logging middleware (only logs errors, not every request)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[REQUEST] {request.method} {request.url.path} - ✗ UNHANDLED EXCEPTION: {type(e).__name__}: {str(e)} - Time: {process_time:.3f}s", exc_info=True)
        raise
    except BaseException as e:  # Catch ALL exceptions including KeyboardInterrupt, SystemExit, etc.
        process_time = time.time() - start_time
        logger.critical(f"[REQUEST] {request.method} {request.url.path} - ✗ CRITICAL BASE EXCEPTION: {type(e).__name__}: {str(e)} - Time: {process_time:.3f}s", exc_info=True)
        raise

# Lazy import analyses router to avoid pydantic/langsmith compatibility issues
def include_analyses_router():
    try:
        from app.api.routes import analyses
        app.include_router(analyses.router)
        logger.info("Analyses router loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to load analyses router: {str(e)}")
        logger.warning("Analyses features will not be available")

include_analyses_router()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Strategic Futures AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

