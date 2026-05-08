# youtube-transcript-mcp

[![PyPI](https://img.shields.io/pypi/v/youtube-transcript-mcp-server.svg)](https://pypi.org/project/youtube-transcript-mcp-server/)

Transcribe YouTube videos for LLM chat apps via [MCP](https://modelcontextprotocol.io/).

Example prompt: `Summarize https://www.youtube.com/watch?v=uB9yZenVLzg`

## Install

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). Add this to your MCP client's config — works for any MCP-compatible app (Claude Desktop, Claude Code, Cursor, Windsurf, VS Code, Zed, …):

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": ["youtube-transcript-mcp-server"]
    }
  }
}
```

Equivalent one-liner if your client wants a single command:

```bash
uvx youtube-transcript-mcp-server
```

## Tool

- `transcribe(youtube_video_url: str) -> str` — fetches the transcript (en/de/es/fr/ru) and prepends an ad-removal instruction for the LLM.

## Develop locally

```bash
git clone https://github.com/SeanPedersen/youtube-transcript-mcp
cd youtube-transcript-mcp
uv venv && uv pip install -r pyproject.toml && source .venv/bin/activate
python mcp_server.py
```

Point your MCP client at the local checkout instead of PyPI:

```json
{
  "command": "uv",
  "args": [
    "run", "--with", "fastmcp", "--with", "youtube-transcript-api",
    "fastmcp", "run", "/absolute/path/to/youtube-transcript-mcp/mcp_server.py"
  ]
}
```
