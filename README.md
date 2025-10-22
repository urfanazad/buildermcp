# 🏗️ AI Builder - MCP Server Setup Guide

## What This Does
You upload text instructions (like "build a house with 3 rooms") and it:
1. Creates architecture diagrams showing the structure
2. Generates AI images of what it looks like
3. Gives you multiple views (exterior, blueprint, interior)

## Files Explained (in plain English)

### 1. `mcp_builder_server.py` - The Brain
This is the MCP server with 3 main tools:
- **generate_architecture()** - Takes your text → Makes a diagram
- **generate_image()** - Takes your text → Makes AI pictures  
- **full_build()** - Does both at once

Each tool uses Claude to understand your instructions, then generates the output.

### 2. `frontend.html` - The Interface
Beautiful web page where you:
- Type your instructions
- Click buttons to generate
- See the results (diagrams and images)

### 3. `http_wrapper.py` - The Bridge
Connects the frontend to the MCP server so they can talk to each other via HTTP.

### 4. `requirements.txt` - The Dependencies
List of Python packages you need to install.

## Setup Steps

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Set Your API Keys
You need two API keys:

1. **Anthropic API Key** (for Claude)
   - Get it from: https://console.anthropic.com/
   - Set it: `export ANTHROPIC_API_KEY="your-key-here"`

2. **OpenAI API Key** (for DALL-E image generation)
   - Get it from: https://platform.openai.com/
   - Set it: `export OPENAI_API_KEY="your-key-here"`

On Windows use `set` instead of `export`.

### Step 3: Run the Server
```bash
python http_wrapper.py
```

You should see: "Uvicorn running on http://0.0.0.0:8000"

### Step 4: Open the Frontend
Double-click `frontend.html` or open it in your browser.

## How to Use

1. **Type instructions** in the text box, for example:
   - "Build a modern 2-story house with 3 bedrooms, garage, and pool"
   - "Design a mobile app with login, home, and profile screens"
   - "Create a treehouse with rope ladder and slide"

2. **Click a button:**
   - 📐 Generate Architecture = Just the diagram
   - 🎨 Generate Images = Just the pictures
   - ⚡ Full Build = Everything at once

3. **Wait** for the AI to work (15-30 seconds)

4. **View results** - diagrams and images appear below

## Troubleshooting

**"Connection refused" error?**
- Make sure the server is running (`python http_wrapper.py`)

**"API key not found" error?**
- Set your environment variables correctly

**Images not generating?**
- Check your OpenAI API key
- Make sure you have credits in your OpenAI account

**Diagrams look weird?**
- The AI sometimes needs clearer instructions
- Try being more specific: "3-bedroom house with kitchen on first floor"

## Cost Estimates
- Claude API: ~$0.01 per request
- DALL-E 3: ~$0.04 per image
- Full build (1 diagram + 3 images): ~$0.13 total

## Advanced: Using Direct MCP (Optional)

If you want to use this as a pure MCP server without HTTP:

```bash
# Run as MCP server (uses stdio)
python mcp_builder_server.py
```

Then connect it to Claude Desktop or any MCP client.

## What Makes This "Cutting Edge"?

1. **FastMCP Framework** - Modern, minimal code compared to raw MCP
2. **AI-Enhanced Prompts** - Claude improves your instructions before generating
3. **Multi-Modal Output** - Combines diagrams (structure) + images (visuals)
4. **Modular Tools** - Use individual tools or combine them
5. **Clean Architecture** - Each file does ONE thing well

## Next Steps / Ideas

- Add more image styles (watercolor, pixel art, etc.)
- Generate 3D models instead of just images
- Save results to a database
- Add file upload for instruction documents
- Create video walkthroughs of the designs

Enjoy building! 🚀
