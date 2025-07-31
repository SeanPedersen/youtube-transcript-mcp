import re
from fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP("YouTube transcription service")


@mcp.tool
def transcribe(youtube_video_url: str) -> str:
    """
    Transcribe a YouTube video using its URL.
    """
    # Extract video ID using regex to handle various YouTube URL formats
    video_id_pattern = (
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})"
    )
    match = re.search(video_id_pattern, youtube_video_url)

    if not match:
        raise ValueError("Invalid YouTube URL format")

    video_id = match.group(1)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    adblock_prompt = "Remove any mention of sponsorships, ads, or promotional content from the following transcript:\n\n"
    transcript_text = "\n".join(snippet.text for snippet in transcript)
    return adblock_prompt + transcript_text


if __name__ == "__main__":
    mcp.run()
