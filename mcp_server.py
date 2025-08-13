import re
import os
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
    """Extract video ID from YouTube URL."""
    video_id_pattern = (
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})"
    )
    match = re.search(video_id_pattern, youtube_video_url)
    if not match:
        raise ValueError("Invalid YouTube URL format")
    return match.group(1)




@mcp.tool
def transcribe(youtube_video_url: str) -> str:
    """
    Transcribe a YouTube video using its URL.
    """
    video_id = get_video_id_from_url(youtube_video_url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    adblock_prompt = "Remove any mention of sponsorships, ads, or promotional content from the following transcript:\n\n"
    transcript_text = "\n".join(snippet.text for snippet in transcript)
    return adblock_prompt + transcript_text


@mcp.tool
def transcribe_to_file(youtube_video_url: str, output_file: str = None) -> str:
    """
    Transcribe a YouTube video and save the transcript to a file.
    Returns a confirmation message instead of the full transcript.
    
    Args:
        youtube_video_url: The YouTube video URL to transcribe
        output_file: Optional path to save the transcript. If not provided, 
                    generates filename from video ID as 'transcript_{video_id}.txt'
    """
    video_id = get_video_id_from_url(youtube_video_url)
    
    # Generate filename if not provided
    if output_file is None:
        output_file = f"transcript_{video_id}.txt"
    
    # Ensure the output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get transcript
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    transcript_text = "\n".join(snippet.text for snippet in transcript)
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"YouTube Video Transcript\n")
        f.write(f"Video ID: {video_id}\n")
        f.write(f"URL: {youtube_video_url}\n")
        f.write("="*50 + "\n\n")
        f.write(transcript_text)
    
    # Return confirmation
    file_size = output_path.stat().st_size
    return f"Transcript saved to '{output_file}' ({file_size:,} bytes, {len(transcript_text):,} characters)"




if __name__ == "__main__":
    mcp.run()
