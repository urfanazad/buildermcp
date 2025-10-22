"""
HTTP Wrapper for MCP Server
Allows the web frontend to communicate with MCP tools via REST API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import mcp_builder_server as mcp_server
import os

# Create a rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(title="MCP Builder API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Enable CORS so frontend can call this from browser
# In a production environment, this should be a specific, trusted domain
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "GET"],
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
@limiter.limit("5/minute")
async def api_generate_architecture(req: ArchitectureRequest, request: Request):
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
@limiter.limit("5/minute")
async def api_generate_image(req: ImageRequest, request: Request):
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
@limiter.limit("3/minute")
async def api_full_build(req: FullBuildRequest, request: Request):
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
