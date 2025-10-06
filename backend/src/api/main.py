from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Promo Creator API",
    description="Generate promotional videos for restaurants from Google Maps URLs",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class VideoGenerationRequest(BaseModel):
    google_maps_url: str
    style: str = "casual"  # luxury, casual, street_food
    duration: int = 30  # seconds

class VideoGenerationResponse(BaseModel):
    task_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"message": "AI Promo Creator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-video", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    Generate a promotional video from a Google Maps URL
    """
    try:
        # TODO: Implement video generation workflow
        # This will orchestrate the agents: MapParser -> MenuExtractor -> ScriptGenerator -> VideoGenerator
        
        return VideoGenerationResponse(
            task_id="temp-task-id",
            status="initiated",
            message="Video generation started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}")
async def get_generation_status(task_id: str):
    """
    Get the status of a video generation task
    """
    # TODO: Implement status checking from database
    return {"task_id": task_id, "status": "processing", "progress": 45}

@app.get("/download/{task_id}")
async def download_video(task_id: str):
    """
    Download the generated video
    """
    # TODO: Implement video download from S3
    raise HTTPException(status_code=404, detail="Video not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)