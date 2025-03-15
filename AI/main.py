from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from services.ai_service import AIService

# Initialize FastAPI app
app = FastAPI(title="Intellibus Kids AI Service", 
              description="AI service for kids learning platform",
              version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI service
ai_service = AIService()

@app.get("/")
async def root():
    # Simple health check endpoint
    return {"message": "AI Service is operational", "status": "healthy"}

@app.post("/api/generate")
async def generate_response(request: Request):
    # Get request JSON body
    data = await request.json()
    query = data.get("query", "")
    
    # Process the query using the AI service
    response = ai_service.process_query(query)
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 