from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, validator
import uvicorn
from typing import Dict, Any, Optional

# Import the TechDetector class from the website_tech_detector.py file
from website_tech_detector import TechDetector

# Create FastAPI app
app = FastAPI(
    title="Website Technology Detector API",
    description="API to detect technologies used by websites",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the TechDetector
detector = TechDetector()

# Define the request model
class UrlRequest(BaseModel):
    url: str
    
    @validator('url')
    def validate_url(cls, v):
        # Simple URL validation
        if not v.startswith(('http://', 'https://')):
            v = 'http://' + v
        return v

# Define the response model
class TechResponse(BaseModel):
    classification: Dict[str, Any]
    technologies: Dict[str, Any]
    url: str
    execution_time: float

@app.get("/")
async def read_root():
    return {"message": "Website Technology Detector API", "usage": "POST /detect with URL in request body"}

@app.post("/detect", response_model=TechResponse)
async def detect_technologies(request: UrlRequest):
    try:
        import time
        start_time = time.time()
        
        # Detect technologies
        results = detector.detect_tech(request.url)
        
        if not results:
            raise HTTPException(status_code=404, detail="No technologies detected or an error occurred")
        
        # Extract classification
        classification = results.pop("classification", {})
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        return {
            "classification": classification,
            "technologies": results,
            "url": request.url,
            "execution_time": round(execution_time, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting technologies: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 