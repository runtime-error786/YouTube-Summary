from youtube_transcript_api import YouTubeTranscriptApi
from phi.model.groq import Groq
from phi.agent import Agent, RunResponse

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    if "youtube.com" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be" in url:
        return url.split("/")[-1]
    else:
        return None

def fetch_transcript(video_url, language="en"):
    """Fetch transcript for the given YouTube video in the specified language."""
    video_id = get_video_id(video_url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return {"transcript": transcript}
    except Exception as e:
        if "No transcripts were found" in str(e):
            return {"error": f"No captions found in {language}. Try another language or auto-generated captions."}
        return {"error": str(e)}

def get_full_transcript(transcript):
    """Concatenate all transcript texts."""
    if "transcript" not in transcript:
        return "No transcript available."
    return " ".join([item['text'] for item in transcript['transcript']])

def summarize_text_with_groq(text):
    """Summarize the given text using the Groq model."""
    api_key = "set api key here"
    agent = Agent(
        model=Groq(id="llama-3.2-3b-preview", api_key=api_key),
        markdown=True
    )
    
    run: RunResponse = agent.run(f"Summarize this text: {text}")
    
    return run.content
