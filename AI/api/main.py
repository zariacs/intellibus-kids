from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.patient_report import router as patient_report_router

# Initialize FastAPI app
app = FastAPI(
    title="Medical Report API",
    description="API for generating medical reports and condition-specific meal plans",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
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
    return {"status": "healthy"}

# Run the application if executed directly
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True) 