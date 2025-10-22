"""
HTTP Wrapper for MCP Server
Allows the web frontend to communicate with MCP tools via REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mcp_builder_server as mcp_server

# Create FastAPI app
app = FastAPI(title="MCP Builder API")

# Enable CORS so frontend can call this from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models (what data the frontend sends)
class ArchitectureRequest(BaseModel):
    instructions: str

class ImageRequest(BaseModel):
    instructions: str
    style: str = "realistic"

class FullBuildRequest(BaseModel):
    instructions: str


# API Endpoints - these are what the frontend calls

@app.post("/mcp/tools/generate_architecture")
async def api_generate_architecture(req: ArchitectureRequest):
    """
    Endpoint: Creates architecture diagram from instructions
    Frontend calls this when user clicks "Generate Architecture"
    """
    try:
        result = mcp_server.generate_architecture(req.instructions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/tools/generate_image")
async def api_generate_image(req: ImageRequest):
    """
    Endpoint: Creates AI image from instructions
    Frontend calls this when user clicks "Generate Images"
    """
    try:
        result = mcp_server.generate_image(req.instructions, req.style)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/tools/full_build")
async def api_full_build(req: FullBuildRequest):
    """
    Endpoint: Complete build - architecture + images
    Frontend calls this when user clicks "Full Build"
    """
    try:
        result = mcp_server.full_build(req.instructions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Check if server is running"""
    return {"status": "healthy", "service": "MCP Builder API"}


if __name__ == "__main__":
    import uvicorn
    # Run the HTTP server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
