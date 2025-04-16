
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import os
from datetime import datetime
import re

from app.models.request_models import AIRequest
from app.models.response_models import AIResponse
from app.services.form_analyzer import analyze_form
from app.services.response_generator import generate_responses
from app.services.page_analyzer import analyze_page

app = FastAPI(title="CareerSpark AI Service", description="AI Service for Job Application Automation")

# Configuration
API_PORT = int(os.environ.get("API_PORT", 8000))

# API routes
@app.get("/")
def read_root():
    return {"status": "ok", "service": "CareerSpark AI Service"}

@app.post("/analyze-form", response_model=AIResponse)
async def api_analyze_form(request: AIRequest):
    """Analyze the form structure and suggest actions"""
    return await analyze_form(request)

@app.post("/generate-responses", response_model=AIResponse)
async def api_generate_responses(request: AIRequest):
    """Generate responses for job application form fields"""
    return await generate_responses(request)

@app.post("/analyze-page", response_model=AIResponse)
async def api_analyze_page(request: dict):
    """Analyze page content to determine if submission is complete or which button to click"""
    page_content = request.get("pageContent", "")
    job_application_id = request.get("jobApplicationId")
    
    return await analyze_page(page_content, job_application_id)

if __name__ == "__main__":
    print(f"Starting CareerSpark AI Service on port {API_PORT}")
    uvicorn.run("main:app", host="0.0.0.0", port=API_PORT, reload=True)