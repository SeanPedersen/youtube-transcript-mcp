# youtube-transcript-mcp

Transcribe YouTube videos for LLM chat apps.

## Usage

### Tools Available

1. **`transcribe`** - Returns the full transcript as text
   - Example: "Transcribe https://www.youtube.com/watch?v=uB9yZenVLzg"

2. **`transcribe_to_file`** - Saves transcript to a file and returns confirmation
   - Example: "Save transcript of https://www.youtube.com/watch?v=uB9yZenVLzg to transcript.txt"
   - Optional `output_file` parameter (defaults to `transcript_{video_id}.txt`)
   - Files are saved in current directory only for security

## Install

- Install [Claude Desktop](https://claude.ai/download)
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) 
- Clone repo: `git clone https://github.com/SeanPedersen/youtube-transcript-mcp`
- `cd youtube-transcript-mcp/`
- Setup environment: `uv venv && uv pip install -r pyproject.toml && source .venv/bin/activate`
- Install the MCP server: `fastmcp install claude-desktop mcp_server.py --with youtube-transcript-api`
- Restart Claude Desktop

## MCP JSON Config
```json
"YouTube transcription service": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "youtube-transcript-api",
        "fastmcp",
        "run",
        "$INSERT_PATH/youtube-transcript-mcp/mcp_server.py"
      ],
      "env": {},
      "transport": "stdio"
    }
```
