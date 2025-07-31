# youtube-transcript-mcp

Transcribe YouTube videos for LLM chat apps.

## Install

- Install [Claude Desktop](https://claude.ai/download)
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) 
- Clone repo: `git clone https://github.com/SeanPedersen/youtube-transcript-mcp`
- `cd youtube-transcript-mcp/`
- Setup environment: `uv venv && uv pip install -r pyproject.toml && source .venv/bin/activate`
- Install the MCP server: `fastmcp install claude-desktop mcp_server.py --with youtube-transcript-api`
- Restart Claude Desktop (Digger Solo app needs to be running)

## Usage

Example prompt: Summarize https://www.youtube.com/watch?v=uB9yZenVLzg
