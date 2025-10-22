"""
MCP Image & Architecture Builder Server
Takes text instructions and creates visual representations
"""

from mcp.server.fastmcp import FastMCP
import anthropic
import re
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the MCP server with a name
mcp = FastMCP("Builder Agent")

# Set up API clients (you'll need to add your API keys)
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")


def _sanitize_instructions(instructions: str) -> str:
    """
    Sanitizes user input to mitigate prompt injection.
    It removes phrases and characters that are commonly used to manipulate LLMs.
    """
    # Remove control characters and backticks
    instructions = re.sub(r'[\x00-\x1f`]', '', instructions)

    # List of injection phrases (case-insensitive)
    injection_phrases = [
        "ignore the above", "ignore your previous instructions",
        "disregard the above", "forget the above", "new instructions",
        "new prompt", "system prompt", "your instructions are",
        "act as", "roleplay as", "print your instructions",
        "what are your instructions", "repeat the above",
    ]

    # Remove the phrases
    for phrase in injection_phrases:
        instructions = re.sub(phrase, '', instructions, flags=re.IGNORECASE)

    return instructions.strip()


@mcp.tool()
def generate_architecture(instructions: str) -> dict:
    """
    Takes instructions and creates a Mermaid diagram showing the architecture/structure
    
    Args:
        instructions: Text describing what to build (e.g., "build a house with 3 rooms")
    
    Returns:
        Dictionary with mermaid code and explanation
    """
    
    if not ANTHROPIC_KEY:
        return {"error": "ANTHROPIC_API_KEY is not set. Please configure your API keys."}

    # Sanitize user input to prevent prompt injection
    sanitized_instructions = _sanitize_instructions(instructions)

    # Use Claude to convert instructions into structured architecture
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    
    prompt = f"""Convert these instructions into a Mermaid flowchart diagram:
    
Instructions: {sanitized_instructions}

Create a clear, hierarchical Mermaid diagram showing the structure and flow.
Return ONLY the mermaid code, no explanation."""
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    mermaid_code = response.content[0].text
    
    return {
        "mermaid": mermaid_code,
        "instructions": instructions,
        "type": "architecture_diagram"
    }


@mcp.tool()
def generate_image(instructions: str, style: str = "realistic") -> dict:
    """
    Creates an AI-generated image based on instructions
    
    Args:
        instructions: What to create (e.g., "modern house with garden")
        style: Art style - "realistic", "blueprint", "3d-render", "sketch"
    
    Returns:
        Dictionary with image URL and metadata
    """
    
    if not ANTHROPIC_KEY or not OPENAI_KEY:
        return {"error": "API keys are not set. Please configure ANTHROPIC_API_KEY and OPENAI_API_KEY."}

    # Sanitize user input to prevent prompt injection
    sanitized_instructions = _sanitize_instructions(instructions)

    # Use Claude to enhance the prompt for better image generation
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    
    enhance_prompt = f"""Transform this into a detailed image generation prompt:

Instructions: {sanitized_instructions}
Style: {style}

Create a concise, vivid prompt (max 200 chars) for DALL-E. Be specific about colors, perspective, lighting."""
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[{"role": "user", "content": enhance_prompt}]
    )
    
    enhanced_prompt = response.content[0].text
    
    # Generate image using DALL-E
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "dall-e-3",
        "prompt": enhanced_prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard"
    }
    
    img_response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=data
    )
    
    if img_response.status_code == 200:
        image_url = img_response.json()["data"][0]["url"]
        return {
            "image_url": image_url,
            "prompt_used": enhanced_prompt,
            "original_instructions": instructions,
            "style": style
        }
    else:
        return {"error": f"Image generation failed: {img_response.text}"}


@mcp.tool()
def full_build(instructions: str) -> dict:
    """
    Complete pipeline: Takes instructions and generates both architecture AND images
    
    Args:
        instructions: Full text describing what to build
    
    Returns:
        Dictionary containing architecture diagram and multiple image views
    """
    
    # Step 1: Generate architecture
    architecture = generate_architecture(instructions)
    
    # Step 2: Generate multiple views
    images = {
        "exterior": generate_image(f"{instructions} - exterior view", "realistic"),
        "blueprint": generate_image(f"{instructions} - technical blueprint", "blueprint"),
        "interior": generate_image(f"{instructions} - interior view", "realistic")
    }
    
    return {
        "architecture": architecture,
        "images": images,
        "status": "complete",
        "instructions": instructions
    }


# Add a resource to provide examples
@mcp.resource("mcp://examples/usage")
def get_examples() -> str:
    """Provides example instructions for users"""
    return """
    Example Instructions:
    
    1. "Build a modern 2-story house with a garage, 3 bedrooms, kitchen, and living room"
    2. "Create a mobile app with login, dashboard, and settings screens"
    3. "Design a database schema for an e-commerce store with users, products, and orders"
    
    Use tools:
    - generate_architecture(instructions) - for diagrams only
    - generate_image(instructions, style) - for images only  
    - full_build(instructions) - for everything at once
    """


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
