import uvicorn
from . import app

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {
        "status": "healthy",
        "service": "nutri lab API",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        port=8000,
        reload=True,  # Enable auto-reload during development
        workers=1,    # Number of worker processes
        log_level="info",
    )