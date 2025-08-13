import re
from pathlib import Path
from fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP("YouTube transcription service")


def sanitize_filename(filename: str) -> str:
    """Sanitize a string to be safe for use as a filename."""
    # Remove or replace characters that are problematic in filenames
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple consecutive underscores
    filename = re.sub(r'_+', '_', filename)
    # Strip leading/trailing whitespace and dots
    filename = filename.strip(' .')
    # Limit length to 255 characters (filesystem limit)
    if len(filename) > 255:
        filename = filename[:252] + '...'
    return filename


def get_video_id_from_url(youtube_video_url: str) -> str:
    video_id_pattern = (
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{10,11})"
    )
    match = re.search(video_id_pattern, youtube_video_url)
    if not match:
        raise ValueError("Invalid YouTube URL format")
    return match.group(1)


def validate_output_path(output_file: str) -> Path:
    path = Path(output_file)
    resolved_path = path.resolve()
    cwd = Path.cwd().resolve()
    
    try:
        resolved_path.relative_to(cwd)
    except ValueError:
        raise ValueError(f"Output path '{output_file}' is outside the allowed directory")
    
    sanitized_name = sanitize_filename(path.name)
    if not sanitized_name or sanitized_name == '.':
        raise ValueError(f"Invalid filename: '{path.name}'")
    
    return path.parent / sanitized_name




def get_transcript_text(video_id: str) -> str:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    transcript_text = "\n".join(snippet.text for snippet in transcript)
    return transcript_text


@mcp.tool
def transcribe(youtube_video_url: str) -> str:
    adblock_prompt = "Remove any mention of sponsorships, ads, or promotional content from the following transcript:\n\n"
    video_id = get_video_id_from_url(youtube_video_url)
    return adblock_prompt + get_transcript_text(video_id)


@mcp.tool
def transcribe_to_file(youtube_video_url: str, output_file: str = None) -> str:
    try:
        video_id = get_video_id_from_url(youtube_video_url)
        
        if output_file is None:
            output_file = f"transcript_{video_id}.txt"
        
        output_path = validate_output_path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        transcript_text = get_transcript_text(video_id)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"YouTube Video Transcript\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {youtube_video_url}\n")
            f.write("="*50 + "\n\n")
            f.write(transcript_text)
        
        file_size = output_path.stat().st_size
        return f"Transcript saved to '{output_path}' ({file_size:,} bytes, {len(transcript_text):,} characters)"
    
    except Exception as e:
        return f"Error: {e}"




if __name__ == "__main__":
    mcp.run()
