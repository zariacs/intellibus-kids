from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="NutriLab APIs", 
              description="AI service persons suffering with IBS",
              version="0.0.1")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI service


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
    
    
    return ""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 