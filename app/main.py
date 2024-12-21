from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from pathlib import Path
from app.services.ai_service import AIService
from app.services.file_service import FileService

# Initialize FastAPI app
app = FastAPI(
    title="UI Generator API",
    description="API for generating UI designs from app ideas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Store generated designs in memory
generated_designs = {}

# Mount static files
static_path = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Initialize templates
templates = Jinja2Templates(directory=str(static_path))

class UIGenerationRequest(BaseModel):
    """
    Request model for UI generation
    """
    prompt: str
    tech_stack: str = "html-tailwind"
    style_preferences: dict = {}

class UIGenerationResponse(BaseModel):
    """
    Response model for UI generation
    """
    html: str
    design_id: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the UI generator interface.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate", response_model=UIGenerationResponse)
async def generate_ui(request: UIGenerationRequest) -> dict:
    """
    Generate UI based on prompt.
    
    Parameters:
    - prompt: The app idea or description
    - tech_stack: The selected tech stack
    - style_preferences: Optional styling preferences
    
    Returns:
    - dict containing generated HTML and design ID
    """
    try:
        # Generate UI using Claude
        preview_html, generated_code = await AIService.analyze_app_idea_with_claude(request.prompt, request.tech_stack)
        
        # Store the result with a unique ID
        design_id = FileService.generate_unique_id()
        generated_designs[design_id] = {
            'html': preview_html,
            'code': generated_code,
            'tech_stack': request.tech_stack
        }
        
        return {"html": preview_html, "design_id": design_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{design_id}")
async def download_code(design_id: str):
    """
    Download the generated UI code as a zip file
    """
    try:
        # Get the stored design
        if design_id not in generated_designs:
            raise HTTPException(status_code=404, detail="Design not found")
        
        design = generated_designs[design_id]
        tech_stack = design['tech_stack']
        
        # Create appropriate files based on tech stack
        if tech_stack == "react-tailwind":
            # Extract React components and types
            content = design['code']  # Use the generated code, not the preview HTML
            zip_path, filename = FileService.create_react_project(content)
        else:
            # Create simple HTML file
            zip_path, filename = FileService.create_zip_from_html(design['code'])
        
        # Return the zip file
        return FileResponse(
            path=zip_path,
            filename=filename,
            media_type='application/zip',
            background=lambda: FileService.cleanup_file(zip_path)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
