from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api")

# Determine if we're in production
is_production = os.getenv("ENVIRONMENT", "development").lower() == "production"

# Setup paths and environment variables
def setup_environment():
    """Set up the environment for the API to run properly"""
    # Determine the AI directory path
    current_dir = Path(__file__).resolve().parent
    ai_dir = current_dir.parent
    
    # Add AI directory to path if not already there
    if str(ai_dir) not in sys.path:
        sys.path.insert(0, str(ai_dir))
    
    # In development, load from .env file
    if not is_production:
        env_path = ai_dir / '.env'
        if env_path.exists():
            logger.info(f"Loading environment variables from {env_path}")
            load_dotenv(dotenv_path=env_path)
        else:
            logger.warning(f".env file not found at {env_path}")
    
    # Verify critical environment variables
    required_vars = ["GEMINI_API_KEY", "MODEL_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        if not is_production:
            # Only exit in development - in production, let it fail more gracefully
            sys.exit(1)

# Set up the environment before importing other modules
setup_environment()

# Import router after environment is set up
from api.patient_report import router as patient_report_router

# Initialize FastAPI app
app = FastAPI(
    title="Medical Report API",
    description="API for generating medical reports and condition-specific meal plans",
    version="0.1.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(patient_report_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Report API. Visit /docs for API documentation."}

# Health check endpoint
@app.get("/health")
async def health_check():
    # Check if we can access the API key (without revealing it)
    api_key_available = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "healthy" if api_key_available else "degraded",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_key_configured": api_key_available
    }

# Run the application if executed directly (development only)
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run("api.main:app", host=host, port=port, reload=not is_production) 